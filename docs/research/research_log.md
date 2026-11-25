# Rekonstruiertes Research Log

Analyse am **29.10.2026**, Projektstand `f1d64b39f14a404f70ddfb422690a11acfa78f45` plus vorbestehender lokaler Änderung an `run_benchmark.py`.

Dieses Log rekonstruiert Entwicklung und vorhandene Beobachtungen. Es ist kein Protokoll nachträglich ausgeführter Vergleichsexperimente. Die Einordnung der Entscheidungen steht im [Decision Log](decisions.md); die Schreibvorlage im [Methodology Mapping](methodology_mapping.md).

## Quellenumfang und Grenzen

Ausgewertet wurden alle aktuellen versionierten Python-Dateien, das aktuelle EDA-Notebook einschließlich Code, Metadaten und textueller Ausgaben, README, AGENTS.md, Python-/pytest-/VS-Code-Konfiguration, Lockfile, drei vorhandene Testdateien, Git-Status, Hauptentwicklungshistorie und relevante Diffs. Bildausgaben des Notebooks wurden als vorhandene Artefakte inventarisiert; aus ihnen wurden keine neuen quantitativen Ergebnisse abgelesen.

Die erreichbaren Git-Referenzen wurden inventarisiert, einschließlich Cline-Checkpoints. Deren Dateibäume enthalten frühe Entwicklungsstände, unter anderem `models/dataframe.py`; sie sind keine Chattranskripte. Zusätzlich wurden unter `/Users/timomeyer/.cline/data/sessions/` zehn tatsächliche Cline-Nachrichtenarchive vom August 2026 gefunden: alle Nutzereingaben wurden gesichtet, relevante Assistentenantworten zu Import, Typen und Export gelesen. Die historische Qualitätsprüfung und das erste EDA-Notebook wurden zusätzlich aus Git gelesen. Codex-Turn-Diff-Referenzen mit Tree-Objekten sind keine datierten Forschungscommits; sie wurden nicht als eigenständige Experimente ausgelegt. Es wurde kein Remote-Fetch ausgeführt.

Im lokalen Verzeichnis `/Users/timomeyer/.codex/sessions/` waren **39 frühere projektbezogene JSONL-Dateien** von September/Oktober 2026 und die aktuelle Sitzung vorhanden. Alle früheren Dateien wurden nach Metadaten und Nutzernachrichten gesichtet; relevante Assistentenantworten und einzelne weitere historische Inhalte wurden gezielt gelesen. Nicht jede interne Toolausgabe jeder Sitzung wurde vollständig ausgewertet. Sitzungsnamen stammen aus `session_index.jsonl`; maßgeblich sind die datierten Nachrichten, nicht der zuletzt aktualisierte Sitzungstitel. Aussagen früherer Assistenten werden als berichtete Ergebnisse gekennzeichnet, wenn der vollständige damalige Lauf nicht unabhängig rekonstruiert wurde.

Die lokalen Rohdaten wurden inventarisiert. Geprüft wurden alle deutschen Zeilen der acht CSV-Dateien und der beiden Blätter der verwendeten Excel-Datei hinsichtlich Abdeckung/Wertspalten, außerdem der Excel-/CSV-Überlappungsbereich. Die ungenutzte Excel-Datei 2006–2015 wurde auf Workbook-Metadaten und eingebettete Texthinweise untersucht, nicht vollständig fachlich aufbereitet. Silver und Gold wurden vollständig auf die unten genannten Struktureigenschaften geprüft. Es erfolgte kein erneuter Import-/Exportlauf; die aktuelle Bereinigungsfolge wurde nur im Speicher nachvollzogen.

**Nicht verfügbar bzw. nicht ausgewertet:** Ein vollständiger accountweiter ChatGPT-Chatverlauf, nicht lokal gespeicherte Codex-Sitzungen, weitere Cline-Sitzungen außerhalb der zehn gefundenen Archive, Betreuergespräche und weitere externe Projektdiskussionen wurden nicht abgerufen. Ihr Inhalt ist unbekannt. Frühere in Chats erwähnte Dateien wie `modeling/compare_models.py`, `modeling/evaluate_dhr.py`, `modeling/README.md`, `tests/test_data_cleaning.py` und spezielle DHR-/Vergleichstests fehlen heute und wurden in den untersuchten Git-Dateibäumen nicht gefunden. Ihr damaliger Inhalt ist nur soweit belegbar, wie die Sitzungen Auszüge oder Berichte enthalten. Dateien an anderen, nicht benannten Orten wurden nicht pauschal durchsucht.

Das in S38 genannte lokale PDF existiert unter `/Users/timomeyer/Downloads/Hewamalage (2022) Forecast evaluation for data scientists.pdf`. Sein lokaler PDF-Volltext wurde in dieser Analyse nicht extrahiert; für Literaturmetadaten und relevante Abschnitte wurde die frei zugängliche Verlagsfassung geprüft. Eine Bachelorarbeitsfassung, ein Literaturverzeichnis oder ein fertiger Forschungsplan lagen im Repository nicht vor.

## Quellenverzeichnis für die Rekonstruktion

### Vorhandene und überprüfte Literaturbezüge

