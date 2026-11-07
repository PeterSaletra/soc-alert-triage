"""Classic IDS: median imputation + train-only feature selection + Random Forest.

Everything learned from data (impute medians, kept features, trees) is fitted in
`IDSModel.fit` on the frame it is given. Call it on a train fold only.
"""
from dataclasses import dataclass, field

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer

from .config import CLASSES, LABEL_COL, SEED


def _clean(X: pd.DataFrame) -> pd.DataFrame:
    return X.replace([np.inf, -np.inf], np.nan)


@dataclass
class IDSModel:
    rf_params: dict = field(default_factory=dict)
    corr_threshold: float = 0.98
    top_k: int = 30
    drop_features: tuple = ()  # excluded up front (ablations)
    seed: int = SEED

    # learned
    all_feats_: list = None
    imputer_: SimpleImputer = None
    selected_: list = None
    selection_log_: dict = None
    rf_: RandomForestClassifier = None
    classes_: list = None

    # ---- feature selection (train only) -------------------------------------
    def _select(self, Xi: pd.DataFrame, y: pd.Series) -> list:
        log = {"start": Xi.shape[1]}

        const = [c for c in Xi.columns if Xi[c].nunique() <= 1]
        Xi = Xi.drop(columns=const)
        log["constant_dropped"] = const

        corr = Xi.corr().abs().to_numpy()
        cols = list(Xi.columns)
        drop = set()
        for i in range(len(cols)):
            if cols[i] in drop:
                continue
            for j in range(i + 1, len(cols)):
                if cols[j] not in drop and corr[i, j] > self.corr_threshold:
                    drop.add(cols[j])
        log["correlated_dropped"] = sorted(drop)
        Xi = Xi.drop(columns=list(drop))
        log["after_variance_corr"] = Xi.shape[1]

        # importance ranking on a stratified train subsample (cheap, train-only)
        rng = np.random.RandomState(self.seed)
        take = []
        for c in y.unique():
            idx = np.flatnonzero((y == c).to_numpy())
            take.append(rng.choice(idx, size=min(len(idx), 30000), replace=False))
        take = np.concatenate(take)
        probe = RandomForestClassifier(
            n_estimators=60, n_jobs=-1, random_state=self.seed
        ).fit(Xi.iloc[take], y.iloc[take])
        imp = pd.Series(probe.feature_importances_, index=Xi.columns).sort_values(
            ascending=False
        )
        keep = list(imp.index[: self.top_k])
        log["importance_top_k"] = {k: round(float(imp[k]), 5) for k in keep}
        log["final"] = len(keep)
        self.selection_log_ = log
        return keep

    # ---- fit / predict --------------------------------------------------------
    def fit(self, df: pd.DataFrame, feats: list):
        self.all_feats_ = [f for f in feats if f not in self.drop_features]
        X = _clean(df[self.all_feats_])
        y = df[LABEL_COL]
        self.imputer_ = SimpleImputer(strategy="median").fit(X)
        Xi = pd.DataFrame(self.imputer_.transform(X), columns=self.all_feats_, index=df.index)

        self.selected_ = self._select(Xi, y)
        params = dict(n_estimators=100, n_jobs=-1, random_state=self.seed)
        params.update(self.rf_params)
        self.rf_ = RandomForestClassifier(**params).fit(Xi[self.selected_], y)
        self.classes_ = list(self.rf_.classes_)
        return self

    def _matrix(self, df: pd.DataFrame) -> pd.DataFrame:
        X = _clean(df[self.all_feats_])
        Xi = pd.DataFrame(self.imputer_.transform(X), columns=self.all_feats_, index=df.index)
        return Xi[self.selected_]

    def predict_proba(self, df: pd.DataFrame) -> pd.DataFrame:
        p = self.rf_.predict_proba(self._matrix(df))
        return pd.DataFrame(p, columns=self.classes_, index=df.index)[CLASSES]

    def predict(self, df: pd.DataFrame) -> pd.Series:
        return self.predict_proba(df).idxmax(axis=1)

    def save(self, path):
        joblib.dump(self, path, compress=3)

    @staticmethod
    def load(path) -> "IDSModel":
        return joblib.load(path)
