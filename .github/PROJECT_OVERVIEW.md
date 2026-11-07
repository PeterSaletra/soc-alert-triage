# Brief projektu: adaptacja Llamy do decyzji SOC

## 1. Proponowany temat i decyzja projektowa

**Opis i priorytetyzacja alertów IDS z wykorzystaniem Llamy dostrojonej do klasyfikacji.**

Projekt wykorzysta gotową Llamę z nową głowicą klasyfikacyjną, uczoną na etykietowanych danych. Obok trybu decyzyjnego zachowany będzie tryb generowania krótkich opisów alertów. Jest to wyspecjalizowany model decyzji do ustalonego zadania, a nie odtworzenie ogólnego modelu Jev.

Rekomendowany zakres to scenariusz rozszerzony tematu 14 „LLM w SOC”. Pełna korelacja źródeł, pamięć incydentów i strumieniowy SOC pozostają poza projektem; rozwinięcie zapisano osobno jako koncepcję magisterki.

## 2. Co dokładnie powstanie

```text
Rekord przepływu sieciowego
        |
        v
Przygotowanie cech
        |
        v
Klasyczny IDS (np. Random Forest) -> przewidywany alert
                                         |
                                         v
                     Alert z obserwacjami i wynikiem IDS
                              /                 \
                             v                   v
                  Llama + głowica klasy      Reguły odniesienia
                             |
                             v
                Ocena alertu i jawna polityka priorytetu
                             |
                             v
                 Llama w trybie generatywnym: opis
```

Tryb decyzyjny: tokenizacja alertu, przetworzenie przez transformer Llamy, pobranie reprezentacji ostatniego nieuzupełniającego tokenu i klasyfikacja przez nową głowicę. Dobór reprezentacji i obsługa paddingu muszą być spójne między treningiem i predykcją.

Tryb opisowy: oryginalna głowica generująca tekst i krótka instrukcja opisania wyłącznie dostarczonych dowodów. Nie wymaga osobnego treningu generacji w pierwszej wersji.

Adapter używany do klasyfikacji powinien być odłączany przy generowaniu opisów albo mieć osobny zapis modelu. Dostrojenie reprezentacji wyłącznie do klasyfikacji nie gwarantuje zachowania jakości generowania. Dwa tryby mogą korzystać z tych samych wag bazowych, ale ich poprawne współdzielenie jest elementem implementacji, nie automatyczną własnością dwóch głowic.

## 3. Model bazowy i trening

### Rekomendacja

Zacząć od **Llama-3.2-1B-Instruct**. Jeżeli sprzęt i wyniki uzasadnią większy model, rozważyć 3B. Llama 3.2 należy do rodziny Llama 3; nie ma konieczności zaczynania od pierwotnej Llamy 3 8B. Warianty 1B i 3B są oficjalnie dostępne. Język kart alertów i opisów najlepiej początkowo ujednolicić do angielskiego.

Wariant 8B jest możliwy, ale zwiększa koszt i ryzyko organizacyjne. Bez znajomości GPU nie należy deklarować czasu treningu ani gwarantować, że określona konfiguracja zmieści się w pamięci. Znaczenie mają także długość wejścia, batch size, optymalizator i sposób kwantyzacji.

### Etapy treningu

1. Uruchomić niewielką próbkę i sprawdzić cały potok na rzeczywistym sprzęcie.
2. Zamrozić bazę i nauczyć głowicę klasyfikacyjną, używając etykiet ze zbioru.
3. Jeśli jakość jest niewystarczająca, dostroić adaptery LoRA wraz z głowicą. Zapewnić, że nowa głowica rzeczywiście jest trenowana i zapisywana.
4. Wybrać konfigurację na walidacji; końcowy test wykonać po zamrożeniu decyzji projektowych.

Przy zamrożonej bazie można jednorazowo zapisać reprezentacje wejść i szybko trenować samą głowicę. Po zmianie wag bazy lub adapterów reprezentacje wymagają ponownego obliczenia.

Dotrenowanie ma poprawić trafność. Zysk szybkości pochodzi przede wszystkim z braku sekwencyjnego generowania odpowiedzi w trybie decyzyjnym, a nie z samego treningu. Większość wag Llamy pozostaje w modelu.

## 4. Dane: co wybrać

### Wybór główny: CIC-IDS2017

**Najlepszy wybór dla tego projektu z punktu widzenia zgodności z dokumentami i ograniczenia prac.** Zbiór ma etykietowane przepływy, gotowe CSV i wymienione w wymaganiach rodzaje ataków.

Wybrać trzy klasy:

