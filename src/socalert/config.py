"""Shared paths and constants for the CIC-IDS2017 three-class pipeline."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = ROOT / "data" / "raw" / "cicids2017_ml"
INTERIM_DIR = ROOT / "data" / "interim"
PROCESSED_DIR = ROOT / "data" / "processed"
MODELS_DIR = ROOT / "models"
REPORTS_DIR = ROOT / "reports"

LABEL_COL = "Label"
CLASSES = ["BENIGN", "DoS Hulk", "FTP-Patator"]
ATTACK_CLASSES = ["DoS Hulk", "FTP-Patator"]

SEED = 42

# This CSV release has no IP / timestamp / flow id, so "closely related flows"
# are approximated by contiguous row blocks of one day file (files are in
# capture order). One block = one split group.
BLOCK_ROWS = 2000

# 5 folds of grouped, class-stratified split: 3 train, 1 val, 1 test (60/20/20).
N_FOLDS = 5
TRAIN_FOLDS = (0, 1, 2)
VAL_FOLDS = (3,)
TEST_FOLDS = (4,)

# Bookkeeping columns, never used as model features.
META_COLS = ["src_file", "row_id", "group", "uid"]
