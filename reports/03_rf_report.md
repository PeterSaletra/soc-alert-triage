# Baseline Random Forest report

## Validation sweep (macro-F1)

| config | params | macro-F1 | fit s |
|---|---|---:|---:|
| rf_default | `{}` | 0.99766 | 42.6 |
| rf_balanced | `{'class_weight': 'balanced_subsample'}` | 0.99765 | 39.3 |
| rf_leaf5 | `{'min_samples_leaf': 5}` | 0.99768 | 42.9 |

Chosen: **rf_leaf5**

## Feature selection (fitted on train)

78 features → constant dropped 8 → correlated (|r|>0.98) dropped 18 → top-30 by RF importance.

Kept: `Bwd Packet Length Std`, `Max Packet Length`, `Bwd Packet Length Mean`, `Destination Port`, `Packet Length Variance`, `Bwd Packet Length Max`, `Flow IAT Max`, `Flow Packets/s`, `Packet Length Mean`, `Flow IAT Mean`, `Fwd Packet Length Max`, `Flow IAT Std`, `Fwd Packet Length Std`, `Fwd IAT Std`, `Fwd IAT Mean`, `Fwd Packet Length Mean`, `Flow Duration`, `Bwd Packets/s`, `Idle Min`, `Fwd Header Length`, `Bwd Header Length`, `Init_Win_bytes_forward`, `FIN Flag Count`, `Total Fwd Packets`, `Init_Win_bytes_backward`, `Bwd IAT Min`, `Bwd IAT Max`, `Min Packet Length`, `Fwd IAT Min`, `Total Length of Fwd Packets`

## Test

| true \ pred | BENIGN | DoS Hulk | FTP-Patator |
|---|---:|---:|---:|
| **BENIGN** | 419,254 | 18 | 0 |
| **DoS Hulk** | 44 | 34,366 | 0 |
| **FTP-Patator** | 1 | 0 | 1,286 |

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| BENIGN | 0.9999 | 1.0000 | 0.9999 | 419,272 |
| DoS Hulk | 0.9995 | 0.9987 | 0.9991 | 34,410 |
| FTP-Patator | 1.0000 | 0.9992 | 0.9996 | 1,287 |

macro-F1 0.9995 · accuracy 0.9999

Alerts (IDS predicted an attack): **35,670** → true 35,652, wrong attack type 0, **false alarms 18** (by predicted class {'DoS Hulk': 18, 'FTP-Patator': 0}); missed attacks (predicted BENIGN) 45.

## Validation

| true \ pred | BENIGN | DoS Hulk | FTP-Patator |
|---|---:|---:|---:|
| **BENIGN** | 419,249 | 19 | 0 |
| **DoS Hulk** | 43 | 34,949 | 0 |
| **FTP-Patator** | 14 | 0 | 1,163 |

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| BENIGN | 0.9999 | 1.0000 | 0.9999 | 419,268 |
| DoS Hulk | 0.9995 | 0.9988 | 0.9991 | 34,992 |
| FTP-Patator | 1.0000 | 0.9881 | 0.9940 | 1,177 |

macro-F1 0.9977 · accuracy 0.9998

Alerts (IDS predicted an attack): **36,131** → true 36,112, wrong attack type 0, **false alarms 19** (by predicted class {'DoS Hulk': 19, 'FTP-Patator': 0}); missed attacks (predicted BENIGN) 57.

## Test, ablation without Destination Port

| true \ pred | BENIGN | DoS Hulk | FTP-Patator |
|---|---:|---:|---:|
| **BENIGN** | 419,239 | 31 | 2 |
| **DoS Hulk** | 92 | 34,318 | 0 |
| **FTP-Patator** | 3 | 0 | 1,284 |

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| BENIGN | 0.9998 | 0.9999 | 0.9998 | 419,272 |
| DoS Hulk | 0.9991 | 0.9973 | 0.9982 | 34,410 |
| FTP-Patator | 0.9984 | 0.9977 | 0.9981 | 1,287 |

macro-F1 0.9987 · accuracy 0.9997

Alerts (IDS predicted an attack): **35,635** → true 35,602, wrong attack type 0, **false alarms 33** (by predicted class {'DoS Hulk': 31, 'FTP-Patator': 2}); missed attacks (predicted BENIGN) 95.
