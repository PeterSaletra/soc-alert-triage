# Data report: CIC-IDS2017 (MachineLearningCVE), three classes

Source: HF mirror `c01dsnap/CIC-IDS2017` (original CSVs; official UNB link is dead).

## Class counts (all 8 day files)

| class | rows | exact dup rows | rows after dedup | NaN rows | Inf rows | in conflict* |
|---|---:|---:|---:|---:|---:|---:|
| BENIGN | 2,273,097 | 176,613 | 2,096,484 | 409 | 1,777 | 130 |
| DoS Hulk | 231,073 | 58,224 | 172,849 | 949 | 949 | 130 |
| FTP-Patator | 7,938 | 2,005 | 5,933 | 0 | 3 | 0 |

*conflict = same feature vector appears under more than one label (unique rows).

Total rows 2,512,108; features 77.
NaN columns: {'Flow Bytes/s': 1358}
Inf columns: {'Flow Bytes/s': 1371, 'Flow Packets/s': 2729}

## Original label counts (all 15 labels, before filtering)

| label | rows |
|---|---:|
| BENIGN | 2,273,097 |
| DoS Hulk | 231,073 |
| PortScan | 158,930 |
| DDoS | 128,027 |
| DoS GoldenEye | 10,293 |
| FTP-Patator | 7,938 |
| SSH-Patator | 5,897 |
| DoS slowloris | 5,796 |
| DoS Slowhttptest | 5,499 |
| Bot | 1,966 |
| Web Attack ï¿½ Brute Force | 1,507 |
| Web Attack ï¿½ XSS | 652 |
| Infiltration | 36 |
| Web Attack ï¿½ Sql Injection | 21 |
| Heartbleed | 11 |
