"""Loading of the raw CIC-IDS2017 MachineLearningCVE CSVs."""
from pathlib import Path

import pandas as pd

from .config import CLASSES, LABEL_COL


def load_raw(raw_dir: Path):
    """Read every day file, keep the three target classes.

    Returns (df, all_label_counts). `df` has the 77 flow features, `Label`,
    `src_file` and `row_id` (row position inside the day file, i.e. capture order).
    Feature values are untouched (NaN / +-Inf kept as in the CSV).
    """
    files = sorted(raw_dir.glob("*.csv"))
    if not files:
        raise FileNotFoundError(f"no CSV files in {raw_dir}")

    parts, all_counts = [], {}
    for f in files:
        # latin-1: the WebAttacks file has a non-UTF8 byte in its label names.
        df = pd.read_csv(f, encoding="latin-1", skipinitialspace=True, low_memory=False)
        df.columns = [c.strip() for c in df.columns]
        # CICFlowMeter writes "Fwd Header Length" twice; verified identical.
        if "Fwd Header Length.1" in df.columns:
            if not df["Fwd Header Length"].equals(df["Fwd Header Length.1"]):
                raise ValueError(f"{f.name}: duplicated header column differs")
            df = df.drop(columns="Fwd Header Length.1")
        df[LABEL_COL] = df[LABEL_COL].str.strip()
        for k, v in df[LABEL_COL].value_counts().items():
            all_counts[k] = all_counts.get(k, 0) + int(v)

        df["src_file"] = f.stem.replace(".pcap_ISCX", "")
        df["row_id"] = range(len(df))
        parts.append(df[df[LABEL_COL].isin(CLASSES)])

    out = pd.concat(parts, ignore_index=True)
    return out, all_counts


def feature_columns(df: pd.DataFrame) -> list:
    from .config import META_COLS

    return [c for c in df.columns if c != LABEL_COL and c not in META_COLS]