- `BENIGN`;
- `DoS Hulk`;
- `FTP-Patator` — scenariusz Brute Force FTP.

Wykorzystanie:

- klasyczny IDS uczy się na cechach numerycznych;
- Llama otrzymuje te same obserwacje zapisane jako krótka karta alertu;
- głowica Llamy uczy się rozpoznawać klasę zdarzenia;
- generator tworzy opis na podstawie obserwacji i jawnie oznaczonych przewidywań.

Nie należy przesyłać całego CSV jako tekstu. Użyć wybranego zestawu cech, nazw pól i stabilnego formatu. Nie dodawać etykiety referencyjnej do wejścia. Wynik IDS jest przewidywaniem, nie potwierdzonym faktem.

Przykładowa karta obejmuje dostępne cechy: czas trwania przepływu, port docelowy, liczbę pakietów, liczbę bajtów i tempo transmisji. Nie dopisywać nieudanych logowań ani uruchomionych procesów, jeśli nie są obserwowane w danych. Zawartość pól zależy od wybranego wydania zbioru; nie zakładać obecności adresów i znaczników czasu w każdym CSV.

Przygotować rozsądny podzbiór zamiast od razu trenować Llamę na całym zbiorze. Roboczy budżet to kilka–kilkadziesiąt tysięcy rekordów treningowych, po pilotażu i kontroli duplikatów. Nie jest to gwarancja wystarczającej liczby przykładów. Test powinien zachować udokumentowane proporcje klas; wyniki należy raportować oddzielnie dla obu ataków.

**Ograniczenie:** CIC-IDS2017 nie dostarcza automatycznie wiarygodnych etykiet biznesowego priorytetu alertów. Jest też zbiorem tabelarycznym, więc nie zakładamy, że Llama pokona model drzewiasty.

### AIT-ADS: alternatywa dla bardziej naturalnych alertów

Zawiera alerty różnych detektorów i scenariusze ataków. Lepiej odpowiada zadaniu opisu alertu niż sam zapis cech przepływu. Wymaga jednak większej pracy nad przygotowaniem danych i sprawdzeniem etykiet. Dokumentacja rozróżnia etykiety oparte na czasie oraz konkretnych zdarzeniach.

Wybrać zamiast CIC, jeśli priorytetem zespołu są treści rzeczywistych formatów alertów i prowadzący zaakceptuje odpowiadające im dwa scenariusze ataku. Nie łączyć obu zbiorów w pierwszej wersji projektu.

### Microsoft GUIDE: zostawić na rozszerzenie lub magisterkę

Duży zbiór dotyczący triage, z ocenami analityków. Jest atrakcyjny dla przyszłego projektu decyzyjnego, ale anonimizacja, dominacja cech tabelarycznych i rozróżnienie rekordów dowodowych, alertów i incydentów komplikują przygotowanie. Etykieta triage nie jest równoznaczna z priorytetem.

**Ostateczna rekomendacja:** jeden zbiór CIC-IDS2017, dwa ataki i ruch normalny. AIT-ADS traktować jako zamiennik, a nie dodatkowy obowiązek.

## 5. Co ma oznaczać decyzja i priorytet

Najbardziej wiarygodnym celem treningowym na CIC jest **klasa zdarzenia**, ponieważ istnieje dla niej etykieta referencyjna. Nie należy przedstawiać tej etykiety jako oceny priorytetu analityka.

Minimalny wariant projektu:

1. Głowica zwraca klasę i wyniki dla trzech klas.
2. Jawnie opisana polityka mapuje przewidywaną klasę oraz dostępne obserwacje na priorytet.
3. Wynik opisuje się jako priorytet według przyjętej polityki demonstracyjnej, a nie jako zweryfikowaną ocenę szkody biznesowej.

Jeżeli głowica ma **bezpośrednio przewidywać priorytet**, potrzebne są dodatkowe etykiety: ocena ręczna według spisanych kryteriów albo jawnie wygenerowane etykiety polityki. W drugim przypadku model uczy się odtwarzania polityki. Porównanie go z dokładnie tą samą regułą, która utworzyła etykiety, nie dowodzi przewagi modelu i nie powinno być głównym eksperymentem.

Dlatego jako główne porównanie zaleca się klasyfikację Llamy z głowicą i prostego IDS na wspólnych etykietach zbioru. Priorytet i opis są funkcjami prezentowanego systemu. Taki zapis należy zawrzeć w zgłoszeniu tematu, ponieważ szczegółowa realizacja priorytetyzacji jest interpretacją wymagania.

## 6. Wymagania przedmiotu

