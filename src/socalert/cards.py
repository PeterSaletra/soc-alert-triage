"""Alert cards: fixed-format English text built from flow observations + IDS output.

The reference label is NEVER part of the card text. It travels separately in the
`reference` field of the JSONL record, for evaluation only.
"""
import math

from .config import CLASSES

# (column, label shown on the card, number format)
CARD_FIELDS = [
    ("Destination Port", "Destination port", "int"),
    ("Flow Duration", "Flow duration (microseconds)", "int"),
    ("Total Fwd Packets", "Forward packets", "int"),
    ("Total Backward Packets", "Backward packets", "int"),
    ("Total Length of Fwd Packets", "Forward bytes", "int"),
    ("Total Length of Bwd Packets", "Backward bytes", "int"),
    ("Flow Bytes/s", "Flow bytes per second", "f2"),
    ("Flow Packets/s", "Flow packets per second", "f2"),
    ("Fwd Packet Length Mean", "Mean forward packet size (bytes)", "f2"),
    ("Bwd Packet Length Mean", "Mean backward packet size (bytes)", "f2"),
    ("SYN Flag Count", "SYN flags", "int"),
    ("ACK Flag Count", "ACK flags", "int"),
    ("PSH Flag Count", "PSH flags", "int"),
    ("RST Flag Count", "RST flags", "int"),
    ("FIN Flag Count", "FIN flags", "int"),
    ("Init_Win_bytes_forward", "Initial TCP window forward (bytes)", "int"),
    ("Init_Win_bytes_backward", "Initial TCP window backward (bytes)", "int"),
]
CARD_COLUMNS = [c for c, _, _ in CARD_FIELDS]


def _fmt(v, kind: str) -> str:
    if v is None or (isinstance(v, float) and (math.isnan(v) or math.isinf(v))):
        return "n/a"
    return str(int(round(v))) if kind == "int" else f"{v:.2f}"


def flow_observations(row) -> dict:
    """Readable name -> formatted value (what the card shows)."""
    return {label: _fmt(row[col], kind) for col, label, kind in CARD_FIELDS}


def build_card(alert_id: str, row, proba: dict) -> str:
    pred = max(proba, key=proba.get)
    scores = ", ".join(f"{c} {proba[c]:.2f}" for c in CLASSES)
    lines = [
        f"Alert {alert_id}",
        f"IDS prediction (model output, not confirmed): {pred}",
        f"IDS class scores: {scores}",
        "Flow observations:",
    ]
    lines += [f"- {k}: {v}" for k, v in flow_observations(row).items()]
    return "\n".join(lines)
