"""Evaluation helpers shared by the IDS and (later) the Llama head."""
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    precision_recall_fscore_support,
)

from .config import ATTACK_CLASSES, CLASSES


def evaluate(y_true: pd.Series, y_pred: pd.Series) -> dict:
    p, r, f, s = precision_recall_fscore_support(
        y_true, y_pred, labels=CLASSES, zero_division=0
    )
    cm = confusion_matrix(y_true, y_pred, labels=CLASSES)
    per_class = {
        c: {
            "precision": float(p[i]),
            "recall": float(r[i]),
            "f1": float(f[i]),
            "support": int(s[i]),
        }
        for i, c in enumerate(CLASSES)
    }
    return {
        "labels": CLASSES,
        "confusion_matrix": cm.tolist(),  # rows = true, cols = predicted
        "per_class": per_class,
        "macro_f1": float(sum(v["f1"] for v in per_class.values()) / len(CLASSES)),
        "macro_f1_attacks_only": float(
            sum(per_class[c]["f1"] for c in ATTACK_CLASSES) / len(ATTACK_CLASSES)
        ),
        "accuracy": float(accuracy_score(y_true, y_pred)),
    }


def alert_outcomes(y_true: pd.Series, y_pred: pd.Series) -> dict:
    """Break IDS output into what triage will see.

    alert = IDS predicted an attack class.
      true_alert        : predicted attack == true attack
      wrong_attack_type : real attack, other attack class predicted
      false_alarm       : true BENIGN flagged as an attack
    missed_attack: real attack predicted BENIGN (never becomes an alert).
    """
    alert = y_pred != "BENIGN"
    attack = y_true != "BENIGN"
    out = {
        "n_alerts": int(alert.sum()),
        "true_alert": int((alert & (y_pred == y_true)).sum()),
        "wrong_attack_type": int((alert & attack & (y_pred != y_true)).sum()),
        "false_alarm": int((alert & ~attack).sum()),
        "missed_attack": int((~alert & attack).sum()),
    }
    out["false_alarm_by_predicted_class"] = {
        c: int((alert & ~attack & (y_pred == c)).sum()) for c in ATTACK_CLASSES
    }
    out["alert_precision"] = out["true_alert"] / out["n_alerts"] if out["n_alerts"] else None
    return out


def cm_markdown(m: dict) -> str:
    labels = m["labels"]
    lines = [
        "| true \\ pred | " + " | ".join(labels) + " |",
        "|---|" + "---:|" * len(labels),
    ]
    for lab, row in zip(labels, m["confusion_matrix"]):
        lines.append(f"| **{lab}** | " + " | ".join(f"{v:,}" for v in row) + " |")
    return "\n".join(lines)
