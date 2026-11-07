# Alert card samples (test split)

Test alerts: 35,670 · outcomes {'true_alert': 35652, 'false_alarm': 18}.
Cards below are the exact LLM input text. The `Reference` line is evaluation-only and is not part of the card.

## False alarms (18: real BENIGN flagged by IDS)

```text
IDS prediction (model output, not confirmed): DoS Hulk
IDS class scores: BENIGN 0.45, DoS Hulk 0.55, FTP-Patator 0.00
Flow observations:
- Destination port: 80
- Flow duration (microseconds): 138
- Forward packets: 2
- Backward packets: 0
- Forward bytes: 0
- Backward bytes: 0
- Flow bytes per second: 0.00
- Flow packets per second: 14492.75
- Mean forward packet size (bytes): 0.00
- Mean backward packet size (bytes): 0.00
- SYN flags: 0
- ACK flags: 1
- PSH flags: 0
- RST flags: 0
- FIN flags: 0
- Initial TCP window forward (bytes): 274
- Initial TCP window backward (bytes): -1
```
Reference: {'label': 'BENIGN', 'outcome': 'false_alarm'}

```text
IDS prediction (model output, not confirmed): DoS Hulk
IDS class scores: BENIGN 0.36, DoS Hulk 0.64, FTP-Patator 0.00
Flow observations:
- Destination port: 80
- Flow duration (microseconds): 1039
- Forward packets: 2
- Backward packets: 0
- Forward bytes: 0
- Backward bytes: 0
- Flow bytes per second: 0.00
- Flow packets per second: 1924.93
- Mean forward packet size (bytes): 0.00
- Mean backward packet size (bytes): 0.00
- SYN flags: 0
- ACK flags: 1
- PSH flags: 0
- RST flags: 0
- FIN flags: 0
- Initial TCP window forward (bytes): 264
- Initial TCP window backward (bytes): -1
```
Reference: {'label': 'BENIGN', 'outcome': 'false_alarm'}

```text
IDS prediction (model output, not confirmed): DoS Hulk
IDS class scores: BENIGN 0.40, DoS Hulk 0.60, FTP-Patator 0.00
Flow observations:
- Destination port: 80
- Flow duration (microseconds): 623
- Forward packets: 2
- Backward packets: 0
- Forward bytes: 0
- Backward bytes: 0
- Flow bytes per second: 0.00
- Flow packets per second: 3210.27
- Mean forward packet size (bytes): 0.00
- Mean backward packet size (bytes): 0.00
- SYN flags: 0
- ACK flags: 1
- PSH flags: 0
- RST flags: 0
- FIN flags: 0
- Initial TCP window forward (bytes): 274
- Initial TCP window backward (bytes): -1
```
Reference: {'label': 'BENIGN', 'outcome': 'false_alarm'}

```text
IDS prediction (model output, not confirmed): DoS Hulk
IDS class scores: BENIGN 0.39, DoS Hulk 0.61, FTP-Patator 0.00
Flow observations:
- Destination port: 80
- Flow duration (microseconds): 315
- Forward packets: 2
- Backward packets: 0
- Forward bytes: 0
- Backward bytes: 0
- Flow bytes per second: 0.00
- Flow packets per second: 6349.21
- Mean forward packet size (bytes): 0.00
- Mean backward packet size (bytes): 0.00
- SYN flags: 0
- ACK flags: 1
- PSH flags: 0
- RST flags: 0
- FIN flags: 0
- Initial TCP window forward (bytes): 274
- Initial TCP window backward (bytes): -1
```
Reference: {'label': 'BENIGN', 'outcome': 'false_alarm'}

```text
IDS prediction (model output, not confirmed): DoS Hulk
IDS class scores: BENIGN 0.17, DoS Hulk 0.83, FTP-Patator 0.00
Flow observations:
- Destination port: 80
- Flow duration (microseconds): 147
- Forward packets: 3
- Backward packets: 0
- Forward bytes: 0
- Backward bytes: 0
- Flow bytes per second: 0.00
- Flow packets per second: 20408.16
- Mean forward packet size (bytes): 0.00
- Mean backward packet size (bytes): 0.00
- SYN flags: 0
- ACK flags: 1
- PSH flags: 0
- RST flags: 0
- FIN flags: 0
- Initial TCP window forward (bytes): 251
- Initial TCP window backward (bytes): -1
```
Reference: {'label': 'BENIGN', 'outcome': 'false_alarm'}

