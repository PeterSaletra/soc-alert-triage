"""Step 3: baseline Random Forest IDS.

Feature selection + imputation + RF are fitted on train only. A tiny RF config
sweep is judged on validation (macro-F1); the chosen config is scored on test once.
Also scores an ablation without `Destination Port` (report only, not used for choice).

Writes models/ids_rf.joblib, data/processed/{val,test}_pred.parquet and
reports/03_rf_report.json + .md.

Run:  .venv/bin/python -I scripts/03_train_rf.py
"""
import json
import time

import pandas as pd

from socalert.config import CLASSES, LABEL_COL, MODELS_DIR, PROCESSED_DIR, REPORTS_DIR
from socalert.data import feature_columns
from socalert.ids import IDSModel
from socalert.metrics import alert_outcomes, cm_markdown, evaluate

CONFIGS = {
    "rf_default": {},
    "rf_balanced": {"class_weight": "balanced_subsample"},
    "rf_leaf5": {"min_samples_leaf": 5},
}


def pred_frame(model: IDSModel, df: pd.DataFrame) -> pd.DataFrame:
    proba = model.predict_proba(df)
    out = df[["uid", "src_file", "row_id", "group", LABEL_COL]].copy()
    out["pred"] = proba.idxmax(axis=1)
    for c in CLASSES:
        out[f"p_{c}"] = proba[c]
    return out


def main() -> None:
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    train = pd.read_parquet(PROCESSED_DIR / "train.parquet")
    val = pd.read_parquet(PROCESSED_DIR / "val.parquet")
    test = pd.read_parquet(PROCESSED_DIR / "test.parquet")
    feats = feature_columns(train)

    rep = {"sweep_val": {}}
    best_name, best_f1, best_model = None, -1.0, None
    for name, params in CONFIGS.items():
        t0 = time.time()
        m = IDSModel(rf_params=params).fit(train, feats)
        fit_s = time.time() - t0
        ev = evaluate(val[LABEL_COL], m.predict(val))
        rep["sweep_val"][name] = {"params": params, "fit_seconds": round(fit_s, 1), **ev}
        print(f"{name}: val macro-F1 {ev['macro_f1']:.5f}  ({fit_s:.0f}s)", flush=True)
        if ev["macro_f1"] > best_f1:
            best_name, best_f1, best_model = name, ev["macro_f1"], m

    rep["chosen"] = best_name
    rep["feature_selection"] = best_model.selection_log_
    rep["selected_features"] = best_model.selected_
    best_model.save(MODELS_DIR / "ids_rf.joblib")

    val_pred = pred_frame(best_model, val)
    test_pred = pred_frame(best_model, test)
    val_pred.to_parquet(PROCESSED_DIR / "val_pred.parquet", index=False)
    test_pred.to_parquet(PROCESSED_DIR / "test_pred.parquet", index=False)

    rep["val"] = {
        **evaluate(val_pred[LABEL_COL], val_pred["pred"]),
        "alerts": alert_outcomes(val_pred[LABEL_COL], val_pred["pred"]),
    }
    rep["test"] = {
        **evaluate(test_pred[LABEL_COL], test_pred["pred"]),
        "alerts": alert_outcomes(test_pred[LABEL_COL], test_pred["pred"]),
    }

    # Ablation: shortcut check, port removed. Report only.
    abl = IDSModel(rf_params=CONFIGS[best_name], drop_features=("Destination Port",)).fit(
        train, feats
    )
    abl_pred = abl.predict(test)
    rep["test_no_destination_port"] = {
        **evaluate(test[LABEL_COL], abl_pred),
        "alerts": alert_outcomes(test[LABEL_COL], abl_pred),
    }

    (REPORTS_DIR / "03_rf_report.json").write_text(json.dumps(rep, indent=2), encoding="utf-8")
    md = render(rep)
    (REPORTS_DIR / "03_rf_report.md").write_text(md, encoding="utf-8")
    print(md)


def per_class_table(ev: dict) -> str:
    lines = ["| class | precision | recall | F1 | support |", "|---|---:|---:|---:|---:|"]
    for c, v in ev["per_class"].items():
        lines.append(
            f"| {c} | {v['precision']:.4f} | {v['recall']:.4f} | {v['f1']:.4f} | {v['support']:,} |"
        )
    lines.append(f"\nmacro-F1 {ev['macro_f1']:.4f} · accuracy {ev['accuracy']:.4f}")
    return "\n".join(lines)


def render(rep: dict) -> str:
    out = ["# Baseline Random Forest report", ""]
    out += ["## Validation sweep (macro-F1)", "", "| config | params | macro-F1 | fit s |", "|---|---|---:|---:|"]
    for n, v in rep["sweep_val"].items():
        out.append(f"| {n} | `{v['params']}` | {v['macro_f1']:.5f} | {v['fit_seconds']} |")
    out += ["", f"Chosen: **{rep['chosen']}**", ""]
    fs = rep["feature_selection"]
    out += [
        "## Feature selection (fitted on train)",
        "",
        f"{fs['start']} features → constant dropped {len(fs['constant_dropped'])} "
        f"→ correlated (|r|>0.98) dropped {len(fs['correlated_dropped'])} "
        f"→ top-{fs['final']} by RF importance.",
        "",
        "Kept: " + ", ".join(f"`{k}`" for k in rep["selected_features"]),
        "",
    ]
    for title, key in (("Test", "test"), ("Validation", "val"), ("Test, ablation without Destination Port", "test_no_destination_port")):
        ev = rep[key]
        out += [f"## {title}", "", cm_markdown(ev), "", per_class_table(ev), ""]
        a = ev["alerts"]
        out += [
            f"Alerts (IDS predicted an attack): **{a['n_alerts']:,}** → true {a['true_alert']:,}, "
            f"wrong attack type {a['wrong_attack_type']:,}, **false alarms {a['false_alarm']:,}** "
            f"(by predicted class {a['false_alarm_by_predicted_class']}); "
            f"missed attacks (predicted BENIGN) {a['missed_attack']:,}.",
            "",
        ]
    return "\n".join(out)


if __name__ == "__main__":
    main()