Podstawa: `Forma_oceniania_MSIWC.pdf`, temat alternatywny 14. Plik ten jest oznaczony jako dotyczący studiów niestacjonarnych; `Regulamin-zajęć.pdf` jest oznaczony jako dotyczący studiów stacjonarnych. Zgodność formalna zależy od tego, który dokument obowiązuje zespół. Poniższy zakres realizuje szczegółową tabelę z pierwszego dokumentu i wspólne wymagania merytoryczne.

| Wymaganie | Plan realizacji | Ocena |
|---|---|---|
| Temat LLM w SOC: opis i priorytetyzacja | Llama z głowicą decyzyjną, jawna polityka priorytetu i opis generatywny | Zachowane funkcje tematu; sposób priorytetyzacji wymaga ujęcia w zaakceptowanym zakresie |
| Dwa podejścia w scenariuszu rozszerzonym | Klasyczny IDS oraz Llama z głowicą na tym samym zadaniu klasyfikacji | Uzasadniona propozycja realizacji; tabela podaje przykłady, nie ten dokładny wariant |
| Dwa typy ataków | DoS Hulk i Brute Force FTP | Spełnione po uwzględnieniu obu w treningu i ocenie |
| Dwie metody obróbki | Obsługa braków/Inf oraz selekcja cech uczona na treningu | Spełnione po implementacji; samych tokenizacji i podziału danych nie liczymy jako dwóch metod |
| Ocena halucynacji | Ręczna ocena opisów na oddzielnej próbce | Spełnione po wykonaniu i opisaniu protokołu |
| Ocena skuteczności | Precision, recall, macro-F1, macierz pomyłek | Spełnione po wykonaniu testu |
| Testy wydajnościowe | Czas oceny alertu oraz czas tworzenia opisu raportowane osobno | Spełnione po pomiarze |
| Oddanie | Kod/notebook, sprawozdanie ze wskazaniem scenariusza, prezentacja | Do przygotowania |
| Akceptacja tematu alternatywnego | Przedstawienie prowadzącemu konkretnego zakresu | Wymóg organizacyjny z dokumentu, nie gwarancja uzyskania zgody |

Scenariusz rozszerzony ma limit 4.5; dokument przewiduje dodatkowe 0.5 za przedstawianie postępów na każdych zajęciach. Sam pomysł lub użycie bardziej złożonej architektury nie gwarantuje oceny.

Jeżeli prowadzący uzna, że porównanie ma dotyczyć ściśle decyzji SOC, zamiast rozszerzać projekt o wiele modeli należy porównać Llamę z głowicą z oryginalną Llamą zwracającą tę samą klasę w trybie generatywnym. Klasyczny IDS nadal pozostaje źródłem alertów i punktem odniesienia.

## 7. Lista prac

1. **Ustalić zakres i sprzęt:** scenariusz oceniania, obowiązujący dokument, dostępna karta GPU i model 1B/3B.
2. **Przygotować dane:** pobrać wskazane klasy, skontrolować braki, Inf, duplikaty i niezbalansowanie.
3. **Ustalić podział:** oddzielić trening, walidację i test przed uczeniem przekształceń. Nie rozdzielać niemal identycznych przepływów jednej sesji pomiędzy częściami. Jeśli wydanie pozwala, stosować grupowanie sesji/okien czasu. Nie dzielić wyłącznie po dniach, gdy spowodowałoby to brak danego ataku w treningu lub teście.
4. **Wytrenować klasyczny IDS:** przygotować podstawowe metryki i generowanie alertów.
5. **Przygotować karty alertów:** stały format i dane dostępne w chwili oceny. Jeśli zawierają wynik IDS, dla treningu Llamy uzyskać go z predykcji spoza próby treningowej IDS, np. out-of-fold; dla testu z IDS wytrenowanego bez testu.
6. **Zaimplementować głowicę i trening:** najpierw zamrożona baza, następnie opcjonalnie LoRA. Weryfikacja zapisu i ponownego wczytania modelu.
7. **Dodać priorytet i opis:** jawna polityka oraz zachowana oryginalna ścieżka generatywna.
8. **Wykonać ocenę:** jakość obu ataków, czas, analiza błędów i halucynacji.
9. **Przygotować demonstrację i materiały:** przykłady poprawnych oraz błędnych ocen, kod, sprawozdanie i prezentacja.

W ramach sześciu spotkań: wybór i pilotaż; dane i IDS; głowica i trening; opisy i testy; raport; prezentacja. Nie jest to deklaracja liczby godzin — czas zależy przede wszystkim od doświadczenia zespołu i GPU.

