# Split report

Group = 2000 consecutive rows of one day file. StratifiedGroupKFold(5), seed 42: folds (0, 1, 2) train, (3,) val, (4,) test.

## Cleaning steps (rows per class)

| step | BENIGN | DoS Hulk | FTP-Patator |
|---|---:|---:|---:|
| raw | 2,273,097 | 231,073 | 7,938 |
| after_exact_dedup | 2,096,484 | 172,849 | 5,933 |
| after_conflict_drop | 2,096,354 | 172,719 | 5,933 |

## Splits

| split | rows | groups | BENIGN | DoS Hulk | FTP-Patator |
|---|---:|---:|---:|---:|---:|
| train | 1,364,600 | 825 | 1,257,814 (60.0% of class) | 103,317 (59.8% of class) | 3,469 (58.5% of class) |
| val | 455,437 | 274 | 419,268 (20.0% of class) | 34,992 (20.3% of class) | 1,177 (19.8% of class) |
| test | 454,969 | 275 | 419,272 (20.0% of class) | 34,410 (19.9% of class) | 1,287 (21.7% of class) |

Checks: group overlap between splits = 0; identical feature vectors across splits = {'train&val': 0, 'train&test': 0, 'val&test': 0}.