```text
IDS prediction (model output, not confirmed): DoS Hulk
IDS class scores: BENIGN 0.31, DoS Hulk 0.69, FTP-Patator 0.00
Flow observations:
- Destination port: 80
- Flow duration (microseconds): 266
- Forward packets: 2
- Backward packets: 0
- Forward bytes: 0
- Backward bytes: 0
- Flow bytes per second: 0.00
- Flow packets per second: 7518.80
- Mean forward packet size (bytes): 0.00
- Mean backward packet size (bytes): 0.00
- SYN flags: 0
- ACK flags: 1
- PSH flags: 0
- RST flags: 0
- FIN flags: 0
- Initial TCP window forward (bytes): 274
- Initial TCP window backward (bytes): -1
```
Reference: {'label': 'BENIGN', 'outcome': 'false_alarm'}

```text
IDS prediction (model output, not confirmed): DoS Hulk
IDS class scores: BENIGN 0.46, DoS Hulk 0.54, FTP-Patator 0.00
Flow observations:
- Destination port: 80
- Flow duration (microseconds): 95268
- Forward packets: 2
- Backward packets: 1
- Forward bytes: 12
- Backward bytes: 0
- Flow bytes per second: 125.96
- Flow packets per second: 31.49
- Mean forward packet size (bytes): 6.00
- Mean backward packet size (bytes): 0.00
- SYN flags: 0
- ACK flags: 0
- PSH flags: 0
- RST flags: 0
- FIN flags: 1
- Initial TCP window forward (bytes): 0
- Initial TCP window backward (bytes): 235
```
Reference: {'label': 'BENIGN', 'outcome': 'false_alarm'}

```text
IDS prediction (model output, not confirmed): DoS Hulk
IDS class scores: BENIGN 0.40, DoS Hulk 0.60, FTP-Patator 0.00
Flow observations:
- Destination port: 80
- Flow duration (microseconds): 80
- Forward packets: 2
- Backward packets: 0
- Forward bytes: 0
- Backward bytes: 0
- Flow bytes per second: 0.00
- Flow packets per second: 25000.00
- Mean forward packet size (bytes): 0.00
- Mean backward packet size (bytes): 0.00
- SYN flags: 0
- ACK flags: 1
- PSH flags: 0
- RST flags: 0
- FIN flags: 0
- Initial TCP window forward (bytes): 274
- Initial TCP window backward (bytes): -1
```
Reference: {'label': 'BENIGN', 'outcome': 'false_alarm'}

```text
IDS prediction (model output, not confirmed): DoS Hulk
IDS class scores: BENIGN 0.08, DoS Hulk 0.92, FTP-Patator 0.00
Flow observations:
- Destination port: 80
- Flow duration (microseconds): 1003
- Forward packets: 3
- Backward packets: 0
- Forward bytes: 0
- Backward bytes: 0
- Flow bytes per second: 0.00
- Flow packets per second: 2991.03
- Mean forward packet size (bytes): 0.00
- Mean backward packet size (bytes): 0.00
- SYN flags: 0
- ACK flags: 1
- PSH flags: 0
- RST flags: 0
- FIN flags: 0
- Initial TCP window forward (bytes): 274
- Initial TCP window backward (bytes): -1
```
Reference: {'label': 'BENIGN', 'outcome': 'false_alarm'}

