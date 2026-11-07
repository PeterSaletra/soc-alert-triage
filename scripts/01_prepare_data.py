"""Step 1: load CIC-IDS2017, keep BENIGN / DoS Hulk / FTP-Patator, audit data quality.

Writes data/interim/cic3_raw.parquet (values untouched) and
reports/01_data_report.json + .md (class counts, NaN, Inf, duplicates).

Run:  .venv/bin/python -I scripts/01_prepare_data.py
"""
import json

import numpy as np
import pandas as pd

from socalert.config import CLASSES, INTERIM_DIR, LABEL_COL, RAW_DIR, REPORTS_DIR
from socalert.data import feature_columns, load_raw


def audit(df: pd.DataFrame, feats: list) -> dict:
    X = df[feats]
    y = df[LABEL_COL]
    is_nan = X.isna()
    is_inf = pd.DataFrame(np.isinf(X.to_numpy()), columns=feats, index=df.index)

    def per_class(mask: pd.Series) -> dict:
        return {c: int(mask[y == c].sum()) for c in CLASSES}

    rep = {
        "rows_total": int(len(df)),
        "class_counts": {c: int((y == c).sum()) for c in CLASSES},
        "n_features": len(feats),
        "nan": {
            "rows_with_nan_per_class": per_class(is_nan.any(axis=1)),
            "cells_per_column": {c: int(n) for c, n in is_nan.sum().items() if n},
        },
        "inf": {
            "rows_with_inf_per_class": per_class(is_inf.any(axis=1)),
            "cells_per_column": {c: int(n) for c, n in is_inf.sum().items() if n},
            "pos_inf_cells": int(np.isposinf(X.to_numpy()).sum()),
            "neg_inf_cells": int(np.isneginf(X.to_numpy()).sum()),
        },
    }

    # Exact duplicates: identical feature vector AND label (extra copies only).
    dup_row = df.duplicated(subset=feats + [LABEL_COL], keep="first")
    # Conflicts: identical feature vector under different labels.
    uniq = df.loc[~dup_row, feats + [LABEL_COL]]
    conflict = uniq.duplicated(subset=feats, keep=False)
    conflict_labels = uniq.loc[conflict, LABEL_COL].value_counts()
    rep["duplicates"] = {
        "exact_dup_rows_per_class": per_class(dup_row),
        "exact_dup_rows_total": int(dup_row.sum()),
        "rows_after_exact_dedup_per_class": {
            c: int(((y == c) & ~dup_row).sum()) for c in CLASSES
        },
        "conflicting_unique_rows_per_class": {
            c: int(conflict_labels.get(c, 0)) for c in CLASSES
        },
    }
    # Same capture day contributes duplicates across files? (global dedup is used)
    rep["duplicates"]["dup_rows_across_files_only"] = int(
        dup_row.sum()
        - df.duplicated(subset=feats + [LABEL_COL, "src_file"], keep="first").sum()
    )
    return rep


def to_markdown(rep: dict) -> str:
    cc = rep["class_counts"]
    dd = rep["duplicates"]
    lines = [
        "# Data report: CIC-IDS2017 (MachineLearningCVE), three classes",
        "",
        "Source: HF mirror `c01dsnap/CIC-IDS2017` (original CSVs; official UNB link is dead).",
        "",
        "## Class counts (all 8 day files)",
        "",
        "| class | rows | exact dup rows | rows after dedup | NaN rows | Inf rows | in conflict* |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for c in CLASSES:
        lines.append(
            f"| {c} | {cc[c]:,} | {dd['exact_dup_rows_per_class'][c]:,} | "
            f"{dd['rows_after_exact_dedup_per_class'][c]:,} | "
            f"{rep['nan']['rows_with_nan_per_class'][c]:,} | "
            f"{rep['inf']['rows_with_inf_per_class'][c]:,} | "
            f"{dd['conflicting_unique_rows_per_class'][c]:,} |"
        )
    lines += [
        "",
        "*conflict = same feature vector appears under more than one label (unique rows).",
        "",
        f"Total rows {rep['rows_total']:,}; features {rep['n_features']}.",
        f"NaN columns: {rep['nan']['cells_per_column']}",
        f"Inf columns: {rep['inf']['cells_per_column']}",
        "",
        "## Original label counts (all 15 labels, before filtering)",
        "",
        "| label | rows |",
        "|---|---:|",
    ]
    for k, v in sorted(rep["all_label_counts"].items(), key=lambda kv: -kv[1]):
        lines.append(f"| {k} | {v:,} |")
    return "\n".join(lines) + "\n"


def main() -> None:
    INTERIM_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    df, all_counts = load_raw(RAW_DIR)
    feats = feature_columns(df)
    rep = audit(df, feats)
    rep["all_label_counts"] = all_counts

    df.to_parquet(INTERIM_DIR / "cic3_raw.parquet", index=False)
    (REPORTS_DIR / "01_data_report.json").write_text(json.dumps(rep, indent=2))
    (REPORTS_DIR / "01_data_report.md").write_text(to_markdown(rep))
    print(to_markdown(rep))


if __name__ == "__main__":
    main()
