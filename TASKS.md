# Zadania

## 1. Przygotować dane CIC-IDS2017 i uruchomić bazowy Random Forest dla trzech klas — GOTOWE

Kod: `scripts/01…04`, `src/socalert/`. Raporty: `reports/`. Jak uruchomić: [README.md](README.md).

- [x] Pobrane CSV, trzy klasy: BENIGN 2 273 097 · DoS Hulk 231 073 · FTP-Patator 7 938 ([reports/01_data_report.md](reports/01_data_report.md)).
- [x] Braki / Inf / duplikaty zbadane i obsłużone (NaN w `Flow Bytes/s`, Inf w `Flow Bytes/s` i `Flow Packets/s`; po dedup Hulk 172 719, FTP-Patator 5 933, BENIGN 2 096 354).
- [x] Podział grupowy, stratyfikowany po klasach, 60/20/20; brak wspólnych grup i wektorów cech między częściami ([reports/02_split_report.md](reports/02_split_report.md)).
- [x] Dobór cech tylko na treningu (78 → 30).
- [x] Random Forest: macierz pomyłek, precision, recall ([reports/03_rf_report.md](reports/03_rf_report.md)).
- [x] Alerty i karty alertów dla val i test, w tym próbka kart z fałszywymi alarmami ([reports/04_alert_cards_sample.md](reports/04_alert_cards_sample.md)).

Wynik na teście (454 969 przepływów):

| klasa | precision | recall |
|---|---:|---:|
| DoS Hulk | 0.9995 | 0.9987 |
| FTP-Patator | 1.0000 | 0.9992 |

IDS wygenerował 35 670 alertów: 35 652 prawdziwe, **18 fałszywych alarmów** (BENIGN uznany za DoS Hulk), 45 ataków przeoczonych (nie stają się alertem). Walidacja: 36 131 alertów, 19 fałszywych.

### Co wynika dla etapu z Llamą

1. **Fałszywych alarmów jest mało** (18 test + 19 val). Odsetek odrzuconych FA z Llamy będzie miał szeroki przedział niepewności. Trzeba zebrać więcej: alerty z walidacji, out-of-fold na treningu (i tak potrzebne, patrz niżej), ewentualnie słabszy IDS.
2. **Jest prosta linia odniesienia do pobicia**: odrzucanie alertów, w których sam IDS jest niepewny. Na teście próg `confidence < 0.7` odrzuca 15/18 FA i traci 59 z 35 652 prawdziwych alertów (reszta progów w `reports/04_alert_cards_summary.json`). Llama ma sens, jeśli wypada lepiej niż to, albo coś dodaje (opis).
3. Wszystkie FA to przepływy na porcie 80 o niskiej pewności (0.51–0.92); 13 z 18 bez żadnych bajtów w obu kierunkach, 11 trwa poniżej 1 ms. Same karty ich nie odróżnią, jeśli karta nie zawiera cech, które IDS widział (w karcie jest 17 pól; RF używa 30).
4. Różnica między wariantami RF na walidacji (macro-F1 0.99765 / 0.99766 / 0.99768) to szum; wybór `rf_leaf5` jest arbitralny.
5. Usunięcie `Destination Port` pogarsza wynik tylko trochę (test macro-F1 0.9987 vs 0.9995), więc port nie jest jedynym skrótem.

## 2. Sprawdzić PyTorch + RX 9070 XT i uruchomić Llama 3.2 1B Instruct na karcie — DO ZROBIENIA

Wykonuje osoba z RX 9070 XT (nie ta maszyna: tu macOS, brak tej karty).

- [ ] `torch.cuda.is_available()` / ROCm, wersja PyTorch, `torch.version.hip`.
- [ ] Llama-3.2-1B-Instruct ładuje się na GPU, generuje krótki tekst, zapisany czas i zajęta pamięć.
- [ ] Dostęp do modelu (licencja Meta na HF) potwierdzony.

## 3. IDS out-of-fold dla zbioru treningowego — DO ZROBIENIA

Do trenowania głowicy Llamy wynik IDS na treningu musi pochodzić z modelu niewidzącego tych przepływów ([PROJECT_OVERVIEW.md](.github/PROJECT_OVERVIEW.md), punkt 5).

- [ ] Grupowy K-fold po kolumnie `group` na `train.parquet`, `IDSModel.fit` osobno w każdym foldzie (selekcja cech też).
- [ ] Alerty OOF i karty dla treningu, z tym samym `build_card`.
- [ ] Zdecydować o próbkowaniu BENIGN/Hulk do budżetu kilka–kilkadziesiąt tysięcy kart, z zachowaniem wszystkich fałszywych alarmów.

## 4. Zamrożona Llama + trening samej głowicy — DO ZROBIENIA (po 2 i 3)

- [ ] Reprezentacja ostatniego nieuzupełniającego tokenu, spójny padding.
- [ ] Zapis i ponowne wczytanie głowicy zweryfikowane.

## 5. Porównanie: ile FA Llama odrzuca, ile prawdziwych ataków przy tym przeocza — DO ZROBIENIA (po 4)

- [ ] Metryki na `alerts_test.jsonl`, razem z linią odniesienia „próg pewności IDS”.
- [ ] Wyniki osobno dla DoS Hulk i FTP-Patator.