```text
IDS prediction (model output, not confirmed): DoS Hulk
IDS class scores: BENIGN 0.46, DoS Hulk 0.54, FTP-Patator 0.00
Flow observations:
- Destination port: 80
- Flow duration (microseconds): 280
- Forward packets: 2
- Backward packets: 0
- Forward bytes: 0
- Backward bytes: 0
- Flow bytes per second: 0.00
- Flow packets per second: 7142.86
- Mean forward packet size (bytes): 0.00
- Mean backward packet size (bytes): 0.00
- SYN flags: 0
- ACK flags: 1
- PSH flags: 0
- RST flags: 0
- FIN flags: 0
- Initial TCP window forward (bytes): 264
- Initial TCP window backward (bytes): -1
```
Reference: {'label': 'BENIGN', 'outcome': 'false_alarm'}

```text
IDS prediction (model output, not confirmed): DoS Hulk
IDS class scores: BENIGN 0.47, DoS Hulk 0.53, FTP-Patator 0.00
Flow observations:
- Destination port: 80
- Flow duration (microseconds): 459
- Forward packets: 2
- Backward packets: 0
- Forward bytes: 0
- Backward bytes: 0
- Flow bytes per second: 0.00
- Flow packets per second: 4357.30
- Mean forward packet size (bytes): 0.00
- Mean backward packet size (bytes): 0.00
- SYN flags: 0
- ACK flags: 1
- PSH flags: 0
- RST flags: 0
- FIN flags: 0
- Initial TCP window forward (bytes): 274
- Initial TCP window backward (bytes): -1
```
Reference: {'label': 'BENIGN', 'outcome': 'false_alarm'}

```text
IDS prediction (model output, not confirmed): DoS Hulk
IDS class scores: BENIGN 0.48, DoS Hulk 0.52, FTP-Patator 0.00
Flow observations:
- Destination port: 80
- Flow duration (microseconds): 289
- Forward packets: 2
- Backward packets: 0
- Forward bytes: 0
- Backward bytes: 0
- Flow bytes per second: 0.00
- Flow packets per second: 6920.42
- Mean forward packet size (bytes): 0.00
- Mean backward packet size (bytes): 0.00
- SYN flags: 0
- ACK flags: 1
- PSH flags: 0
- RST flags: 0
- FIN flags: 0
- Initial TCP window forward (bytes): 264
- Initial TCP window backward (bytes): -1
```
Reference: {'label': 'BENIGN', 'outcome': 'false_alarm'}

```text
IDS prediction (model output, not confirmed): DoS Hulk
IDS class scores: BENIGN 0.39, DoS Hulk 0.61, FTP-Patator 0.00
Flow observations:
- Destination port: 80
- Flow duration (microseconds): 117346
- Forward packets: 3
- Backward packets: 2
- Forward bytes: 421
- Backward bytes: 5817
- Flow bytes per second: 53159.03
- Flow packets per second: 42.61
- Mean forward packet size (bytes): 140.33
- Mean backward packet size (bytes): 2908.50
- SYN flags: 0
- ACK flags: 0
- PSH flags: 1
- RST flags: 0
- FIN flags: 0
- Initial TCP window forward (bytes): 29200
- Initial TCP window backward (bytes): 123
```
Reference: {'label': 'BENIGN', 'outcome': 'false_alarm'}

```text
IDS prediction (model output, not confirmed): DoS Hulk
IDS class scores: BENIGN 0.49, DoS Hulk 0.51, FTP-Patator 0.00
Flow observations:
- Destination port: 80
- Flow duration (microseconds): 227334
- Forward packets: 9
- Backward packets: 5
- Forward bytes: 413
- Backward bytes: 10795
- Flow bytes per second: 49301.91
- Flow packets per second: 61.58
- Mean forward packet size (bytes): 45.89
- Mean backward packet size (bytes): 2159.00
- SYN flags: 0
- ACK flags: 0
- PSH flags: 1
- RST flags: 0
- FIN flags: 0
- Initial TCP window forward (bytes): 65535
- Initial TCP window backward (bytes): 15544
```
Reference: {'label': 'BENIGN', 'outcome': 'false_alarm'}