## 8. Jak oceniać wynik

- **Decyzje:** macro-F1, precision i recall dla obu ataków, macierz pomyłek; accuracy pomocniczo.
- **Priorytet:** zgodność z jawną polityką; nie utożsamiać tej miary ze skutecznością operacyjną SOC.
- **Opisy:** roboczo 60–100 przypadków łącznie, obejmujących oba ataki, ruch normalny i błędne alarmy IDS. Oddzielić próbkę reprezentatywną od celowo wybranych trudnych przykładów. Ocenić poprawność liczb i pól, nieuprawnione dopowiedzenia oraz czy przewidywanie przedstawiono jako pewny fakt. Opisać dobór próbki i liczbę oceniających.
- **Wydajność:** czas decyzji i generacji osobno, z rozgrzanym modelem, na tym samym sprzęcie, przy jawnej długości wejścia i wyjścia. Wystarczy prosty pomiar; nie budujemy pełnego testu obciążeniowego SOC.

Nie oczekujemy opisu „udowodniono włamanie”, jeśli wejście zawiera tylko statystyki przepływu. Przewidywanie modelu może być błędne i powinno pozostać oznaczone jako przewidywanie.

## 9. Trudność względem innych tematów

Poniższe oceny są orientacyjną oceną implementacji w ograniczonym zakresie, a nie obiektywnym rankingiem tematów.

| Przykładowy projekt | Trudność w skali 1–10 |
|---|---:|
| Klasyczny IDS na gotowym CSV | 3–4 |
| Niezbalansowanie klas albo XAI dla modelu drzewiastego | 4–5 |
| Model klasyczny i autoencoder | 5–6 |
| LLM opisujący alerty bez dostrajania | 5–6 |
| Ten projekt: Llama 1B, głowica, opisy, dwa ataki | 7 |
| Ten projekt z 8B, QLoRA i własnym współdzieleniem dwóch głowic | 8 |
| GNN, federated learning lub pełny strumieniowy IDS | 7–9 zależnie od zakresu |

Największe trudności: poprawny trening głowicy i adapterów, pamięć GPU, rzetelny podział danych, etykiety priorytetu oraz zachowanie jakości opisów. Najłatwiejsze części: prosty IDS, formatowanie kart i prezentacja wyniku.

Ocena: projekt ambitniejszy od klasycznego IDS i zwykłego podłączenia LLM, ale wykonalny po ograniczeniu do 1B, jednego zbioru, dwóch ataków i krótkich wejść. Nie powinien obejmować pełnej korelacji źródeł ani treningu modelu od zera.

## 10. Propozycja opisu dla prowadzącego

Projekt obejmie adaptację modelu Llama do klasyfikacji alertów przez dołączenie i wytrenowanie głowicy decyzyjnej. Wykorzystamy CIC-IDS2017 z ruchem normalnym oraz atakami DoS Hulk i Brute Force FTP. Klasyczny IDS będzie generował alerty, a model oparty na Llamie oceni ich klasę. Priorytet zostanie wyznaczony według jawnie opisanej polityki, natomiast zachowany tryb generatywny Llamy przygotuje krótki opis oparty na danych alertu. Zastosujemy dwie metody obróbki danych, porównamy podejścia klasyczne i językowe na wspólnych etykietach, ocenimy skuteczność oraz czas działania i przeanalizujemy halucynacje w opisach. Projekt realizuje temat „LLM w SOC – opis i priorytetyzacja alertów”; przedstawiony sposób realizacji scenariusza rozszerzonego podlega akceptacji prowadzącego.

## 11. Źródła i dokumenty

Brief opracowano 31 października 2026 r. Dokładny checkpoint i konfigurację należy ustalić po pilotażu.

- Dokument lokalny: `Forma_oceniania_MSIWC.pdf` — szczegółowe wymagania tematu 14 i scenariuszy oceniania.
- Dokument lokalny: `Regulamin-zajęć.pdf` — ogólne wymagania i proponowane tematy; oznaczenie innego trybu studiów.
- [CIC-IDS2017 — oficjalny opis i dane](https://www.unb.ca/cic/datasets/ids-2017.html).
- [AIT-ADS — repozytorium autorów](https://github.com/ait-aecid/alert-data-set).
- [GUIDE — publikacja autorów](https://arxiv.org/abs/2407.09017).
- [Llama 3.2 — dokumentacja Meta](https://dev.meta.ai/llama/docs/model-cards-and-prompt-formats/llama3_2).
- [Oficjalne repozytorium modeli Llama](https://github.com/meta-llama/llama-models).
