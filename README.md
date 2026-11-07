# soc-alert-triage

Triage alertów IDS: klasyczny Random Forest generuje alerty, Llama 3.2 1B Instruct z nową głowicą klasyfikacyjną ocenia, które z nich są prawdziwe. Zakres i uzasadnienia: [.github/PROJECT_OVERVIEW.md](.github/PROJECT_OVERVIEW.md). Lista zadań: [TASKS.md](TASKS.md).

## Dane

CIC-IDS2017, oryginalne CSV (MachineLearningCVE, 8 plików dziennych, 2 830 743 przepływy). Zostają trzy klasy: `BENIGN`, `DoS Hulk`, `FTP-Patator`.

Oficjalny link UNB z bezpośrednim pobraniem już nie działa. Pliki pobrano z mirrora HF `c01dsnap/CIC-IDS2017`; liczebności wszystkich 15 etykiet zgadzają się z opublikowanymi (suma 2 830 743).

```bash
mkdir -p data/raw/cicids2017_ml && cd data/raw/cicids2017_ml
for f in Monday-WorkingHours Tuesday-WorkingHours Wednesday-workingHours \
         Thursday-WorkingHours-Morning-WebAttacks Thursday-WorkingHours-Afternoon-Infilteration \
         Friday-WorkingHours-Morning Friday-WorkingHours-Afternoon-PortScan Friday-WorkingHours-Afternoon-DDos; do
  curl -L --fail -O "https://huggingface.co/datasets/c01dsnap/CIC-IDS2017/resolve/main/$f.pcap_ISCX.csv"
done
```

`data/` i `models/` są w `.gitignore`.

## Uruchomienie

```bash
python3 -m venv .venv && .venv/bin/pip install -e .
.venv/bin/python -I scripts/01_prepare_data.py   # liczebności, NaN, Inf, duplikaty
.venv/bin/python -I scripts/02_split.py          # czyszczenie, dedup, podział grupowy 60/20/20
.venv/bin/python -I scripts/03_train_rf.py       # Random Forest, metryki, predykcje
.venv/bin/python -I scripts/04_alert_cards.py    # alerty i karty alertów (val, test)
```

Raporty z ostatniego uruchomienia: `reports/`. Całość trwa kilka minut (12 rdzeni, 17 GB RAM).

## Decyzje o danych

- Przepływy `±Inf` → `NaN`; braki uzupełniane medianą z treningu (wiersze zostają: 949 przepływów Hulk ma NaN/Inf, usunięcie wycięłoby ich wzorzec).
- Duplikaty (ten sam wektor cech i etykieta) usuwane globalnie przed podziałem: -25% Hulk, -25% FTP-Patator. Wiersze z tym samym wektorem i różnymi etykietami (260) usuwane.
- To wydanie CSV nie ma IP, portu źródłowego ani czasu, więc „bliskie przepływy” przybliża blok 2000 kolejnych wierszy jednego pliku dziennego (pliki są w kolejności przechwycenia). Cały blok trafia do jednej części. Przybliżenie: wiersze na granicy bloków mogą być podobne po obu stronach, a podział nie jest losowy po sesjach.
- Dobór cech (stałe → korelacja |r|>0.98 → top-30 wg ważności RF) i mediany liczone wyłącznie na treningu.