```text
IDS prediction (model output, not confirmed): DoS Hulk
IDS class scores: BENIGN 0.45, DoS Hulk 0.55, FTP-Patator 0.00
Flow observations:
- Destination port: 80
- Flow duration (microseconds): 227310
- Forward packets: 10
- Backward packets: 4
- Forward bytes: 407
- Backward bytes: 9755
- Flow bytes per second: 44705.47
- Flow packets per second: 61.59
- Mean forward packet size (bytes): 40.70
- Mean backward packet size (bytes): 2438.75
- SYN flags: 0
- ACK flags: 0
- PSH flags: 1
- RST flags: 0
- FIN flags: 0
- Initial TCP window forward (bytes): 65535
- Initial TCP window backward (bytes): 15544
```
Reference: {'label': 'BENIGN', 'outcome': 'false_alarm'}

```text
IDS prediction (model output, not confirmed): DoS Hulk
IDS class scores: BENIGN 0.44, DoS Hulk 0.56, FTP-Patator 0.00
Flow observations:
- Destination port: 80
- Flow duration (microseconds): 387604
- Forward packets: 9
- Backward packets: 8
- Forward bytes: 991
- Backward bytes: 12438
- Flow bytes per second: 34646.19
- Flow packets per second: 43.86
- Mean forward packet size (bytes): 110.11
- Mean backward packet size (bytes): 1554.75
- SYN flags: 0
- ACK flags: 0
- PSH flags: 1
- RST flags: 0
- FIN flags: 0
- Initial TCP window forward (bytes): 29200
- Initial TCP window backward (bytes): 1006
```
Reference: {'label': 'BENIGN', 'outcome': 'false_alarm'}

```text
IDS prediction (model output, not confirmed): DoS Hulk
IDS class scores: BENIGN 0.20, DoS Hulk 0.80, FTP-Patator 0.00
Flow observations:
- Destination port: 80
- Flow duration (microseconds): 86
- Forward packets: 3
- Backward packets: 0
- Forward bytes: 0
- Backward bytes: 0
- Flow bytes per second: 0.00
- Flow packets per second: 34883.72
- Mean forward packet size (bytes): 0.00
- Mean backward packet size (bytes): 0.00
- SYN flags: 0
- ACK flags: 1
- PSH flags: 0
- RST flags: 0
- FIN flags: 0
- Initial TCP window forward (bytes): 251
- Initial TCP window backward (bytes): -1
```
Reference: {'label': 'BENIGN', 'outcome': 'false_alarm'}

```text
IDS prediction (model output, not confirmed): DoS Hulk
IDS class scores: BENIGN 0.47, DoS Hulk 0.53, FTP-Patator 0.00
Flow observations:
- Destination port: 80
- Flow duration (microseconds): 344
- Forward packets: 2
- Backward packets: 0
- Forward bytes: 0
- Backward bytes: 0
- Flow bytes per second: 0.00
- Flow packets per second: 5813.95
- Mean forward packet size (bytes): 0.00
- Mean backward packet size (bytes): 0.00
- SYN flags: 0
- ACK flags: 1
- PSH flags: 0
- RST flags: 0
- FIN flags: 0
- Initial TCP window forward (bytes): 274
- Initial TCP window backward (bytes): -1
```
Reference: {'label': 'BENIGN', 'outcome': 'false_alarm'}

## True alerts (random sample, up to 3 per attack)

```text
IDS prediction (model output, not confirmed): DoS Hulk
IDS class scores: BENIGN 0.00, DoS Hulk 1.00, FTP-Patator 0.00
Flow observations:
- Destination port: 80
- Flow duration (microseconds): 86176974
- Forward packets: 6
- Backward packets: 6
- Forward bytes: 344
- Backward bytes: 11595
- Flow bytes per second: 138.54
- Flow packets per second: 0.14
- Mean forward packet size (bytes): 57.33
- Mean backward packet size (bytes): 1932.50
- SYN flags: 0
- ACK flags: 0
- PSH flags: 0
- RST flags: 0
- FIN flags: 1
- Initial TCP window forward (bytes): 0
- Initial TCP window backward (bytes): 235
```
Reference: {'label': 'DoS Hulk', 'outcome': 'true_alert'}

