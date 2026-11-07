"""Step 4: turn IDS predictions into alerts and alert cards.

Alert = IDS predicted an attack class. For val and test writes
data/processed/alerts_{split}.jsonl with, per alert:
  id, card (text for the LLM), ids_pred, ids_proba, observations,
  reference {label, outcome}   <- evaluation only, never feed to the LLM
and reports/04_alert_cards_sample.md (every test false alarm + a few true alerts).

Note: val/test alerts come from an IDS fitted on train, so they are out-of-sample.
Train-split alerts for Llama need out-of-fold IDS predictions (separate step).

Run:  .venv/bin/python -I scripts/04_alert_cards.py
"""
import json

import numpy as np
import pandas as pd

from socalert.cards import CARD_COLUMNS, build_card, flow_observations
from socalert.config import CLASSES, LABEL_COL, PROCESSED_DIR, REPORTS_DIR, SEED


def outcome(label: str, pred: str) -> str:
    if label == pred:
        return "true_alert"
    return "false_alarm" if label == "BENIGN" else "wrong_attack_type"


def build_alerts(split: str) -> list:
    pred = pd.read_parquet(PROCESSED_DIR / f"{split}_pred.parquet")
    pred = pred[pred["pred"] != "BENIGN"]
    feats = pd.read_parquet(
        PROCESSED_DIR / f"{split}.parquet", columns=["uid"] + CARD_COLUMNS
    ).set_index("uid")
    records = []
    for r in pred.to_dict("records"):
        row = feats.loc[r["uid"]]
        proba = {c: float(r[f"p_{c}"]) for c in CLASSES}
        aid = f"{split}-{r['uid']}"
        label = r[LABEL_COL]
        records.append(
            {
                "id": aid,
                "card": build_card(aid, row, proba),
                "ids_pred": r["pred"],
                "ids_proba": proba,
                "observations": flow_observations(row),
                "reference": {"label": label, "outcome": outcome(label, r["pred"])},
            }
        )
    return records


def main() -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    summary, test_alerts = {}, None
    for split in ("val", "test"):
        alerts = build_alerts(split)
        with open(PROCESSED_DIR / f"alerts_{split}.jsonl", "w") as f:
            for a in alerts:
                f.write(json.dumps(a) + "\n")
        oc = pd.Series([a["reference"]["outcome"] for a in alerts]).value_counts().to_dict()
        by_pred = (
            pd.crosstab(
                [a["ids_pred"] for a in alerts], [a["reference"]["outcome"] for a in alerts]
            )
            .to_dict("index")
        )
        # Trivial reference triage Llama has to beat: reject alerts the IDS itself is unsure about.
        is_fa = np.array([a["reference"]["outcome"] == "false_alarm" for a in alerts])
        conf = np.array([max(a["ids_proba"].values()) for a in alerts])
        baseline = {
            f"reject_if_ids_conf_below_{t}": {
                "false_alarms_rejected": int((is_fa & (conf < t)).sum()),
                "false_alarms_total": int(is_fa.sum()),
                "other_alerts_rejected": int((~is_fa & (conf < t)).sum()),
                "other_alerts_total": int((~is_fa).sum()),
            }
            for t in (0.6, 0.7, 0.8, 0.9)
        }
        summary[split] = {
            "n_alerts": len(alerts),
            "outcomes": oc,
            "by_ids_pred": by_pred,
            "confidence_threshold_baseline": baseline,
        }
        if split == "test":
            test_alerts = alerts

    (REPORTS_DIR / "04_alert_cards_summary.json").write_text(json.dumps(summary, indent=2))

    rng = np.random.RandomState(SEED)
    fa = [a for a in test_alerts if a["reference"]["outcome"] == "false_alarm"]
    ta = [a for a in test_alerts if a["reference"]["outcome"] == "true_alert"]
    sample_true = []
    for cls in ("DoS Hulk", "FTP-Patator"):
        pool = [a for a in ta if a["ids_pred"] == cls]
        sample_true += [pool[i] for i in rng.choice(len(pool), size=3, replace=False)]

    md = [
        "# Alert card samples (test split)",
        "",
        f"Test alerts: {summary['test']['n_alerts']:,} · outcomes {summary['test']['outcomes']}.",
        "Cards below are the exact LLM input text. The `Reference` line is evaluation-only and is not part of the card.",
        "",
        f"## False alarms ({len(fa)}: real BENIGN flagged by IDS)",
        "",
    ]
    for a in fa:
        md += ["```text", a["card"], "```", f"Reference: {a['reference']}", ""]
    md += ["## True alerts (random sample, 3 per attack)", ""]
    for a in sample_true:
        md += ["```text", a["card"], "```", f"Reference: {a['reference']}", ""]
    (REPORTS_DIR / "04_alert_cards_sample.md").write_text("\n".join(md))
    print(json.dumps(summary, indent=2))
    print("\n--- example false-alarm card ---\n" + fa[0]["card"])
    print("\n--- example true-alert card ---\n" + sample_true[-1]["card"])


if __name__ == "__main__":
    main()
