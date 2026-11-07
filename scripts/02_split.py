"""Step 2: clean, dedup, grouped class-stratified train/val/test split.

Order matters (nothing here is learned from data, so no leakage):
  1. +-Inf -> NaN (row-wise rule; imputation values are learned later, on train only)
  2. drop exact duplicates (same features + label, kept once, global across files)
  3. drop conflicting rows (same features, different label)
  4. group = contiguous block of BLOCK_ROWS rows in one day file (capture order);
     this release has no IP/timestamp, so a block stands in for "one session window"
  5. StratifiedGroupKFold(5): folds 0-2 train, 3 val, 4 test; whole groups never split

Run:  .venv/bin/python -I scripts/02_split.py
"""
import json

import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedGroupKFold

from socalert.config import (
    BLOCK_ROWS,
    CLASSES,
    INTERIM_DIR,
    LABEL_COL,
    N_FOLDS,
    PROCESSED_DIR,
    REPORTS_DIR,
    SEED,
    TEST_FOLDS,
    TRAIN_FOLDS,
    VAL_FOLDS,
)
from socalert.data import feature_columns


def counts(df: pd.DataFrame) -> dict:
    return {c: int((df[LABEL_COL] == c).sum()) for c in CLASSES}


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_parquet(INTERIM_DIR / "cic3_raw.parquet")
    feats = feature_columns(df)
    steps = {"raw": counts(df)}

    # 1. Inf -> NaN
    arr = df[feats].to_numpy()
    n_inf_cells = int(np.isinf(arr).sum())
    df[feats] = df[feats].replace([np.inf, -np.inf], np.nan)

    # 2. exact duplicates
    df = df[~df.duplicated(subset=feats + [LABEL_COL], keep="first")]
    steps["after_exact_dedup"] = counts(df)

    # 3. conflicting labels on identical features
    conflict = df.duplicated(subset=feats, keep=False)
    df = df[~conflict].reset_index(drop=True)
    steps["after_conflict_drop"] = counts(df)

    # 4. groups
    df["group"] = df["src_file"] + ":" + (df["row_id"] // BLOCK_ROWS).astype(str)
    df["uid"] = df["src_file"] + ":" + df["row_id"].astype(str)

    # 5. grouped, class-stratified folds
    sgkf = StratifiedGroupKFold(n_splits=N_FOLDS, shuffle=True, random_state=SEED)
    fold = np.full(len(df), -1, dtype=np.int8)
    for k, (_, idx) in enumerate(sgkf.split(df, df[LABEL_COL], df["group"])):
        fold[idx] = k
    assert (fold >= 0).all()
    df["fold"] = fold

    parts = {
        "train": df[df["fold"].isin(TRAIN_FOLDS)],
        "val": df[df["fold"].isin(VAL_FOLDS)],
        "test": df[df["fold"].isin(TEST_FOLDS)],
    }

    # integrity checks
    g = {k: set(v["group"]) for k, v in parts.items()}
    assert not (g["train"] & g["val"] or g["train"] & g["test"] or g["val"] & g["test"])
    h = {k: set(pd.util.hash_pandas_object(v[feats], index=False)) for k, v in parts.items()}
    feat_overlap = {
        "train&val": len(h["train"] & h["val"]),
        "train&test": len(h["train"] & h["test"]),
        "val&test": len(h["val"] & h["test"]),
    }
    assert sum(feat_overlap.values()) == 0, feat_overlap

    rep = {
        "block_rows": BLOCK_ROWS,
        "seed": SEED,
        "inf_cells_replaced_with_nan": n_inf_cells,
        "pipeline_counts": steps,
        "splits": {},
        "feature_vector_overlap_between_splits": feat_overlap,
        "group_overlap_between_splits": 0,
    }
    total = len(df)
    for name, p in parts.items():
        c = counts(p)
        rep["splits"][name] = {
            "rows": int(len(p)),
            "share_of_rows": round(len(p) / total, 4),
            "n_groups": int(p["group"].nunique()),
            "class_counts": c,
            "class_share": {k: round(v / len(p), 5) for k, v in c.items()},
            "class_share_of_class_total": {
                k: round(v / steps["after_conflict_drop"][k], 4) for k, v in c.items()
            },
            "rows_with_nan": int(p[feats].isna().any(axis=1).sum()),
        }
        p.to_parquet(PROCESSED_DIR / f"{name}.parquet", index=False)

    (REPORTS_DIR / "02_split_report.json").write_text(json.dumps(rep, indent=2))

    lines = [
        "# Split report",
        "",
        f"Group = {BLOCK_ROWS} consecutive rows of one day file. "
        f"StratifiedGroupKFold({N_FOLDS}), seed {SEED}: folds {TRAIN_FOLDS} train, "
        f"{VAL_FOLDS} val, {TEST_FOLDS} test.",
        "",
        "## Cleaning steps (rows per class)",
        "",
        "| step | " + " | ".join(CLASSES) + " |",
        "|---|" + "---:|" * len(CLASSES),
    ]
    for s, c in steps.items():
        lines.append(f"| {s} | " + " | ".join(f"{c[k]:,}" for k in CLASSES) + " |")
    lines += [
        "",
        "## Splits",
        "",
        "| split | rows | groups | " + " | ".join(CLASSES) + " |",
        "|---|---:|---:|" + "---:|" * len(CLASSES),
    ]
    for name, s in rep["splits"].items():
        lines.append(
            f"| {name} | {s['rows']:,} | {s['n_groups']} | "
            + " | ".join(
                f"{s['class_counts'][k]:,} ({s['class_share_of_class_total'][k]:.1%} of class)"
                for k in CLASSES
            )
            + " |"
        )
    lines += [
        "",
        f"Checks: group overlap between splits = 0; identical feature vectors across splits = {feat_overlap}.",
    ]
    (REPORTS_DIR / "02_split_report.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