```text
IDS prediction (model output, not confirmed): DoS Hulk
IDS class scores: BENIGN 0.00, DoS Hulk 1.00, FTP-Patator 0.00
Flow observations:
- Destination port: 80
- Flow duration (microseconds): 83348124
- Forward packets: 7
- Backward packets: 6
- Forward bytes: 348
- Backward bytes: 11595
- Flow bytes per second: 143.29
- Flow packets per second: 0.16
- Mean forward packet size (bytes): 49.71
- Mean backward packet size (bytes): 1932.50
- SYN flags: 0
- ACK flags: 1
- PSH flags: 0
- RST flags: 0
- FIN flags: 0
- Initial TCP window forward (bytes): 274
- Initial TCP window backward (bytes): 235
```
Reference: {'label': 'DoS Hulk', 'outcome': 'true_alert'}

```text
IDS prediction (model output, not confirmed): DoS Hulk
IDS class scores: BENIGN 0.00, DoS Hulk 1.00, FTP-Patator 0.00
Flow observations:
- Destination port: 80
- Flow duration (microseconds): 98451900
- Forward packets: 7
- Backward packets: 7
- Forward bytes: 310
- Backward bytes: 11595
- Flow bytes per second: 120.92
- Flow packets per second: 0.14
- Mean forward packet size (bytes): 44.29
- Mean backward packet size (bytes): 1656.43
- SYN flags: 0
- ACK flags: 1
- PSH flags: 0
- RST flags: 0
- FIN flags: 0
- Initial TCP window forward (bytes): 274
- Initial TCP window backward (bytes): 235
```
Reference: {'label': 'DoS Hulk', 'outcome': 'true_alert'}

```text
IDS prediction (model output, not confirmed): FTP-Patator
IDS class scores: BENIGN 0.00, DoS Hulk 0.00, FTP-Patator 1.00
Flow observations:
- Destination port: 21
- Flow duration (microseconds): 8198750
- Forward packets: 9
- Backward packets: 15
- Forward bytes: 101
- Backward bytes: 188
- Flow bytes per second: 35.25
- Flow packets per second: 2.93
- Mean forward packet size (bytes): 11.22
- Mean backward packet size (bytes): 12.53
- SYN flags: 0
- ACK flags: 0
- PSH flags: 1
- RST flags: 0
- FIN flags: 0
- Initial TCP window forward (bytes): 29200
- Initial TCP window backward (bytes): 227
```
Reference: {'label': 'FTP-Patator', 'outcome': 'true_alert'}

```text
IDS prediction (model output, not confirmed): FTP-Patator
IDS class scores: BENIGN 0.00, DoS Hulk 0.00, FTP-Patator 1.00
Flow observations:
- Destination port: 21
- Flow duration (microseconds): 250
- Forward packets: 2
- Backward packets: 1
- Forward bytes: 14
- Backward bytes: 0
- Flow bytes per second: 56000.00
- Flow packets per second: 12000.00
- Mean forward packet size (bytes): 7.00
- Mean backward packet size (bytes): 0.00
- SYN flags: 1
- ACK flags: 1
- PSH flags: 0
- RST flags: 0
- FIN flags: 0
- Initial TCP window forward (bytes): 229
- Initial TCP window backward (bytes): 0
```
Reference: {'label': 'FTP-Patator', 'outcome': 'true_alert'}

```text
IDS prediction (model output, not confirmed): FTP-Patator
IDS class scores: BENIGN 0.00, DoS Hulk 0.00, FTP-Patator 1.00
Flow observations:
- Destination port: 21
- Flow duration (microseconds): 10176966
- Forward packets: 9
- Backward packets: 15
- Forward bytes: 100
- Backward bytes: 188
- Flow bytes per second: 28.30
- Flow packets per second: 2.36
- Mean forward packet size (bytes): 11.11
- Mean backward packet size (bytes): 12.53
- SYN flags: 0
- ACK flags: 0
- PSH flags: 1
- RST flags: 0
- FIN flags: 0
- Initial TCP window forward (bytes): 29200
- Initial TCP window backward (bytes): 227
```
Reference: {'label': 'FTP-Patator', 'outcome': 'true_alert'}