**L1:** Hewamalage, H., Ackermann, K. und Bergmeir, C.: *Forecast evaluation for data scientists: common pitfalls and best practices*. Data Mining and Knowledge Discovery, 37, 788–832 (2023); online veröffentlicht am 02.12.2022. DOI: [10.1007/s10618-022-00894-5](https://link.springer.com/article/10.1007/s10618-022-00894-5). Im Projekt durch S38, Nutzerzeile 12, als Betreuerempfehlung und durch das vorhandene lokale PDF belegt. Die Schreibweise „2022“ im Dateinamen bezeichnet nicht zwingend das Bandjahr. Am 29.10.2026 wurden Verlagsmetadaten und Abschnitte zur Evaluation geprüft; keine neue historische Begründung daraus abgeleitet.

**L2:** Hyndman und Athanasopoulos, *Forecasting: Principles and Practice*, dritte Ausgabe, Online-Lehrbuch. Im Code `modeling/dynamic_harmonic_regression.py:10` verlinkt: [komplexe Saisonalität und Stromlastbeispiel](https://otexts.com/fpp3/advanced.html#example-electricity-demand). In S22 zusätzlich verlinkt: [Dynamische harmonische Regression](https://otexts.com/fpp3/dynamic-regression.html#dynamic-harmonic-regression), Abschnitt 10.5; die alte URL `dhr.html` wird inzwischen auf das Kapitel weitergeleitet. Beide relevanten Onlineabschnitte wurden am 29.10.2026 geprüft. Die Projektimplementierung übernimmt nicht automatisch alle Einflussgrößen oder Parameter des Lehrbuchbeispiels.

**L3:** ENTSO-E, *Guidelines for Monthly Statistics Data Collection*, Final version, 31.05.2015, insbesondere Abschnitt 5.1, gedruckte Seite 6. [Originalrichtlinie](https://eepublicdownloads.entsoe.eu/clean-documents/Publications/Statistics/20150531_MS_guidelines_public.pdf). In S16, Assistentenzeile 67, verlinkt und am 29.10.2026 erneut geöffnet. Die historische Richtlinie belegt nicht abschließend die konkrete spätere CSV-Exportsemantik.

Diese drei Werke sind aus zugänglichen Projektquellen bekannte Literaturbezüge. Weitere in Chats bzw. historischem Code genannte Autorennamen oder API-Links gelten hier nicht ohne Prüfung als vollständige wissenschaftliche Literaturgrundlage. Die extern geprüften Fassungen wurden nicht in das Repository kopiert.

### Lokale Sitzungen

Wurzel aller folgenden relativen Pfade: `/Users/timomeyer/.codex/sessions/`. Zeilenzitate im Decision Log beziehen sich auf die jeweilige JSONL-Datei; die Register-IDs sind dauerhaft für diese Dokumentationsfassung vergeben. Die lokalen Dateien sind außerhalb des Repositories und auf anderen Rechnern nicht automatisch zugänglich.

| ID | Sitzungstitel laut lokalem Index | Relativer Dateipfad |
|---|---|---|
| S01 | Rewrite monthly seasonality cell | `2026/09/02/rollout-2026-09-02T21-46-53-01a063a8-f98e-7d42-ade4-d76f6822d1f6.jsonl` |
| S02 | Import EDA loader function | `2026/09/03/rollout-2026-09-03T22-41-27-01a06901-4c2b-71d0-9a37-b348e3338ed3.jsonl` |
| S03 | Use data consistency checks | `2026/09/03/rollout-2026-09-03T23-11-56-01a0691d-34fb-71b2-ba9d-1a2d631bedf3.jsonl` |
| S04 | Explain unexpected timestamps | `2026/09/03/rollout-2026-09-03T23-44-11-01a0693a-ba4d-7510-9753-453f5c1294a9.jsonl` |
| S05 | Explain false time series check | `2026/09/18/rollout-2026-09-18T16-42-28-01a0b4f8-0450-7111-b540-441053cf7451.jsonl` |
| S06 | Configure pytest with VS Code and uv | `2026/09/22/rollout-2026-09-22T21-56-29-01a0cab0-f3da-76f2-afe3-9791fe6a8f7c.jsonl` |
| S07 | Add pytest template | `2026/09/22/rollout-2026-09-22T22-15-15-01a0cac2-211b-78c1-9882-d2110db25b0c.jsonl` |
| S08 | Add repository contributor guide | `2026/09/22/rollout-2026-09-22T22-49-53-01a0cae1-d6e7-7d40-aa83-cb91bddabd6a.jsonl` |
| S09 | Add panel fixture to test_panel | `2026/09/22/rollout-2026-09-22T22-51-59-01a0cae3-c227-7981-9b34-6bbf1a29ec2b.jsonl` |
| S10 | Refactor check_time_series_comple… | `2026/09/23/rollout-2026-09-23T20-01-37-01a0cf6e-270b-7921-b61d-cf942859b77b.jsonl` |
| S11 | Add accessible repo config | `2026/09/23/rollout-2026-09-23T20-23-29-01a0cf82-2b48-7e10-9a5d-c96cf2b7a16e.jsonl` |
| S12 | Passende Typen für Start und Ende | `2026/09/23/rollout-2026-09-23T20-31-34-01a0cf89-914a-7782-9888-6881b3dcf902.jsonl` |
| S13 | Überlappung der Zeitreihen auflösen | `2026/09/23/rollout-2026-09-23T20-49-10-01a0cf99-adaa-7eb3-a905-ccaa8b4a8e8d.jsonl` |
| S14 | Choose data preparation folder name | `2026/09/24/rollout-2026-09-24T20-08-36-01a0d49a-e64d-7b71-9885-38e41260fec3.jsonl` |
| S15 | Add panel CSV export | `2026/09/24/rollout-2026-09-24T20-32-40-01a0d4b0-efd0-71d3-bb15-79bb0dc0903c.jsonl` |
| S16 | Behebe Datenqualitätsfehler | `2026/09/24/rollout-2026-09-24T20-34-57-01a0d4b3-04e7-7ee0-a780-d32c48a37c69.jsonl` |
| S17 | Fix TimeFrom schema mismatch | `2026/09/24/rollout-2026-09-24T21-09-39-01a0d4d2-cc74-75d3-806a-9a12474be484.jsonl` |
| S18 | Erkläre Data-Cleaning-Datei | `2026/09/26/rollout-2026-09-26T14-13-04-01a0dda2-1fd0-7ed2-a670-6d5dd66239f8.jsonl` |
| S19 | Vergleiche validate gold und panel | `2026/09/26/rollout-2026-09-26T14-29-48-01a0ddb1-6e8f-78f2-98ff-e9cbfb60d7ee.jsonl` |
| S20 | Design time-series model protocol | `2026/09/26/rollout-2026-09-26T16-21-41-01a0de17-dd8e-7742-bc25-239c65034abf.jsonl` |
| S21 | Features in build_features ergänzen | `2026/09/26/rollout-2026-09-26T21-05-07-01a0df1b-5aa6-7972-9dcc-940a8495a619.jsonl` |
| S22 | Plan für Dynamic Harmonic Regression | `2026/09/27/rollout-2026-09-27T20-25-12-01a0e41d-2bd7-7e30-afbe-2c51b895acf2.jsonl` |
| S23 | Vergleiche DHR ARIMA und XGBoost | `2026/09/27/rollout-2026-09-27T20-48-40-01a0e432-a998-7a50-be34-7dd8a3ef0eec.jsonl` |
| S24 | Add lead-time error analysis | `2026/09/27/rollout-2026-09-27T21-11-39-01a0e447-b212-7fa0-bfda-6482db43f84a.jsonl` |
| S25 | Bewerte Titel zur Stromprognose | `2026/09/28/rollout-2026-09-28T18-17-36-01a0e8ce-b897-72b2-b6bb-36933ff2d0d7.jsonl` |
| S26 | Aktuelle Datei erklären | `2026/10/10/rollout-2026-10-10T21-51-43-01a1275f-0e69-70c3-8c81-324c9bdf61b3.jsonl` |
| S27 | Lag- und MA-Features aufteilen | `2026/10/10/rollout-2026-10-10T22-24-26-01a1277d-0351-7702-b82c-040a256a8a8d.jsonl` |
| S28 | Explain lag feature type warning | `2026/10/10/rollout-2026-10-10T22-48-14-01a12792-cc0b-7c43-8709-d2c4dee06f49.jsonl` |
| S29 | Generate two weeks of test data | `2026/10/10/rollout-2026-10-10T23-59-24-01a127d3-f30c-7410-8b88-0fec764d0b6e.jsonl` |
| S30 | Debug-Einstellungen fürs Repo finden | `2026/10/11/rollout-2026-10-11T17-38-19-01a12b9d-6d99-7443-a62b-45bdbfc344d5.jsonl` |
| S31 | Explain root logger warning | `2026/10/11/rollout-2026-10-11T18-55-41-01a12be4-3fa8-7dc3-98d2-78c74eee646b.jsonl` |
| S32 | Fix forecasting feature lookup error | `2026/10/11/rollout-2026-10-11T20-56-46-01a12c53-1b41-7a30-b93a-517728cacd2e.jsonl` |
| S33 | Plan lag feature tests | `2026/10/18/rollout-2026-10-18T11-40-14-01a14e62-1945-75c2-9580-d6d63a2a8bcf.jsonl` |
| S34 | Assess sktime for both models | `2026/10/18/rollout-2026-10-18T13-02-57-01a14ead-d43e-7042-b391-23c97315c499.jsonl` |
| S35 | Integrate gradient boosting with sk | `2026/10/20/rollout-2026-10-20T20-15-19-01a15a86-641a-7e22-a4a1-b4400382215e.jsonl` |
| S36 | Fit-Methode fürs Forecasting anpass | `2026/10/20/rollout-2026-10-20T20-34-47-01a15a98-3872-7d43-8122-fac78675df09.jsonl` |
| S37 | Write sktime evaluation script | `2026/10/20/rollout-2026-10-20T20-49-22-01a15aa5-8fc3-7953-906f-600aa545bafb.jsonl` |
| S38 | Gradientboosting-Güte bewerten | `2026/10/23/rollout-2026-10-23T16-41-27-01a16935-aaa5-7462-a86f-a9ee84e526fe.jsonl` |
| S39 | Plan DHR sktime compatibility | `2026/10/23/rollout-2026-10-23T17-57-56-01a1697b-b106-7fd0-b51d-38b94bba651c.jsonl` |

### Lokale Cline-Archive

Wurzel: `/Users/timomeyer/.cline/data/sessions/`. Belege verwenden nullbasierte Positionen im JSON-Array `messages`, bei Bedarf die dortigen Nachrichten-IDs. Daten stammen aus `ts` der Nachricht, umgerechnet nach Europe/Berlin. Frühe Assistentenempfehlungen wurden nicht als geprüfte aktuelle Bibliotheksdokumentation übernommen.

| ID | Beginn in Europe/Berlin | Zahl der Nachrichten | Relativer Dateipfad |
|---|---|---|---|
| C01 | 22.08.2026 16:09 | 105 | `1787407761276_g1lyk/1787407761276_g1lyk.messages.json` |
| C02 | 23.08.2026 16:34 | 12 | `1787495650353_4jsed/1787495650353_4jsed.messages.json` |
| C03 | 23.08.2026 19:09 | 2 | `1787504958629_vg7zt/1787504958629_vg7zt.messages.json` |
| C04 | 23.08.2026 19:20 | 21 | `1787505619253_rv3wy/1787505619253_rv3wy.messages.json` |
| C05 | 24.08.2026 21:19 | 82 | `1787599157438_319rj/1787599157438_319rj.messages.json` |
| C06 | 24.08.2026 21:47 | 18 | `1787600820950_qysjn/1787600820950_qysjn.messages.json` |
| C07 | 24.08.2026 21:53 | 12 | `1787601231719_gcf9n/1787601231719_gcf9n.messages.json` |
| C08 | 30.08.2026 20:57 | 2 | `1788116255973_bkf70/1788116255973_bkf70.messages.json` |
| C09 | 30.08.2026 21:03 | 2 | `1788116608345_pe3ho/1788116608345_pe3ho.messages.json` |
| C10 | 30.08.2026 21:09 | 14 | `1788116962313_slgtf/1788116962313_slgtf.messages.json` |

C01 behandelt einen anfänglichen Import aller elf Tabellen einschließlich der später ungenutzten Datei 2006–2015. C02–C05 betreffen Datentypen, Filter, Excel-Blätter, CSV-Schemata und Float-Inferenz. C06 enthält die ausdrückliche Anweisung, vorhandenes `panel.csv` nicht zu überschreiben. C07 diskutiert Stundenrundung, Datumsindex und Visualisierung. C08–C10 behandeln EDA-Spalten-/Importfehler und Jahreslabels. Diese Inhalte ergänzen insbesondere DEC-001/004/005/006/013. Die Gründe des späteren Ausschlusses vor 2015 bleiben unbekannt.

### Prüfungen während dieser Rekonstruktion

**R01 – Bestands- und Datenprüfung am 29.10.2026.** Ausschließlich lesende Bestandsprüfungen und Berechnungen im Speicher; keine Datenneuschreibung und keine neuen Forecast-Vergleichsläufe:

| Prüfung | Beobachtung |
|---|---|
| Silver | 98.593 Zeilen; Spalten `DateUTC, Value, TimeFrom, TimeTo`; Beginn 2014-12-31 23:00, Ende 2026-03-31 23:00 unter UTC-Annahme |
| Silver-Zeitkonflikte | Sechs zusätzliche Zeilen mit doppeltem Zeitstempel 03:00 und sechs fehlende 02:00-Stunden an den Korrekturdaten 2019–2024; keine exakten Zeilenduplikate |
| Silver-Intervallkonflikte | Je Datum zwei unterschiedliche Lastwerte; die zu korrigierende Zeile trägt `TimeFrom=02:00`, `TimeTo=03:00` |
| Gold | 98.591 Zeilen; ausschließlich `DateUTC, Value`; 2015-01-01 01:00 bis 2026-03-31 23:00 UTC; keine doppelten Zeitstempel oder fehlenden Stunden im konfigurierten Raster; keine fehlenden Felder |
| Bereinigung im Speicher | Die Funktionen `normalize_dates → validate_source_fields → correct_known_timestamps → filter_time_window` mit anschließender Zweispaltenauswahl reproduzieren das geladene Gold exakt; sechs Korrekturen, zwei Zeilen vor Start ausgeschlossen |
| Verwendete Excel-Datei | 40.895 deutsche Zeilen in beiden Blättern, insgesamt 2014-12-31 23:00 bis 2019-08-31 21:00; überall `Cov_ratio=98`; überall `Value != Value_ScaleTo100` |
| CSV-Dateien 2019–2026 | Alle deutschen Zeilen: `Cov_ratio=100`, `Value == Value_ScaleTo100`. Jahreszahlen der Zeilen: 8.760, 8.784, 8.760, 8.760, 8.760, 8.784, 8.760 und 2.160 |
| Quellenüberlappung | 5.830 Excel-Zeilen ab 2019; beim Join mit 2019-CSV kein exakt gleiches `Value`-Paar. Auch die hochgerechnete Excel-Spalte stimmt innerhalb Toleranz 1e-6 in keinem Paar mit CSV-`Value` überein. Der Konflikt ist somit nicht allein durch Auswahl der skalierten Spalte gelöst |
| Reihenfolge | Die 2025-CSV ist in Dateireihenfolge nicht chronologisch. Die Gold-Bereinigung sortiert; die Ingestion selbst sortiert nicht explizit |
| Aktueller Forecast-Split | Ohne Modelllauf nur Splitter angewandt: zwölf vollständige 168-Stunden-Folds, 2.016 bewertbare Stunden; letzter Zielzeitpunkt 2026-03-25 23:00, verbleibend 144 Stunden |
| Benchmark-Splitgrenzen | Aus Konstanten berechnet: Validierung 2025-01-01 bis exklusiv 2025-04-02, Test bis exklusiv 2026-04-01; Trainingsfenster 17.472 Stunden = 104 Wochen |
| Ergebnisdateien | Keine gespeicherten Vergleichsergebnisse unter `data/results/` vorhanden; `evaluation/` enthält keine Implementierung |
| Umgebungsabgleich | Installierte zentrale Bibliotheksversionen stimmen mit dem gelesenen Lockfile überein; siehe Tabelle unten |

Die Prüfungen validieren die strukturelle Umsetzung, nicht unabhängig die physische Zeitzuordnung, die Hochrechnung oder die wissenschaftliche Eignung der Messreihe.

**R02 – vorhandene Tests am 29.10.2026.** Ausgeführt wurde:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m pytest -p no:cacheprovider tests/test_silver_panel.py tests/test_gold_panel.py tests/modeling/test_gradient_boosting.py -q
```

Ergebnis: **10 bestanden, 1 fehlgeschlagen**, zwei sktime-Zukunftswarnungen, Laufzeit laut pytest 2,20 Sekunden. Fehler: `tests/modeling/test_gradient_boosting.py:40` erwartet `model.models`, obwohl das aktuelle Modell nur `model_` besitzt. Die beiden Fit-Aufrufe davor waren erfolgreich. Sämtliche vorhandenen Silver-/Gold-Prüfungen und die beiden Featuretests bestehen. Das ist keine Validierung des vollständigen Benchmarkentwurfs oder der DHR-Prognose. Es wurden keine Tests ergänzt oder korrigiert; Cache-Schreiben und Python-Bytecode-Schreiben waren abgeschaltet.

### Daten- und Softwarefingerabdrücke

SHA-256 der gelesenen lokalen Dateien, berechnet am 29.10.2026. Diese Fingerabdrücke dokumentieren den hier beobachteten Bestand, nicht frühere Experimentdatenstände.

| Datei | SHA-256 |
|---|---|
| `data/bronze/MHLV_data-2015-2019.xlsx` | `5fc842f658a036993c11f6ac0f4ce8884c031c0a7a4791da86bc495d4721138a` |
| `data/bronze/Monthly-hourly-load-values_2006-2015.xlsx` (ungenutzt) | `3a762b8dcee5567cfc84912deee1bbe5e908553d813228634bbd43e7ff0a0b20` |
| `data/bronze/monthly_hourly_load_values_2019.csv` | `dbc826d18ac91966353f77d5bcb757afa4c7e6762079225d740ef142158c006a` |
| `data/bronze/monthly_hourly_load_values_2020.csv` | `f1dd9521b7c4eac7051b80f0c3488e027011a3170ac6dc0964f0e3304e761b33` |
| `data/bronze/monthly_hourly_load_values_2021.csv` | `b702f58dfc19cbfd3ab14c84417a2f11578a12e3216023fc440cd6937a040367` |
| `data/bronze/monthly_hourly_load_values_2022.csv` | `4a59d9e2e073426058f85cfe3b6167d25a9c4f2ed9f5a650d58bf9f13e6f365e` |
| `data/bronze/monthly_hourly_load_values_2023.csv` | `2c524a2ec544ec9b78bdfdced4ecf87fa2c7c43742730d86cbf5dc32c34b5327` |
| `data/bronze/monthly_hourly_load_values_2024.csv` | `60cd96959147a3dc768f3e3e49617850ad848a6d65fc3b18da9886d9adbc94cb` |
| `data/bronze/monthly_hourly_load_values_2025.csv` | `cb18e827305823d5a773755ea4b066e4758205674a58ceb01367f22a8216a36a` |
| `data/bronze/monthly_hourly_load_values_2026.csv` | `c83a171acbabcbcc0b95f333f8e6b379d861bd93dfc1f7817b3d91fb4d0d2199` |
| `data/silver/panel.csv` | `313c5ecbfbc707b22b9cbd75d32684a6f261477269e12c8858d45484e921aabb` |
| `data/gold/panel.csv` | `22123da9b664195094522899fc14bda1124174105ebaf19cb7cb33290ee71327` |
| lokales `run_benchmark.py` | `9d232308a1378ff1ec213bc3e67ab0291e6ae8501d3905a2400eff88a187d75c` |
| `uv.lock` | `ecf0ca4307fb87379b85d80f6beacddb93a4e8609674fe214ca61ed7fbb5b9f8` |

| Paket | Lockfile und lokal installiert |
|---|---|
| NumPy | 2.5.2 |
| pandas | 3.0.5 |
| Polars | 1.43.2 |
| sktime | 1.2.0 |
| statsmodels | 0.15.0 |
| XGBoost | 3.4.1 |
| SciPy | 1.18.1 |
| pytest | 9.1.1 |

Python-Vorgabe: `.python-version=3.12`, Projektanforderung `>=3.12`; Notebookmetadaten nennen 3.12.12. Daraus wird keine Hardware- oder historische Laufzeitkonfiguration abgeleitet.

## Chronologische Rekonstruktion

Git-Daten unten sind die tatsächlich gelesenen Autorzeitstempel einschließlich UTC-Offset. Chatdaten stammen aus Nachrichtenzeitstempeln, in die Nutzerzeitzone Europe/Berlin umgerechnet. Commitdatum, Chatdatum und Ausführungsdatum eines Experiments sind nicht gleichzusetzen.

### 07.08.2026, 14:18–14:39 +02:00 – Projektgrundlage

**Ziel/Komponenten:** Python-Projekt und Entwicklungsumgebung einrichten. **Änderungen:** Initialisierung, `main.py`, `pyproject.toml`, Python-Vorgabe und Editor-Einstellungen; Commits `6c6c236`, `7244301`, `975c450`. **Beobachtung:** `main.py` ist weiterhin eine Begrüßung, kein Experimenttreiber. **Probleme/offen:** Keine Forschungsfrage, Datenversion oder Hardwarefestlegung aus diesen Commits ableitbar. **Entscheidungen:** DEC-035.

### 22.08.2026, 14:59:24 +02:00 – Lockfile ergänzt

**Ziel/Komponenten:** Umgebungsverwaltung. **Änderung:** `uv.lock` in `2791a02`. **Beobachtung:** Abhängigkeiten sind versioniert; der Commitname „added venv“ beweist nicht die Versionierung einer virtuellen Umgebung. **Offen:** Keine rekonstruierbare komplette historische Hardware-/Ausführungskonfiguration. **Entscheidungen:** DEC-035.

### 22.08.2026, 16:10–16:22 +02:00 – Früher Importversuch einschließlich Daten vor 2015

**Ziel:** CSV-/Excel-Dateien mit Polars einlesen; C01, `messages[2]`. **Plan:** Alle acht CSVs, das ältere Excel-Blatt 2006–2015 und die zwei Blätter 2015–2019 laden (`messages[22,24]`). **Probleme:** Zunächst falsch vorgeschlagenes Excel-Backend und falsche Parameter; später Korrektur auf fastexcel, Erkennung der abweichenden Trennzeichen und Float-Inferenzprobleme (`messages[50,71,79]`). **Berichtetes Ergebnis:** Assistent meldet das erfolgreiche Laden aller elf Tabellen (`messages[91]`); kein daraus belegtes Forecast-Experiment. **Offen:** Warum der spätere endgültige Panelimport die ältere Datei nicht mehr enthält, ist nicht dokumentiert. **Entscheidungen:** DEC-001/004/035.

### 23.08.2026, 21:20:52 +02:00 – Erste Ingestion

**Ziel:** Deutsche Lastdaten aus Excel und CSV zusammenführen. **Komponenten:** `ingestion/load_raw.py`, zusätzliche Abhängigkeiten, Commit `4593c99`. **Änderung:** Quellenliste, Länderfilter, Spaltenauswahl. **Beobachtung:** Der methodische Rahmen ist eine einzelne nationale Lastreihe. **Probleme/offen:** Gründe der Anfangsjahr- und Zielspaltenwahl fehlen; die Abdeckungsdifferenz wird erst bei R01 ausdrücklich festgestellt. **Entscheidungen:** DEC-001/002/004.

### 24.08.2026, 21:37:38 und 22:07:27 +02:00 – Import repariert, erste EDA

**Ziel:** Dateien tatsächlich einlesen und erste Struktur darstellen. **Änderungen:** `fc0d36b` ergänzt Pfade, zwei Excel-Blätter, Trennzeichenfallback und Exportaufruf; `bb5accc` ergänzt Float-Schemata, Datumsnormalisierung, Nichtüberschreiben und EDA-Notebook. **Ergebnisartefakt:** Das historische Notebook enthält 104.423 Werte in `describe()`; die damals gespeicherte Quelldatenversion ist nicht eigenständig archiviert. **Probleme:** Der frühe Notebookcode rundet auf Stunden, die aktuelle Bereinigung weist unterstündige Werte ab. Der historische Bestand enthält die später beseitigte Quellenüberlappung; die Zahl allein beweist keinen sauberen Panelstand. **Offen:** Kein verlässliches Ausführungsdatum der gespeicherten Zellen. **Entscheidungen:** DEC-003/004/005/006/013/035.

### 24.08.2026, 21:47–22:01 +02:00 – Nichtüberschreibschutz und frühe EDA-Zeitachse

**Ziel/Änderung:** C06, `messages[0,17]`, beauftragt und berichtet den Schutz vorhandener Paneldateien vor Überschreiben. C07 bespricht die Darstellung nur mit Datum/Stunde und einen Zeitindex; ein früher Vorschlag rundet auf Stunden. **Beobachtung:** Das frühe Notebook in `bb5accc` enthält tatsächlich `dt.floor("h")`; der heutige Datenaufbereitungscode weist Unterstunden stattdessen ab. **Offen:** Die Anweisung belegt das Nichtüberschreibverhalten, aber keine vollständige Datenversionierungsstrategie. **Entscheidungen:** DEC-005/006/035.

### 30.08.2026, 20:57–21:12 +02:00 – Cline-Checkpoints und zugehörige EDA-Dialoge

**Ziel/Änderungen:** Aus Checkpointreferenzen sind Zwischenstände der frühen Entwicklung erreichbar; unter anderem `67cd070`, `bbdeb5c`, `18264d9`, `fe8fd32`. Die tatsächlich gefundenen Dialoge C08–C10 dokumentieren zusätzlich einen falschen EDA-Spaltennamen, einen fehlenden matplotlib-Import und Jahreslabels. **Beobachtung:** Checkpointbäume allein sind keine eigenständigen Forschungsprotokolle. **Offen:** Kein Forecast-Experiment aus diesen Quellen belegt. **Entscheidungen:** DEC-013; keine neue methodische Entscheidung aus reinen Darstellungsreparaturen.

### 02.09.2026, Chat 21:47–22:42; Commit 22:56:21 +02:00 – Saisonprofile und ADF-Diskussion

**Ziel:** Monatsdarstellung um Wochen- und Tagesprofile ergänzen. **Komponenten:** S01 und Commit `f529db2`, `eda/utils.py`. **Beobachtungen:** Nutzer berichtet in S01:180 ADF −23,301889136439137 und p-Ausgabe 0,0; dieser Wert unterscheidet sich vom später gespeicherten aktuellen Notebookwert. **Probleme/offen:** Keine Gleichsetzung der Datenstände; saisonale Einheitswurzeltests werden diskutiert, aber nicht als durchgeführt belegt. **Entscheidungen:** DEC-013/014.

### 03.09.2026, 23:42:02 +02:00 – Erste Datenqualitätsprüfung

**Ziel:** Fehlwerte, Konsistenz und Zeitreihenvollständigkeit prüfen. **Komponenten:** `18bf53d`, historisches `quality_check/quality_check.ipynb`, S02–S04. **Ergebnisse:** Gespeicherte Ausgabe meldet keine Fehlwerte und Vollständigkeit für den damals eingestellten Teilzeitraum mit 10.921 Sollzeitpunkten bei 104.423 Gesamtzeilen. **Problem:** „Vollständig“ für einen Ausschnitt ist keine Vollständigkeit des Gesamtzeitraums. S04:49 berichtet bei erweitertem Zeitraum Lücken im März und viele 2019-Duplikate. **Offen:** Exportzeitzone und Quellenüberlappung werden noch untersucht. **Entscheidungen:** DEC-003/006/007/011.

### 18.–23.09.2026 – Qualitätssicherung auf pytest umstellen

**Ziel:** Große Prüfungsfunktion in gezielte Prüfungen zerlegen und Testumgebung nutzbar machen. **Komponenten:** S05–S12; `21c0b81` vom 22.09., 23:12:10 +02:00; `quality_check`-Notebook entfällt, Tests wandern nach `tests/`. **Probleme:** Importpfade, Fixtures und Verantwortung einzelner Prüfungen werden diskutiert. YAML/Pydantic bleiben Konfigurationsvorschläge. **Ergebnisse:** Vorhandene Tests sind Implementierungsartefakte, kein finaler wissenschaftlicher Versuch. **Offen:** Datenunabhängigkeit der Tests und eine verbindliche Qualitätsschranke. **Entscheidungen:** DEC-011/035.

### 23.09.2026, Chat 20:53–21:14; Commit 21:24:40 +02:00 – Quellenpriorität und Zeitfenster

**Ziel:** Überlappung des Jahres 2019 lösen. **Komponenten:** S13, Commit `8a55cf5`. **Änderung:** Excel vor 2019 abschneiden; zentrale Zeitkonstanten einführen. **Beobachtungen:** S13:63 berichtet 5.830 Konfliktzeilen, die R01 später bestätigt. **Probleme:** Quellenpriorität ersetzt keine Erklärung unterschiedlicher Messwerte; ein Zeitzonentypkonflikt tritt beim Vergleich auf. **Offen:** Die Anbieterrevision ist nur eine Hypothese, ebenso die fachliche Begründung des Analysebeginns um 01:00. **Entscheidungen:** DEC-003/006/008/037.

### 24.09.2026, Chat 20:35–21:48; Commit 22:01:48 +02:00 – Gold-Pipeline und sechs Korrekturen

**Ziel:** Fehler der Silver-Qualität prüfen und ein nutzbares Gold-Panel erzeugen. **Komponenten:** S15–S17, Commit `ce631ca`. **Änderungen:** Intervallfelder im Import, Quelleingangsvalidierung, UTC-Annahme, exakte Duplikate, gezielte Korrekturen, Zeitraumfilter, abschließende Indexvalidierung, Gold-Writer. **Beobachtungen:** S16:31 erklärt 436 vermeintliche Duplikate als Testfehler. S16:116 berichtet 98.591 Zeilen, sechs Korrekturen, zwei ausgeschlossene Anfangsstunden und 28 bestandene Tests. S16:173 berichtet nach einem weiteren Umbau neun bestandene vorhandene Tests. Dies sind **historische Assistentenmeldungen**, keine aktuelle Testbilanz. **Probleme:** UTC bleibt Annahme; Bericht/README über gespeicherte Auditfelder widerspricht dem später betrachteten Exportcode bereits in diesem Commit. Dessen letzter Exportschritt selektiert zwei Spalten und benennt sie in `timestamp/load` um. **Offen:** Physische Zeitzuordnung und dauerhafte Auditsicherung. **Entscheidungen:** DEC-004–012.

### 26.09.2026, Chat 14:13–15:00; Commit 15:03:07 +02:00 – Cleaning-Refaktorierung mit methodischen Folgen

**Ziel:** Verständlichkeit und Verantwortlichkeiten der Bereinigung verbessern; S18/S19. **Änderungen:** `ed2dee2` trennt Datumsnormalisierung und Feldprüfung, führt `filter_time_window` ein und stellt Exportnamen `DateUTC/Value` her. **Methodisch relevant:** Exakte Duplikatentfernung, `validate_gold` und Grenzprüfungen entfallen. **Probleme:** Es treten im Chat Index-/Spaltenfehler und unbekannte Zeitkonflikte auf. Der Wunsch nach weniger Prüfungszeilen belegt nicht, dass die methodische Abschwächung beabsichtigt war. **Offen:** README und tatsächlicher Validierungsablauf abgleichen. **Entscheidungen:** DEC-010/011/012.

### 26.09.2026, Chat ab 16:21 bzw. 21:08; Commit 21:59:03 +02:00 – Modellvertrag, Zerlegung und erste XGBoost-Modelle

**Ziel:** Modellstruktur und erste Tagesprognose implementieren. **Komponenten:** S20/S21, Commit `7c0184a`. **Änderungen:** `ForecastModel`, fünf realisierte Merkmale, 24 Modelle nach Zieluhrzeit, Gold-basierter kurzer Testlauf als Wunsch des Nutzers; additive Zerlegung und MSTL erscheinen im Notebook. **Beobachtungen:** Lags 1/2 werden wegen Verfügbarkeit im Tagesmodell verworfen; Mittelwerte enden vor Tagesbeginn. **Probleme:** Paketinstallation/XGBoost-Umgebung und frei wählbare Trainings-/Testzeiträume werden diskutiert. **Offen:** Keine belegte Hyperparameteroptimierung oder finale Vergleichsauswertung. **Entscheidungen:** DEC-015/018/019/021/035.

### 27.09.2026, 20:25–20:42 +02:00 – DHR-Entwurf und berichteter Pilot

**Ziel:** DHR nach dem damaligen Modellvertrag implementieren; S22. **Änderungen laut Sitzung:** Fourier-Terme, nicht saisonale ARIMA-Fehler, fixe Phase, Skalierung, Zustandsaktualisierung ohne Neuparametrisierung; damals auch zusätzliche Tests und Evaluation. **Berichtetes Ergebnis:** S22:85 meldet 38 bestandene Tests und einen Gold-Probelauf über **zwei Prognosetage**, DHR-MAE ungefähr 2.388 gegenüber Wochen-Naiv-MAE ungefähr 1.162. **Einordnung:** Pilot mit Startkonfiguration, keine finale Aussage zur Überlegenheit eines Verfahrens. Vollständige Parameter-, Datums- und Ergebnisartefakte des Piloten liegen heute nicht vor; die Zahlen werden nicht als neu verifiziert ausgegeben. **Offen:** Die Klasse erscheint erst in `876783d` am 11.10. im Hauptbranch. Zwischen Chatimplementierung und Commit fehlen dauerhaft verfügbare Dateien. **Entscheidungen:** DEC-023–027/032/036.

### 27.09.2026, 20:48–21:13 +02:00 – Zwei Modelle, zwei Horizonte, Lead-Auswertung

**Ziel:** Vergleichsskript mit 24-/168-Stunden-Prognosen und MAE/RMSE/MAPE, S23/S24. **Entscheidung:** Nutzer streicht separates klassisches ARIMA und bestätigt Horizonte statt Eingabefenster. **Änderungen laut Sitzung:** gleiche Historien/Ursprünge, rekursive XGBoost-Folgetage, Exporte von Konfiguration und Einzelprognosen; anschließend exakte Lead-MAE. **Beobachtungen:** S23:65 berichtet 34 Tests plus synthetischen Durchlauf, S24:38 sechs Vergleichstests. **Probleme:** Diese Dateien und Exporte fehlen heute; damalige Testmeldungen sind deshalb nur historische Sitzungsbelege. ACF/PACF stammen laut Nutzer aus der ursprünglichen Lastreihe, nicht aus DHR-Residuen. **Offen:** Finale Umsetzung und Originalartefakte wiederfinden, keine erfundene Commitzuordnung. **Entscheidungen:** DEC-014/016/021/028/032/034/036.

### 28.09.2026, 18:17–18:18 +02:00 – Arbeitstitel diskutiert

**Ziel:** S25 prüft den Nutzertitel „Prognose des deutschen Stromverbrauchs: Ein empirischer Vergleich von DHR-ARIMA und Gradient Boosting“. **Beobachtung:** Der Assistent schlägt „Kurzfristige Prognose der deutschen Stromlast … XGBoost“ vor. **Offen:** Eine endgültige Titelannahme ist nicht belegt. **Entscheidungen:** DEC-001/016/028.

### 10.–11.10.2026 – Featureverständnis, Testdaten und Wochenrekursion

**Ziel:** Fourier-Dimension und Featuremethoden verstehen; synthetische Tests und Forecast-Ausführung verbessern. **Quellen:** S26–S32, `876783d` vom 11.10., 17:45:45 +02:00, und `33fdffd` um 21:31:41 +02:00. **Änderungen:** DHR wird eingecheckt; Gold-Zeilenduplikattest entfällt; XGBoost berechnet sieben Tagesblöcke rekursiv. **Problem:** Das Entfernen fehlender Featurezeilen während der Prognose hatte angefragte Zukunftszeilen entfernt; S32 dokumentiert den daraus folgenden Lookupfehler. **Beobachtungen:** Die damalige Struktur besitzt weiterhin 24 Zieluhrzeitmodelle. UTC-Intervallstart gegen Stundenende wird erneut diskutiert. **Offen:** Keine empirisch belegte Wahl von drei Harmonischen. **Entscheidungen:** DEC-006/010/018–021/024/026/035.

### 18.10.2026, Chat 11:40–14:05; Commit 21:34:29 +02:00 – Featuretests und Evaluationsdesign

**Ziel:** Lag-/Mittelwertmerkmale testen und beide Modelle gemeinsam evaluieren. **Komponenten:** S33/S34, Commit `8b6e383`. **Änderungen:** Kleine lineare Testdaten und erwartete Featurewerte; Diskussion sktime, gemeinsamer Horizonte und direkter gegenüber rekursiver Prognose. **Beobachtung:** S34 empfiehlt tägliche Ursprünge, gemeinsame 168-Stunden-Prognosen und 24-Stunden-Präfixauswertung; das ist ein Vorschlag, nicht das später realisierte Wochenraster. **Offen:** Welche Vorschläge werden final übernommen? **Entscheidungen:** DEC-018/019/021/027–029/035.

### 20.10.2026, Chat ab 20:17; Commit 21:09:44 +02:00 – sktime-Migration und erste zeitliche Evaluation

**Ziel:** Rekursives XGBoost als sktime-Modell; S35–S37. **Änderungen:** `c95e29f` ersetzt 24 Modelle durch ein gemeinsames Modell, führt `_fit/_predict` und wachsende Wochen-Backtests ein; Testbeginn zunächst 2025-04-01. **Beobachtung:** Nutzer postet in S37:57 bereits Fold-MAE/-MSE und Laufzeiten aus 2025. **Problem:** Der Testzeitraum wird damit sichtbar; eine spätere Behauptung vollständiger Unberührtheit muss diesen Verlauf berücksichtigen. Empfohlene XGBoost-Fouriermerkmale und stündlich rollende Mittelwerte werden im eingecheckten Modell nicht realisiert. **Offen:** Modellstrategie und Featurewahl wissenschaftlich begründen. **Entscheidungen:** DEC-017–022/027/029/030/032/034.

### 23.10.2026, Chat ab 16:42; Commit 17:49:36 +02:00 – Evaluationsliteratur und wechselnde Testgrenzen

**Ziel:** Modellgüte wissenschaftlich bewerten; S38 mit Betreuerempfehlung L1. **Änderungen:** Validierungsphase wird diskutiert; `e55c885` setzt Testbeginn auf 2024-04-01 und korrigiert die Ausgabe von Foldzahl/Stunden/Tagen. **Berichtetes Ergebnis:** S38:221 enthält 469 Blöcke, 78.792 Stunden, MAE 2.485,686 und RMSE 3.857,635. **Einordnung:** Diese Chat-Ausgabe gehört laut anschließender Diskussion zu einer unbeabsichtigt breiten Zeitaufteilung, nicht nachweislich zu einer final definierten Zwei-Jahres-Testphase. **Probleme:** Tage und Wochen wurden zuvor verwechselt; Nutzer wollte später zwei Jahre testen. **Offen:** Tatsächlicher Ursprung der ausgegebenen Zahlen, Parametereinfrieren und Testunabhängigkeit. **Entscheidungen:** DEC-028–030/032/036.

### 23.–24.10.2026 – DHR-Migration und Rechenaufwand diskutiert

**Ziel:** DHR ebenfalls an sktime anbinden, S39. **Änderungen:** Am 23.10. zunächst Plan und Codevorschlag; Nutzer stoppt eine automatische Umsetzung und implementiert später selbst. Nachricht vom 24.10., 21:45 Europe/Berlin, berichtet längere Evaluation gegenüber XGBoost. **Beobachtung:** Die Erklärung nennt SARIMAX-Schätzung und wiederholte Re-Fits; eine kontrollierte Laufzeitmessung ist nicht vorhanden. Optionen wie `cov_type="none"`, kürzere Historie und geringeres `maxiter` werden vorgeschlagen, aber nicht als übernommen belegt. **Offen:** Hardware, tatsächliche Zeiten und Konvergenzstatus. **Entscheidungen:** DEC-024–027/029/035.

### 26.10.2026, 20:58:18 +01:00 – Benchmarkentwurf eingecheckt

**Ziel:** DHR und XGBoost mit Baselines gemeinsam auswerten. **Komponenten:** `f1d64b3`, `ForecastingBenchmark`. **Änderungen:** Feste 104-Wochen-Trainingsfenster, 13 Validierungs-/52 Testwochen, fünf Seeds plus Ensemble, MAPE/MASE, gepaarte wöchentliche Verlusttests, Einzelprognosen und Metadatenexport. DHR migriert zu sktime; im separaten Forecast-Runner wird der Testbeginn auf 2026-01-01 geändert. **Beobachtung:** Der Docstring behauptet Festlegung vor Tests; es gibt keine nachgewiesenen vollständigen Benchmark-Ergebnisartefakte. **Probleme:** Abhängigkeit wöchentlicher Verlustdifferenzen ist bei der Testvarianz nicht automatisch gelöst. **Offen:** Vorabfestlegung, Hauptmetrik und finale Modell-/Fensterdefinition. **Entscheidungen:** DEC-022–033/036.

### Nach diesem Commit, vor der Bestandsaufnahme am 29.10.2026 – Benchmark lokal gekürzt

**Datum:** Genaues Änderungsdatum nicht aus Git rekonstruierbar; nur die Reihenfolge ist sicher. **Änderungen:** Der lokale Diff entfernt Docstring, Argumentparser, Verlusttests, Diagnostik, Forecast-Umformung, aggregierte Exporte und Metadaten. **Beobachtung:** `main()` verwendet weiterhin `args.period`, obwohl `args` nicht definiert ist. **Probleme:** Skript ist im aktuellen Stand nicht direkt ausführbar; verbliebene Konstanten beweisen keine ausgeführte Auswertung. **Offen:** Zwischenstand oder beabsichtigte Reduktion? Keine Mutmaßung über das Motiv. **Entscheidungen:** DEC-028–033/034/036.

### 29.10.2026 – Diese Rekonstruktion und begrenzte Verifikation

**Ziel:** Quellenbelegte Dokumentation, keine Implementierungsänderung. **Änderungen:** Ausschließlich die drei Dokumentationsdateien unter `docs/research/`. **Ergebnisse:** R01 und R02, 37 Entscheidungsdatensätze: 13 A, 20 B, 4 C. Der neu geprüfte Unterschied zwischen Excel-Abdeckung 98 und CSV-Abdeckung 100 ist ein aktueller Analysebefund und wird nicht rückwirkend als bekanntes Entscheidungsmotiv ausgegeben. **Offen:** Die fünf priorisierten Fragen stehen im Methodology Mapping.

## Verlässliche Ergebnisgrenzen

Vorhanden sind explorative Notebookausgaben, historische Chatberichte zu Piloten und einzelnen Backtests sowie die aktuellen Struktur-/Testprüfungen R01/R02. **Ein finaler, vollständig archivierter DHR-XGBoost-Vergleich mit belegter Validierung, unveränderter Konfiguration und geprüfter Inferenz ist aus den zugänglichen Quellen nicht nachgewiesen.**

Die aktuelle Gold-Reihe ist strukturell konsistent und aus dem vorhandenen Silver-Stand im Speicher reproduzierbar. Ob sie fachlich zeitlich korrekt und über alle Jahre bezüglich Abdeckung harmonisiert ist, bleibt gesondert zu bestätigen.

