# Rekonstruiertes Decision Log

Stand der Analyse: **29.10.2026**. Referenz: `f1d64b39f14a404f70ddfb422690a11acfa78f45` und der bereits zu Beginn lokal geänderte Stand von `run_benchmark.py`. Vorhandene Implementierungen wurden nicht geändert.

## Einordnung und Leseregeln

Dieses Log unterscheidet **A – explizit dokumentierte Entscheidung samt Begründung**, **B – Umsetzung nachgewiesen, ursprüngliche Begründung nicht dokumentiert** und **C – Hypothese bzw. ungeklärte endgültige Festlegung**. Dazu gehören die Statuswerte Bestätigt, Rekonstruiert und Zu klären. „Bestätigt“ bezeichnet den Quellenbeleg, nicht die wissenschaftliche Richtigkeit oder einen final freigegebenen Versuchsplan. Bei einer revidierten Entscheidung kann die historische Begründung belegt sein, während der Grund ihrer Revision fehlt.

Alle „möglichen wissenschaftlichen Begründungen“ sind **nachträgliche Ansätze und noch zu prüfen**. Assistentenantworten sind als solche gekennzeichnet: Ein Vorschlag wird erst zusammen mit Nutzeranweisung oder späterer Implementierung als übernommene Entscheidung gewertet. Historische Testmeldungen sind keine aktuellen Testergebnisse.

Die Quellenkürzel **S01–S39**, **C01–C10**, **L1–L3** und **R01–R02** werden im [Research Log](research_log.md) aufgelöst. S-Zeilen beziehen sich auf physische Zeilen lokaler JSONL-Dateien, C-Belege auf nullbasierte Einträge im `messages`-Array der Cline-JSON-Dateien. Dateizeilen gelten für den analysierten Arbeitsstand; historische Belege verwenden `Commit:Pfad`. Notebookzellen werden ab 0 gezählt und zusätzlich durch Zell-ID benannt.

## Übersicht

37 Einträge: **13 Kategorie A**, **20 Kategorie B**, **4 Kategorie C**. Die Zählung beschreibt die Evidenz der Einträge, nicht 37 abschließend festgelegte Versuchskriterien.

Besonders folgenreich sind die Quellzeitannahme (DEC-006), die sechs Korrekturen (DEC-007), entfallene Validierung und Auditpersistenz (DEC-011/012), die Modelländerung bei der sktime-Migration (DEC-021), widersprüchliche Versuchsstände (DEC-028/029) und die bereits betrachteten späteren Testdaten (DEC-030).

## Entscheidungen

### DEC-001: Deutsche Lastreihe ab 2015 aus ausgewählten Exporten

> **Update 2026-11-25:** Die Arbeitsmappe 2015–2019 wird nicht mehr eingelesen; das Panel beginnt am 01-01-2019 (`config.TRAIN_START`) und besteht nur aus den acht CSV-Dateien (`ingestion/sources.py`).

**Status:** Rekonstruiert

**Evidenzkategorie:** B

**Themenbereich:** Datengrundlage

**Entscheidung:**  
Die Pipeline verwendet Deutschland (`CountryCode == "DE"`), die Arbeitsmappe `MHLV_data-2015-2019.xlsx` und acht Jahres-CSV-Dateien 2019–2026. Die ebenfalls vorhandene Datei 2006–2015 wird nicht eingelesen.

**Kontext / Problemstellung:**  
Eine durchgehende nationale Zeitreihe wird aus mehreren Exporten aufgebaut; die Forschungsdiskussion betrifft deutsche Stromlast.

**Alternativen:**  
C01, Assistenteneinträge 22/24, plant zunächst auch das Einlesen der Datei 2006–2015; Eintrag 91 berichtet das Laden aller elf Tabellen einschließlich dieses Bestands. Der spätere Ausschluss aus der aktuellen Panelpipeline ist belegt, sein Grund nicht.

**Begründung zum Entscheidungszeitpunkt:**  
Nicht dokumentiert.

**Mögliche wissenschaftliche Begründung:**  
Nachträglicher Begründungsansatz, zu prüfen: Eine nationale Reihe begrenzt Heterogenität; ein Beginn 2015 könnte Datenkompatibilität erleichtern. Für genau diese Grenze fehlt ein Nachweis.

**Literaturgrundlage:**  
L3 enthält eine Definition stündlicher Last. Die Auswahl Deutschlands und des Anfangsjahres benötigt zusätzlich eine fachliche Begründung und exportbezogene Metadaten.

**Konkrete Umsetzung:**  
`CSV_FILES_PATH`, `XLSX_FILE_PATH`, `load_2015_2019_file`, `filter_country`; zwei Excel-Blätter werden vertikal zusammengefügt.

**Auswirkungen auf das Experiment:**  
Die Aussagekraft beschränkt sich zunächst auf eine Reihe. Dateiname und Landescode belegen weder vollständige Marktabdeckung noch eine repräsentative Auswahl mehrerer Prognoseaufgaben.

**Evidenz / Quellen im Projekt:**  
`ingestion/load_raw.py:6–17,41–56,73–89`; Einführung `4593c99`; C01, `messages[2,22,24,91]`; S25, Nutzerzeile 9; lokale Bronze-Inventur R01.

**Offene Fragen:**  
Warum 2015 statt früher? Welche genaue Lastdefinition und geografische Abdeckung gelten je Export? Ist der diskutierte Arbeitstitel final?

**Relevanz für die Bachelorarbeit:**  
Datengrundlage; Untersuchungsgegenstand.

---

### DEC-002: Unskalierte Zielspalte Value und Verzicht auf Abdeckungsmerkmale

> **Update 2026-11-25:** Ohne Arbeitsmappe tragen alle verwendeten Zeilen `Cov_ratio=100`. `PanelCleaner._check_coverage` bricht bei abweichender Abdeckung ab; eine Harmonisierung entfällt.

**Status:** Rekonstruiert

**Evidenzkategorie:** B

**Themenbereich:** Datengrundlage

**Entscheidung:**  
Als Zielgröße bleibt `Value` erhalten. `Value_ScaleTo100`, `Cov_ratio`, Erstellungs- und Aktualisierungsdaten gelangen nicht ins Silver-Panel.

**Kontext / Problemstellung:**  
Die Exporte besitzen mehrere Wert- und Metadatenspalten.

**Alternativen:**  
Nicht dokumentiert.

**Begründung zum Entscheidungszeitpunkt:**  
Nicht dokumentiert.

**Mögliche wissenschaftliche Begründung:**  
Nachträglicher Begründungsansatz, zu prüfen: Eine einheitliche Zielvariable vereinfacht den Vergleich. Die Gleichheit beider Wertspalten kann den Verzicht auf Hochrechnung nur für tatsächlich geprüfte Daten stützen.

**Literaturgrundlage:**  
L3 zur Repräsentativität; keine geprüfte spezifische Dokumentation der neueren Exportspalten. Exportbeschreibung und Definition von MW gegenüber MWh recherchieren.

**Konkrete Umsetzung:**  
`select_rellevant_columns` wählt `DateUTC`, `Value`, `TimeFrom`, `TimeTo`. R01 zeigt für sämtliche deutschen CSV-Zeilen 2019–2026 `Cov_ratio=100` und identische `Value`/`Value_ScaleTo100`. Die nachfolgende vollständige Prüfung des deutschen Anteils beider verwendeter Excel-Blätter ergibt dagegen 40.895 Zeilen mit `Cov_ratio=98`; in sämtlichen Zeilen unterscheiden sich `Value` und `Value_ScaleTo100`.

**Auswirkungen auf das Experiment:**  
Die Pipeline verbindet vor 2019 Werte mit ausgewiesener Abdeckung 98 mit späteren Werten bei Abdeckung 100, ohne Abdeckung oder Hochrechnung zu übernehmen. Dies ist ein konkretes Risiko eines Messniveauwechsels. Die fachliche Bedeutung der Abdeckung und eine geeignete Harmonisierung sind zu klären. Die MW-Beschriftung im Projekt ist keine eigenständige Exportdefinition; Monatsmittel der Last sind keine Monatsenergiesummen.

**Evidenz / Quellen im Projekt:**  
`ingestion/load_raw.py:19–23,55–56`; `eda/utils.py:51–54`; R01, Bronze-CSV-Feldprüfung; ungenutzte ältere Arbeitsmappe enthält einen Hochrechnungshinweis.

**Offene Fragen:**  
Soll vor 2019 die auf 100 skalierte Reihe verwendet werden? Was bedeutet die Abdeckung 98 fachlich, und ist die Hochrechnung vergleichbar mit späteren Exporten? Liegt mittlere Leistung in MW vor?

**Relevanz für die Bachelorarbeit:**  
Datengrundlage; Definition der Zielvariable.

---

### DEC-003: CSV erhält Vorrang im Überlappungsjahr 2019

> **Update 2026-11-25:** Gegenstandslos, da die Arbeitsmappe entfällt; `remove_overlap` wurde entfernt.

**Status:** Bestätigt

**Evidenzkategorie:** A

**Themenbereich:** Datenaufbereitung

**Entscheidung:**  
Excel-Zeilen ab 2019-01-01 werden vor der Zusammenführung entfernt; das Jahr 2019 stammt aus der CSV.

**Kontext / Problemstellung:**  
Die Excel-Lieferung reicht in 2019 hinein und überlappt die CSV mit abweichenden Werten.

**Alternativen:**  
Einfaches Anhängen und pauschales `unique()` wurden in S13 ausdrücklich als unzureichend diskutiert; Gründe für eine andere fachliche Quellenpriorität sind nicht dokumentiert.

**Begründung zum Entscheidungszeitpunkt:**  
S13, Assistentenzeile 63, empfiehlt die neuere CSV wegen der abweichenden Werte und fordert eine klare Quellenpriorität. Die anschließende Implementierung ist in `8a55cf5` belegt. Eine tatsächliche Revision durch den Anbieter wird dort nur vermutet.

**Mögliche wissenschaftliche Begründung:**  
Nachträglicher Begründungsansatz, zu prüfen: Eine deterministische Priorität verhindert doppelte Gewichtung und beliebige Konfliktauflösung; Aktualität allein beweist keine höhere Datenqualität.

**Literaturgrundlage:**  
Keine geprüfte Anbieterbeschreibung zur Revision der Exporte. Versions- und Revisionspolitik der Datenquelle recherchieren.

**Konkrete Umsetzung:**  
`remove_overlap` filtert ausschließlich den Excel-Anteil mit `DateUTC < 2019-01-01`.

**Auswirkungen auf das Experiment:**  
Die Werteauswahl wird reproduzierbar, kann aber einen Messbruch zwischen Quellen erzeugen. S13 berichtet 5.830 überlappende Zeilen; dies ist ein historischer Analysebefund, keine neue Vollprüfung der Excel-Datei.

**Evidenz / Quellen im Projekt:**  
`ingestion/load_raw.py:69–79`; Commit `8a55cf5`; S13, Zeilen 9,25,63 und 81–85.

**Offene Fragen:**  
Warum gilt die CSV fachlich als maßgeblich? Welche Änderungen erklären die abweichenden Werte?

**Relevanz für die Bachelorarbeit:**  
Datenaufbereitung; Zusammenführung und Quellenkonflikte.

---

### DEC-004: Formatspezifisches Einlesen und vereinheitlichte Datentypen

**Status:** Bestätigt

**Evidenzkategorie:** A

**Themenbereich:** Datenaufbereitung

**Entscheidung:**  
CSV-Dateien werden zunächst tabulatorgetrennt, bei fehlendem `CountryCode` erneut semikolongetrennt gelesen; numerische Felder, Datum und Intervallzeiten werden explizit typisiert.

**Kontext / Problemstellung:**  
2021 und 2022 verwenden andere Trennzeichen; Excel- und CSV-Zeitspalten hatten inkompatible Datentypen.

**Alternativen:**  
Für die Intervallzeiten wurden in S17 Casting- und Parsingvarianten diskutiert; eine systematische Bibliotheksauswahl ist nicht dokumentiert.

**Begründung zum Entscheidungszeitpunkt:**  
Der Kommentar in `load_raw.py:30` nennt die abweichenden Trennzeichen. Bereits C01, Assistenteneinträge 50/71/79, dokumentiert den Wechsel zum tatsächlich benötigten fastexcel-Backend, unterschiedliche CSV-Schemata und eine fehlerhafte Integer-Inferenz. S17 ergänzt spätere Schema- und Zeitparsingfehler.

**Mögliche wissenschaftliche Begründung:**  
Nachträglicher Begründungsansatz, zu prüfen: Explizite Typisierung kann unerwünschte Typinferenz und schemabedingte Datenverluste vermeiden. Das Vorhandensein einer Spalte ist jedoch keine vollständige Formatvalidierung.

**Literaturgrundlage:**  
Keine wissenschaftliche Vergleichsliteratur im Projekt; für die konkrete Technik sind versionsgebundene Polars-/fastexcel-Dokumentationen noch als technische Referenzen festzuhalten.

**Konkrete Umsetzung:**  
`FLOAT_OVERRIDES`, `str.to_datetime(time_unit="ms")`, `str.to_time()`, Excel-Casts auf `Datetime("ms")` und `Time`; Polars/fastexcel beim Import, pandas im weiteren Ablauf.

**Auswirkungen auf das Experiment:**  
Einheitliche Schemata ermöglichen vertikale Konkatenation. Datumsinterpretation und ungültige Eingaben bleiben gesondert zu prüfen.

**Evidenz / Quellen im Projekt:**  
`ingestion/load_raw.py:19–47`; Commits `fc0d36b`, `bb5accc`, `ce631ca`; C01, `messages[50,71,79]`; C05, `messages[22,29,79,81]`; S17, Nutzerzeilen 9,30; R01 bestätigt CSV-Trennzeichen.

**Offene Fragen:**  
Sind sämtliche Quellformate ausdrücklich spezifiziert? Soll das Datumsformat statt automatischer Erkennung festgelegt werden?

**Relevanz für die Bachelorarbeit:**  
Implementierung; Datenimport.

---

### DEC-005: Bronze-, Silver- und Gold-Stufen mit unterschiedlichen Schreibregeln

> **Update 2026-11-25:** Bronze/Silver/Gold ersetzt durch `ingestion.LoadPanel`: Rohdaten aus `data/raw/`, bereinigtes Panel im Speicher, Cache `data/processed/panel.parquet` (Neuaufbau mit `uv run python -m ingestion` oder `clean(refresh=True)`). Abschließende Rasterprüfung (vgl. DEC-011) erfolgt in `PanelCleaner._validate_grid`.

**Status:** Rekonstruiert

**Evidenzkategorie:** B

**Themenbereich:** Datenmanagement

**Entscheidung:**  
Bronze enthält die Exporte, Silver die zusammengeführte Auswahl, Gold die zugeschnittene und korrigierte Reihe. Silver wird bei bestehender Datei nicht ersetzt; Gold wird überschrieben.

**Kontext / Problemstellung:**  
Import und nachgelagerte Aufbereitung sind als getrennte Schritte angelegt.

**Alternativen:**  
C06 beauftragt und dokumentiert den Nichtüberschreibschutz eines bestehenden Panels. Ein weitergehendes Motiv nennt die Nutzeranweisung nicht. S13, Zeilen 70–74, diskutiert später Dateinamen mit Versionszeitstempel; diese Versionierung ist aktuell nicht umgesetzt.

**Begründung zum Entscheidungszeitpunkt:**  
Nicht dokumentiert.

**Mögliche wissenschaftliche Begründung:**  
Nachträglicher Begründungsansatz, zu prüfen: Stufen können Rohdaten und Analysebestand unterscheidbar machen; feste Dateinamen allein sichern keine Provenienz.

**Literaturgrundlage:**  
Keine spezifische Literatur vorhanden. Leitlinien zu Datenprovenienz und reproduzierbaren Datenpipelines recherchieren.

**Konkrete Umsetzung:**  
`save_df` beendet sich bei vorhandenem `data/silver/panel.csv`; `save_panel` schreibt `data/gold/panel.csv`. Ingestion arbeitet relativ zum Arbeitsverzeichnis, Loader/Writer relativ zum Projekt. Alte `raw`-/`processed`-Konstanten bleiben in `config.py`.

**Auswirkungen auf das Experiment:**  
Ein erneuter Import kann unbemerkt einen alten Silver-Bestand weiterverwenden. Überschreiben von Gold erschwert die Zuordnung zu früheren Auswertungen.

**Evidenz / Quellen im Projekt:**  
`ingestion/load_raw.py:59–66`; `common/loader.py:6–11`; `common/writer.py:6–9`; `config.py:7–10`; Commit `ce631ca`; C06, `messages[0,17]`; S13, S15.

**Offene Fragen:**  
Welcher Rohdatenstand gehört zu welchem Panel und Modelllauf? Soll eine Versions- oder Hashreferenz verbindlich werden?

**Relevanz für die Bachelorarbeit:**  
Implementierung; Reproduzierbarkeit.

---

### DEC-006: UTC und Intervallanfang als ausdrücklich vorläufige Quellannahmen

**Status:** Bestätigt

**Evidenzkategorie:** A

**Themenbereich:** Zeitachsen und Datenaufbereitung

**Entscheidung:**  
Naive `DateUTC`-Werte werden als UTC interpretiert; zeitzonenbewusste Werte werden nach UTC umgerechnet. Die Zeitstempel werden als Intervallanfänge behandelt.

**Kontext / Problemstellung:**  
Spaltenname, Intervallbeschriftung und historische CET/CEST-/Stundenende-Dokumentation ergeben keine abschließend geklärte Exportsemantik.

**Alternativen:**  
`Europe/Berlin`-Lokalisierung und pauschale Verschiebung um eine Stunde wurden in S16 diskutiert und wegen der konkreten Exportbefunde nicht empfohlen.

**Begründung zum Entscheidungszeitpunkt:**  
`README.md:12–15` nennt den Exportspaltennamen als Grundlage und kennzeichnet UTC als Annahme. S16, Assistentenzeile 67, verweist auf Übereinstimmung mit Intervallanfängen und den fehlenden Beweis einer Quellzeitzone.

**Mögliche wissenschaftliche Begründung:**  
Nachträglicher Begründungsansatz, zu prüfen: Ein regelmäßiges UTC-Raster erleichtert 24-/168-Stunden-Vergleiche. Regelmäßigkeit beweist die physische Zeitzuordnung nicht.

**Literaturgrundlage:**  
L3, Abschnitt 5.1, wurde geprüft; die historische Richtlinie ersetzt keine Definition der konkreten CSV-Spalten. Eine versionsbezogene Exportbeschreibung oder ein Referenzabgleich fehlt.

**Konkrete Umsetzung:**  
`normalize_dates` und `validate_source_fields` nutzen `pd.to_datetime(..., utc=True)`. Runner konvertieren anschließend mit `tz_convert(None)` in naive UTC.

**Auswirkungen auf das Experiment:**  
Eine falsche Zuordnung verschiebt Lags, Tagesgrenzen und saisonale Phasen. Naive UTC für sktime ist eine Darstellungsentscheidung nach UTC-Konvertierung, keine Umrechnung nach deutscher Ortszeit.

**Evidenz / Quellen im Projekt:**  
`README.md:12–15`; `preprocessing/data_cleaning.py:23–43`; `run_forecasting.py:22–23`; `run_benchmark.py:56–66`; S16, Zeilen 38,67,74; S32, Zeilen 97–158.

**Offene Fragen:**  
Bestätigt der Anbieter Zeitzone und Intervallbezug je Dateigeneration? Wie werden Ortszeit, Sommerzeit und Veröffentlichungsverzug fachlich behandelt?

**Relevanz für die Bachelorarbeit:**  
Datengrundlage; Zeitkonventionen; Limitationen.

---

### DEC-007: Sechs bekannte Zeitstempelkonflikte gezielt korrigieren

**Status:** Bestätigt

**Evidenzkategorie:** A

**Themenbereich:** Datenbereinigung

**Entscheidung:**  
Für sechs gelistete Frühjahrsdaten 2019–2024 wird `03:00` auf `02:00` korrigiert, wenn das Intervall `02:00–03:00` lautet. Lastwerte bleiben erhalten.

**Kontext / Problemstellung:**  
Je betroffenem Datum existieren zwei verschiedene Lastwerte unter `03:00`; `02:00` fehlt. Die Intervallspalten unterscheiden die Zeilen.

**Alternativen:**  
Löschen, Mitteln, Interpolieren und pauschale DST-Umdeutung wurden in S16 erörtert und nicht als geeignete Konfliktlösung übernommen.

**Begründung zum Entscheidungszeitpunkt:**  
S16, Assistentenzeile 67, begründet den Korrekturkandidaten mit dem Widerspruch zwischen `DateUTC` und den Intervallspalten; Nutzerzeile 74 autorisiert die entsprechende Pipeline.

**Mögliche wissenschaftliche Begründung:**  
Nachträglicher Begründungsansatz, zu prüfen: Eine eng begrenzte Regel erhält Messwerte und verhindert willkürliche Auswahl. Die Regel plausibilisiert den Export, bestätigt aber nicht unabhängig die UTC-Semantik.

**Literaturgrundlage:**  
L3 ist historischer Kontext, kein Beweis der sechs Korrekturen. Ein quellenunabhängiger Abgleich dieser Stunden ist noch erforderlich.

**Konkrete Umsetzung:**  
`CORRECTION_TIMESTAMPS`; `candidate = DateUTC.normalize() + TimeFrom`; nur bekannte Abweichungen erlaubt. Intervalllänge wird modulo eines Tages auf genau eine Stunde geprüft, einschließlich `23:00–00:00`.

**Auswirkungen auf das Experiment:**  
Zeitindex und saisonale Zuordnung ändern sich für sechs Beobachtungen. Unbekannte Konflikte lösen einen Fehler aus. Auditspalten werden intern erzeugt, aber derzeit nicht exportiert (DEC-012).

**Evidenz / Quellen im Projekt:**  
`preprocessing/data_cleaning.py:10–20,48–76`; Commit `ce631ca`; S16, Zeilen 67,74,94,116; R01 bestätigt die sechs Konflikte und die Reproduktion von Gold im Speicher.

**Offene Fragen:**  
Sind die sechs Zuordnungen extern bestätigt? Wie werden neu auftretende Konflikte untersucht und freigegeben?

**Relevanz für die Bachelorarbeit:**  
Datenaufbereitung; Fehlerkorrekturen und Zeitachse.

---

### DEC-008: Inklusives Analysefenster von Januar 2015 bis März 2026

**Status:** Rekonstruiert

**Evidenzkategorie:** B

**Themenbereich:** Datenfilterung

**Entscheidung:**  
Gold wird auf 2015-01-01 01:00 UTC bis 2026-03-31 23:00 UTC begrenzt, beide Grenzen eingeschlossen.

**Kontext / Problemstellung:**  
Silver beginnt bereits am 2014-12-31 23:00; zwei Beobachtungen liegen vor dem konfigurierten Beginn.

**Alternativen:**  
S16, Assistentenzeile 31, nennt den Beginn des deutschen Kalenderjahres als andere mögliche Grenze, ohne eine endgültige fachliche Auswahl zu belegen.

**Begründung zum Entscheidungszeitpunkt:**  
Nicht dokumentiert.

**Mögliche wissenschaftliche Begründung:**  
Nachträglicher Begründungsansatz, zu prüfen: Ein festes Fenster vereinfacht Vollständigkeitsprüfungen. Gerade die Startstunde 01:00 benötigt eine fachliche Erklärung.

**Literaturgrundlage:**  
Keine spezifische Literatur vorhanden; die Grenzauswahl benötigt primär eine dokumentierte fachliche Festlegung.

**Konkrete Umsetzung:**  
`START_DATETIME`, `END_DATETIME`; `filter_time_window` verwendet `between`, setzt den Index und sortiert.

**Auswirkungen auf das Experiment:**  
R01 findet 98.591 Gold-Zeilen und einen vollständigen Stundenindex. Zwei Stunden werden ausgeschlossen. Der konfigurierte Gesamtbestand ist von tatsächlich verwendeten Trainings- und Testfenstern zu unterscheiden.

**Evidenz / Quellen im Projekt:**  
`config.py:13–17`; `preprocessing/data_cleaning.py:79–88`; `tests/test_gold_panel.py:36–42,66–98`; Commit `8a55cf5`; S16, Zeilen 31,116; R01.

**Offene Fragen:**  
Warum beginnt die Reihe um 01:00? War das Ende datengetrieben oder vorab festgelegt? Ist eine frühere Grenze methodisch erforderlich?

**Relevanz für die Bachelorarbeit:**  
Datengrundlage; Ein- und Ausschlusskriterien.

---

### DEC-009: Lastwerte unverändert lassen; fehlende Werte als Fehler behandeln

**Status:** Rekonstruiert

**Evidenzkategorie:** B

**Themenbereich:** Datenbereinigung

**Entscheidung:**  
Die vorhandene Pipeline interpoliert oder mittelt keine Lastwerte. Fehlende und nicht endliche Werte werden abgewiesen; eine statistische Ausreißerbereinigung ist nicht implementiert.

**Kontext / Problemstellung:**  
Ungültige Messwerte und Zeitkonflikte sind von fachlich möglichen Lastspitzen zu unterscheiden.

**Alternativen:**  
S16 bespricht Interpolation nur für gegebenenfalls verbleibende echte Lücken; eine konkrete Imputationsmethode oder Ausreißerregel wurde nicht ausgewählt.

**Begründung zum Entscheidungszeitpunkt:**  
Nicht dokumentiert. Die README bestätigt das Verhalten, begründet aber keine allgemeine Ausreißerstrategie.

**Mögliche wissenschaftliche Begründung:**  
Nachträglicher Begründungsansatz, zu prüfen: Unveränderte Lasten vermeiden künstliche Glättung. Ungeprüfte Messausreißer könnten zugleich Training und Fehlermetriken beeinflussen.

**Literaturgrundlage:**  
L1 behandelt Evaluationsprobleme; eine spezifische, auf deutsche Lastmessungen bezogene Qualitäts- und Imputationsliteratur fehlt.

**Konkrete Umsetzung:**  
`validate_source_fields` prüft `isna` und `np.isfinite`; Runner prüfen nach `asfreq("h")` auf endliche Werte. Keine Winsorisierung, Ausreißerschwelle oder Lastnormalisierung in der Datenpipeline.

**Auswirkungen auf das Experiment:**  
Fehlende Zeitpunkte werden beim Runner sichtbar, statt durch Imputation verdeckt zu werden. Abwesenheit einer Ausreißerregel belegt keinen bewussten fachlichen Verzicht.

**Evidenz / Quellen im Projekt:**  
`preprocessing/data_cleaning.py:29–45,91–99`; `run_forecasting.py:28–31`; `run_benchmark.py:66–69`; `README.md:17–21`; S16, Zeile 31.

**Offene Fragen:**  
Wurden extreme, negative oder Nullwerte fachlich untersucht? Welche Regel gilt bei zukünftigen Lücken und ungültigen Zielwerten?

**Relevanz für die Bachelorarbeit:**  
Datenaufbereitung; Messqualität und Limitationen.

---

### DEC-010: Echte Duplikate einschließlich Zeitstempel prüfen; spätere Entfernung entfällt

**Status:** Bestätigt

**Evidenzkategorie:** A

**Themenbereich:** Datenbereinigung

**Entscheidung:**  
Historisch wurden exakte Zeilenduplikate einschließlich `DateUTC` geprüft und entfernt. Der aktuelle Bereinigungslauf enthält keine Duplikatentfernung mehr.

**Kontext / Problemstellung:**  
Ein früherer Test meldete 436 scheinbare Duplikate, weil nach Setzen des Datumsindex nur wiederholte Lastwerte geprüft wurden.

**Alternativen:**  
`panel.duplicated()` ohne Indexberücksichtigung wurde in S16 als ungeeignet erklärt; `panel.reset_index().duplicated()` ist dort die begründete Alternative.

**Begründung zum Entscheidungszeitpunkt:**  
S16, Assistentenzeile 31: Gleiche Lastwerte zu verschiedenen Zeitpunkten sind zulässig und dürfen nicht als identische Beobachtungen gelöscht werden.

**Mögliche wissenschaftliche Begründung:**  
Nachträglicher Begründungsansatz, zu prüfen: Ein fachlich vollständiger Beobachtungsschlüssel verhindert Informationsverlust. Zeitkonflikte mit verschiedenen Werten erfordern gesonderte Klärung.

**Literaturgrundlage:**  
Keine spezifische Literatur im Projekt. Datenqualitätsliteratur zur Unterscheidung von Schlüsselduplikaten und wiederholten Messwerten recherchieren.

**Konkrete Umsetzung:**  
`ce631ca:clean_panel` enthielt `drop_duplicates`. `ed2dee2` entfernt diesen Schritt; `876783d` entfernt den separaten Gold-Zeilenduplikat-Test. Der Gold-Zeitstempeltest bleibt bestehen.

**Auswirkungen auf das Experiment:**  
Die historischen 436 Meldungen belegen keine 436 zu löschenden Messungen. R01 findet aktuell keine exakten Silver-Zeilenduplikate; für veränderte Eingaben fehlt eine automatische Bereinigung.

**Evidenz / Quellen im Projekt:**  
S16, Nutzerzeile 9 und Assistentenzeile 31; `ce631ca`, `ed2dee2`, `876783d`; `tests/test_gold_panel.py:58–63`; R01.

**Offene Fragen:**  
War die Entfernung des Bereinigungsschritts beabsichtigt? Soll bei echten Duplikaten gelöscht oder abgebrochen werden?

**Relevanz für die Bachelorarbeit:**  
Datenaufbereitung; Duplikatdefinition und Qualitätsprüfung.

---

### DEC-011: Prüfungen vor dem Gold-Export wurden teilweise entfernt

**Status:** Rekonstruiert

**Evidenzkategorie:** B

**Themenbereich:** Datenvalidierung

**Entscheidung:**  
Der Stand `ce631ca` prüfte nach der Korrektur die vollständige und eindeutige Gold-Zeitachse. Seit `ed2dee2` wird Gold ohne diese abschließende Laufzeitprüfung geschrieben.

**Kontext / Problemstellung:**  
README und Docstring versprechen weiterhin vollständige Validierung; aktuelle Tests prüfen nur bei separatem Aufruf.

**Alternativen:**  
Das Beibehalten ausgelagerter Prüfungen wurde in S16 und S19 empfohlen. Warum stattdessen Teile entfallen sind, ist nicht dokumentiert.

**Begründung zum Entscheidungszeitpunkt:**  
Nicht dokumentiert. Der Wunsch nach verständlicherem Code ist in S19 belegt, aber kein Beleg für eine absichtliche methodische Abschwächung.

**Mögliche wissenschaftliche Begründung:**  
Nachträglicher Begründungsansatz, zu prüfen: Getrennte Tests können Qualität prüfen; sie ersetzen ohne verpflichtende Einbindung keine Exportbedingung.

**Literaturgrundlage:**  
Keine spezifische Literatur vorhanden. Reproduzierbare Datenvalidierung und ausführbare Datenverträge recherchieren.

**Konkrete Umsetzung:**  
`validate_gold`, Grenzvalidierung und `drop_duplicates` wurden entfernt. Pflichtfelder, endliche Lasten, Stundenraster und Intervallkonflikte werden weiterhin geprüft. Gold-Integrationstests kontrollieren Eindeutigkeit, Zeitraum und Vollständigkeit.

**Auswirkungen auf das Experiment:**  
Eine neue Lücke oder ein Duplikat könnte Gold erreichen, obwohl die README einen Abbruch zusagt. Für den derzeit vorhandenen Bestand bestehen die Datenprüfungen.

**Evidenz / Quellen im Projekt:**  
`preprocessing/data_cleaning.py:29–99`; `tests/test_gold_panel.py:45–107`; Diff `ed2dee2`; `README.md:10–28`; S16, Zeile 126; S19, Zeilen 22,32; R02.

**Offene Fragen:**  
Soll die vollständige Prüfung wieder verbindliche Exportbedingung werden? Welche README-Aussagen sollen gelten?

**Relevanz für die Bachelorarbeit:**  
Datenaufbereitung; Qualitätssicherung; Reproduzierbarkeit.

---

### DEC-012: Gold enthält nur Zeitstempel und Last; Audit bleibt nicht persistent

**Status:** Rekonstruiert

**Evidenzkategorie:** B

**Themenbereich:** Datenmanagement

**Entscheidung:**  
Exportiert werden ausschließlich `DateUTC` und `Value`; Intervallfelder, ursprüngliche Zeitstempel und Korrekturkennzeichen fehlen in Gold.

**Kontext / Problemstellung:**  
Die Korrekturfunktion erstellt Auditspalten, während README deren Aufbewahrung und den Erhalt der Intervallfelder beschreibt.

**Alternativen:**  
Die interne Aufbewahrung dieser Felder ist historisch dokumentiert; eine gesonderte Auditdatei ist nicht implementiert.

**Begründung zum Entscheidungszeitpunkt:**  
Nicht dokumentiert.

**Mögliche wissenschaftliche Begründung:**  
Nachträglicher Begründungsansatz, zu prüfen: Ein schmales Modellschema kann versehentliche Metadatenverwendung vermeiden. Das rechtfertigt ohne separate Ablage noch keinen Verlust der Korrekturprovenienz.

**Literaturgrundlage:**  
Keine spezifische Literatur im Projekt; Datenprovenienz und nachvollziehbare Transformationen recherchieren.

**Konkrete Umsetzung:**  
`main` selektiert vor `save_panel` genau zwei Spalten. `ce631ca` benannte sie beim Export noch in `timestamp`/`load` um; `ed2dee2` stellt die heutigen Feldnamen her. Schon im Commit `ce631ca` werden Auditfelder im letzten Exportschritt verworfen.

**Auswirkungen auf das Experiment:**  
Die Begründung von sechs Änderungen ist aus Gold allein nicht sichtbar. R01 bestätigt das Zweispaltenschema; die README weicht vom tatsächlichen Export ab.

**Evidenz / Quellen im Projekt:**  
`preprocessing/data_cleaning.py:73–75,98–99`; `common/writer.py:6–9`; `README.md:17–25`; Commits `ce631ca`, `ed2dee2`; R01.

**Offene Fragen:**  
Soll ein separater Auditbestand erhalten bleiben? Wurde ein historisch erzeugtes Panel mit Auditspalten dauerhaft archiviert?

**Relevanz für die Bachelorarbeit:**  
Datenaufbereitung; Reproduzierbarkeit.

---

### DEC-013: Saisonalität mit zeitlichen Mittelwertprofilen explorieren

**Status:** Rekonstruiert

**Evidenzkategorie:** B

**Themenbereich:** Explorative Analyse

**Entscheidung:**  
Monats-, Wochentags- und Stundenprofile werden nach Jahr getrennt als arithmetische Lastmittel visualisiert.

**Kontext / Problemstellung:**  
Die EDA untersucht wiederkehrende zeitliche Struktur der Lastreihe.

**Alternativen:**  
Nicht dokumentiert.

**Begründung zum Entscheidungszeitpunkt:**  
Nicht dokumentiert. S01 fordert die zusätzlichen Wochen- und Tagesplots, nennt aber keine Begründung der Aggregation oder der Jahresaufteilung.

**Mögliche wissenschaftliche Begründung:**  
Nachträglicher Begründungsansatz, zu prüfen: Profile können zeitliche Struktur sichtbar machen. Mittelwerte verdecken die Streuung und gewichten unterschiedlich vollständig beobachtete Gruppen verschieden.

**Literaturgrundlage:**  
Keine konkrete Literatur für diese Plotwahl im Projekt; Literatur zur explorativen Analyse saisonaler Zeitreihen recherchieren.

**Konkrete Umsetzung:**  
`plot_yearly_seasonality`, `plot_weekly_seasonality`, `plot_daily_seasonality`: `dropna`, `groupby`, `mean`. Kalenderfelder entstehen im Notebook; Zufallsseed 42 steuert nur Farben im Jahresplot.

**Auswirkungen auf das Experiment:**  
Diese Aggregation verändert nicht die stündliche Modellzielreihe. Das Jahr 2026 umfasst nur Januar bis März; ein Jahresvergleich ist entsprechend unvollständig. Die EDA umfasst auch spätere Auswertungsdaten.

**Evidenz / Quellen im Projekt:**  
`eda/utils.py:9–148`; `eda/eda.ipynb`, Zellen 4–8, IDs `588b64a9` bis `89bb4ba6`; Commits `f529db2`, `ed2dee2`; S01, Nutzerzeilen 9,51,92.

**Offene Fragen:**  
Welche EDA-Auswertungen sollen nur Trainingsdaten betreffen? Sollen Streuung und Stichprobenzahlen neben Profilmitteln berichtet werden?

**Relevanz für die Bachelorarbeit:**  
Explorative Datenanalyse; saisonale Struktur.

---

### DEC-014: ADF mit AIC-Lagauswahl und explorativer Schwelle 0,05

**Status:** Rekonstruiert

**Evidenzkategorie:** B

**Themenbereich:** Explorative Statistik

**Entscheidung:**  
Die Rohlastreihe wird per Augmented-Dickey-Fuller-Test mit `autolag="AIC"` untersucht; der Code gibt bei p < 0,05 die Bezeichnung `Stationary` aus. ACF/PACF werden ergänzend geplottet.

**Kontext / Problemstellung:**  
Die Entwicklung diskutiert Stationarität und die Wahl von ARIMA-Strukturen.

**Alternativen:**  
Tests auf saisonale Einheitswurzeln wurden in S01, Nutzerzeile 191, nachgefragt; eine Umsetzung ist nicht nachgewiesen.

**Begründung zum Entscheidungszeitpunkt:**  
Nicht dokumentiert.

**Mögliche wissenschaftliche Begründung:**  
Nachträglicher Begründungsansatz, zu prüfen: Ein Einheitswurzeltest kann einen Aspekt der Zeitreihenstruktur untersuchen. Eine Ablehnung ersetzt keine Prüfung saisonaler Struktur, Strukturbrüche oder Modellresiduen.

**Literaturgrundlage:**  
Keine überprüfte Originalquelle zum ADF-Test im Projekt. Testannahmen, deterministische Terme, Lagwahl und Interpretation recherchieren; nicht aus dem Text `Stationary` eine umfassende Eigenschaft ableiten.

**Konkrete Umsetzung:**  
`check_stationarity` ruft `adfuller` ohne weitere explizite Testparameter auf; `identifying_model_parameters` nutzt ACF/PACF-Defaults.

**Auswirkungen auf das Experiment:**  
Gespeichert sind ADF = −21,230530745378385 und p-Ausgabe 0,0. Dies sind Notebookausgaben ohne Laufdatum; 0,0 ist kein Beleg einer mathematisch exakt null betragenden Wahrscheinlichkeit. Daraus folgt keine belegte Auswahl von DHR `d=0`.

**Evidenz / Quellen im Projekt:**  
`eda/utils.py:151–162`; `eda/eda.ipynb`, Zelle 9, ID `5aedcc15`, und Zelle 10; S01, Nutzerzeile 180; S23, Nutzerzeilen 72,89.

**Offene Fragen:**  
Welche Testoptionen und Datenversion gelten? Wurden Residuen und saisonale Einheitswurzeln geprüft? Wann entstanden die gespeicherten Ausgaben?

**Relevanz für die Bachelorarbeit:**  
EDA; statistische Diagnostik und Einschränkungen.

---

### DEC-015: Additive Tageszerlegung und robuste MSTL nur explorativ verwenden

**Status:** Rekonstruiert

**Evidenzkategorie:** B

**Themenbereich:** Explorative Analyse

**Entscheidung:**  
Das Notebook nutzt eine additive Zerlegung mit Periode 24 und eine robuste MSTL mit Perioden 24 und 168.

**Kontext / Problemstellung:**  
Mehrere saisonale Komponenten werden in der Entwicklung untersucht.

**Alternativen:**  
Additive und multiplikative Modellbegriffe werden in S20 angesprochen; ein dokumentierter empirischer Variantenvergleich fehlt.

**Begründung zum Entscheidungszeitpunkt:**  
Nicht dokumentiert.

**Mögliche wissenschaftliche Begründung:**  
Nachträglicher Begründungsansatz, zu prüfen: Mehrere Perioden können getrennte zeitliche Muster untersuchen. Die Angemessenheit additiver Komponenten ist anhand der Lastreihe zu prüfen.

**Literaturgrundlage:**  
L2 nennt komplexe Saisonalität; eine im Projekt belegte spezifische MSTL-Referenz fehlt und sollte recherchiert werden.

**Konkrete Umsetzung:**  
`seasonal_decompose(..., model="additive", period=24)`; Darstellung eines Ausschnitts ab Zeile 24 für 14 Tage; `MSTL(periods=(24,168), stl_kwargs={"robust":True})`.

**Auswirkungen auf das Experiment:**  
Die Zerlegungen werden auf dem gesamten geladenen Gold-Bestand durchgeführt. Sie gehen aktuell nicht als Modellmerkmale ein. Eine spätere Übernahme zentrierter oder vollstichprobenbasierter Komponenten wäre gesondert auf Zukunftsinformation zu prüfen.

**Evidenz / Quellen im Projekt:**  
`eda/eda.ipynb`, Zellen 11–14, IDs `78ca3b7f`, `69612312`, `7eacca70`, `747f68f1`; S20, Nutzerzeilen 49,59,76; Commit `7c0184a`.

**Offene Fragen:**  
Wurden Perioden vor Sichtung späterer Testdaten bestimmt? Soll die Zerlegung nur beschreibend bleiben? Welche genaue MSTL-Konfiguration und Referenz gelten?

**Relevanz für die Bachelorarbeit:**  
EDA; Saisonanalyse; Abgrenzung von Modellvorverarbeitung.

---

### DEC-016: DHR mit ARIMA-Fehlern gegen XGBoost vergleichen; separates ARIMA ausschließen

**Status:** Rekonstruiert

**Evidenzkategorie:** B

**Themenbereich:** Auswahl der Vergleichsverfahren

**Entscheidung:**  
Der fachliche Vergleich betrifft DHR mit ARIMA-Fehlern und Gradient Boosting mit XGBoost. Ein zusätzliches klassisches ARIMA wurde ausdrücklich aus dem Vergleich genommen.

**Kontext / Problemstellung:**  
S23 klärt, welche Verfahren und Prognosehorizonte die gewünschte Vergleichsdatei umfassen soll; S25 diskutiert einen passenden Arbeitstitel.

**Alternativen:**  
Klassisches ARIMA wurde zuerst angefragt und anschließend ausdrücklich ausgeschlossen.

**Begründung zum Entscheidungszeitpunkt:**  
Nicht dokumentiert. Die Nutzerentscheidung zum Ausschluss ist belegt, ihre fachliche Begründung fehlt.

**Mögliche wissenschaftliche Begründung:**  
Nachträglicher Begründungsansatz, zu prüfen: Zwei strukturell verschiedene Modellfamilien erlauben einen begrenzten Vergleich saisonaler Modellierung. Ein einzelner Vertreter rechtfertigt keine Aussage über alle Boosting- oder statistischen Verfahren.

**Literaturgrundlage:**  
L2 zur DHR-Modellfamilie ist vorhanden; eine überprüfte grundlegende XGBoost-Publikation sowie Lastprognose-Vergleichsliteratur fehlen.

**Konkrete Umsetzung:**  
Zwei eigene Modellklassen; der Benchmarkentwurf ergänzt saisonale Naivmodelle, keine separate reine ARIMA-Klasse.

**Auswirkungen auf das Experiment:**  
`modeling/dynamic_harmonic_regression.py`; `modeling/gradient_boosting.py`; `run_benchmark.py:76–93`; S23, Nutzerzeilen 9,45; S25, Nutzerzeile 9.

**Evidenz / Quellen im Projekt:**  
Warum diese zwei Verfahren? Welche Forschungsfrage und welche Reichweite sollen die Schlussfolgerungen haben? Ist der Titel aus S25 verbindlich?

**Offene Fragen:**  
Theoretische Grundlagen; Auswahl der Vergleichsverfahren.

**Relevanz für die Bachelorarbeit:**  
undefined

---

### DEC-017: Univariate Modelle ohne zusätzliche Wetter- oder Kalenderregressoren

**Status:** Rekonstruiert

**Evidenzkategorie:** B

**Themenbereich:** Informationsbasis der Modelle

**Entscheidung:**  
Die Runner übergeben nur `Value`. Beide Modellklassen deklarieren `capability:exogenous=False`. DHR verwendet intern aus Zeitstempeln berechnete Fourier-Regressoren.

**Kontext / Problemstellung:**  
Die Eingabe ist eine einzelne stündliche Lastreihe.

**Alternativen:**  
S35 schlägt Fourier-/Kalendermerkmale für XGBoost vor; sie sind im aktuellen Modell nicht umgesetzt. Wetter und Arbeitstage erscheinen im verlinkten Lehrbuchbeispiel, aber nicht als belegte Projektoption.

**Begründung zum Entscheidungszeitpunkt:**  
Nicht dokumentiert.

**Mögliche wissenschaftliche Begründung:**  
Nachträglicher Begründungsansatz, zu prüfen: Univariate Eingaben erleichtern einen Vergleich ohne ungesicherte zukünftige Wetterdaten. Gleiche Rohdaten bedeuten dennoch keine identische Merkmalsbasis.

**Literaturgrundlage:**  
L2 ist Modellkontext, keine Begründung für das Weglassen zusätzlicher Einflussgrößen. Vergleichsliteratur zu univariater und multivariater Lastprognose recherchieren.

**Konkrete Umsetzung:**  
`Value` als `pd.Series`; XGBoost nutzt fünf Lastmerkmale, DHR Zeitbasisfunktionen. Keine Feiertags-, Temperatur- oder Jahresperiodenmerkmale implementiert.

**Auswirkungen auf das Experiment:**  
Unterschiede umfassen Modellfamilie und Repräsentation. Ein Kausalurteil über den Effekt der Modellfamilie allein wäre zu weitgehend. Fehlende Jahressaisonalität oder Feiertage können die Fehlerstruktur beeinflussen.

**Evidenz / Quellen im Projekt:**  
`run_forecasting.py:19–20`; `run_benchmark.py:58,76–93`; `modeling/gradient_boosting.py:8–13,72–88`; `modeling/dynamic_harmonic_regression.py:14–19,38–61`; S35, Assistentenzeilen 46,70.

**Offene Fragen:**  
Ist univariate Prognose bewusst der Forschungsrahmen? Werden Merkmalsunterschiede als Teil der Verfahren oder als kontrollierte Bedingung behandelt?

**Relevanz für die Bachelorarbeit:**  
Modellierung; Vergleichbarkeit und Grenzen.

---

### DEC-018: XGBoost-Lags 24, 48 und 168 statt kurzer Zielstunden-Lags

**Status:** Bestätigt

**Evidenzkategorie:** A

**Themenbereich:** Feature Engineering

**Entscheidung:**  
Die realisierten Lagmerkmale sind die Lasten 24, 48 und 168 Stunden vor der jeweiligen Zielstunde; die zunächst diskutierten Lags 1 und 2 entfallen.

**Kontext / Problemstellung:**  
Ursprünglich sollten 24 Zielstunden am Tageswechsel gemeinsam vorhergesagt werden.

**Alternativen:**  
S21, Nutzerzeile 9, fordert zunächst Lags 1,2,24,48,168; Nutzerzeile 70 und Assistentenzeile 73 behandeln das Weglassen kurzer Lags.

**Begründung zum Entscheidungszeitpunkt:**  
S21, Assistentenzeile 73, erklärt, dass kurze, relativ zur Zielstunde gebildete Lags für spätere Tagesstunden am gemeinsamen Prognosestart noch unbekannt wären. Die fünf verbleibenden Merkmale werden in Nutzerzeile 80 beauftragt.

**Mögliche wissenschaftliche Begründung:**  
Nachträglicher Begründungsansatz, zu prüfen: Tages- und Wochenlags können bekannte Lastmuster repräsentieren. Nach Wechsel zur stündlichen Rekursion könnten kurze Lags wieder zulässig sein; ihre weitere Auslassung ist nicht neu begründet.

**Literaturgrundlage:**  
Keine geprüfte Lastprognosequelle für genau diese Lags im Projekt. Fachliteratur zur Lagwahl und zur Informationsverfügbarkeit bei Mehrschrittprognosen recherchieren.

**Konkrete Umsetzung:**  
`_build_lag_features` berechnet Quellzeitpunkte per `Timedelta` und ordnet mit `reindex` zu; damit sind es Zeit- statt bloßer Zeilenabstände.

**Auswirkungen auf das Experiment:**  
Innerhalb eines längeren Forecasts stammen einzelne Lagwerte ab späteren Tagen aus eigenen Prognosen. Die aktuelle Featuremenge ist kein Nachweis einer optimalen Auswahl.

**Evidenz / Quellen im Projekt:**  
`modeling/gradient_boosting.py:39–50`; `tests/modeling/test_gradient_boosting.py:43–57`; `7c0184a`; S21, Zeilen 9,70–104.

**Offene Fragen:**  
Sollen die Lags nach dem Strategiewechsel erneut validiert werden? Werden Merkmalsvarianten auf einer getrennten Validierung verglichen?

**Relevanz für die Bachelorarbeit:**  
Modellierung; XGBoost-Merkmale.

---

### DEC-019: Gleitende Mittelwerte am Ende des Vortags fixieren

**Status:** Bestätigt

**Evidenzkategorie:** A

**Themenbereich:** Feature Engineering

**Entscheidung:**  
`ma_24` und `ma_168` enden jeweils um 23:00 des UTC-Vortags der Zielstunde. Innerhalb eines Zieltages sind sie identisch.

**Kontext / Problemstellung:**  
Die ursprüngliche Tagesprognose durfte ausschließlich am Tageswechsel verfügbare Lasten verwenden.

**Alternativen:**  
S35 diskutiert stündlich aktualisierte rückwärtsgerichtete Mittelwerte ausdrücklich als zusätzliche Modellvariante; diese Variante ist nicht implementiert.

**Begründung zum Entscheidungszeitpunkt:**  
S21, Assistentenzeilen 73,93, erklärt die gleiche Informationsbasis aller 24 Tagesstunden und die Verfügbarkeit vor Tagesbeginn. Die Umsetzung folgt diesem Entwurf.

**Mögliche wissenschaftliche Begründung:**  
Nachträglicher Begründungsansatz, zu prüfen: Eine feste Tagesbasis verhindert unzulässige Verwendung wahrer intratäglicher Zielwerte im damaligen Tagesmodell. Für das heutige rekursive Ein-Modell-Verfahren kann die Fixierung unnötig Informationen auslassen.

**Literaturgrundlage:**  
Keine projektspezifische Literatur zur Wahl dieser Fensterdefinition. Mehrschrittstrategien und zeitkonsistente Aggregatmerkmale recherchieren.

**Konkrete Umsetzung:**  
`last_observed_times = target_times.normalize() - 1h`; `rolling(window, min_periods=window).mean()`; anschließend Zuordnung an diesen Endzeiten.

**Auswirkungen auf das Experiment:**  
Dies sind keine zu jeder Zielstunde neu endenden Mittelwerte. Spätere Prognosetage können prognostizierte Werte enthalten. Training und Prognose nutzen dieselbe Berechnungsfunktion.

**Evidenz / Quellen im Projekt:**  
`modeling/gradient_boosting.py:52–70`; `tests/modeling/test_gradient_boosting.py:60–73`; S21, Zeilen 73,93,104; S35, Assistentenzeilen 46,56,70.

**Offene Fragen:**  
Soll die Tagesfixierung beibehalten werden? Sind Prognosestarts immer an UTC-Tagesgrenzen vorgesehen?

**Relevanz für die Bachelorarbeit:**  
Modellierung; Aggregatmerkmale und Informationsverfügbarkeit.

---

### DEC-020: Trainingszeilen mit unvollständigen Features ausschließen

**Status:** Bestätigt

**Evidenzkategorie:** A

**Themenbereich:** Trainingsdatenaufbereitung

**Entscheidung:**  
Nur Zeilen mit vollständigen Merkmalswerten und vorhandenem Zielwert gelangen ins XGBoost-Training.

**Kontext / Problemstellung:**  
Die ersten Stunden eines Trainingsfensters besitzen noch keine ausreichend lange Vorgeschichte für Wochenlag und Wochenmittel.

**Alternativen:**  
S32 diskutiert die Trennung zwischen Entfernen unvollständiger Trainingszeilen und dem Bewahren zukünftiger Prognosezeilen.

**Begründung zum Entscheidungszeitpunkt:**  
S32, Nutzerzeile 33, nennt fehlende Historie ausdrücklich als Grund, anfängliche NaN-Zeilen im Training zu entfernen.

**Mögliche wissenschaftliche Begründung:**  
Nachträglicher Begründungsansatz, zu prüfen: Der Ausschluss vermeidet Training mit unvollständiger Merkmalsbasis. Er verkürzt das effektive Training gegenüber der an den Splitter übergebenen Datenmenge.

**Literaturgrundlage:**  
Keine konkrete Literatur zu dieser Warm-up-Regel vorhanden. Literatur zur gemeinsamen Informationsbasis in Modellvergleichen recherchieren.

**Konkrete Umsetzung:**  
`valid_rows = features.notna().all(axis=1) & y.notna()`; Fehler bei leerem Training. Die Tagesfixierung kann neben 168 Stunden weitere Anfangsstunden ausschließen, abhängig vom Fensterbeginn.

**Auswirkungen auf das Experiment:**  
Bei identischer übergebener Historie verwendet XGBoost weniger Zielbeispiele als DHR. Die Regel sollte keine fehlenden Messwerte im Inneren der Reihe verdecken; Runner prüfen diese zuvor.

**Evidenz / Quellen im Projekt:**  
`modeling/gradient_boosting.py:90–103`; `run_forecasting.py:28–31`; S32, Nutzerzeilen 12,33; `c95e29f`.

**Offene Fragen:**  
Wie groß ist die effektive Trainingsstichprobe je Fenster? Werden Warm-up-Unterschiede berichtet? Welche Mindesthistorie wird verbindlich gefordert?

**Relevanz für die Bachelorarbeit:**  
Modelltraining; Vergleichbarkeit.

---

### DEC-021: Von 24 Stundenmodellen zur rekursiven Prognose mit einem XGBoost-Modell

**Status:** Rekonstruiert

**Evidenzkategorie:** B

**Themenbereich:** Prognosestrategie

**Entscheidung:**  
Historisch wurden 24 Modelle nach Zieluhrzeit trainiert; später wurden sieben Tagesblöcke rekursiv verkettet. Seit `c95e29f` trainiert ein Modell über alle Stunden und prognostiziert stündlich rekursiv bis zum größten angeforderten Lead.

**Kontext / Problemstellung:**  
Die sktime-Migration ändert neben der Schnittstelle auch die Modellarchitektur.

**Alternativen:**  
24 Modelle nach Tagesstunde, 24/168 direkte Modelle nach Lead und ein gemeinsames rekursives Modell wurden in S21, S32 und S34–S36 diskutiert.

**Begründung zum Entscheidungszeitpunkt:**  
Nicht dokumentiert. Der Nutzer wünscht in S35 eine rekursive sktime-Lösung; eine explizite fachliche Begründung, warum die 24 Stundenmodelle aufgegeben wurden, fehlt.

**Mögliche wissenschaftliche Begründung:**  
Nachträglicher Begründungsansatz, zu prüfen: Gemeinsames Training kann Daten über Uhrzeiten teilen; Rekursion ermöglicht variable Horizonte. Vorhersagefehler können sich zugleich fortpflanzen.

**Literaturgrundlage:**  
Keine geprüfte Quelle zur direkten, rekursiven und hybriden Mehrschrittprognose im Projekt. Ein Vergleich dieser Strategien und grundlegende XGBoost-Literatur fehlen.

**Konkrete Umsetzung:**  
`_fit` erzeugt `model_`; `_predict` schreibt jeden vorhergesagten Wert in eine temporäre Historie. Sparse Horizonte werden durch Berechnung aller Zwischenstunden bedient. Aktuell gibt es keine XGBoost-Fouriermerkmale.

**Auswirkungen auf das Experiment:**  
Frühere Ergebnisse mit 24 Stundenmodellen sind nicht demselben Verfahren zuzuordnen. Der vorhandene Trainingstest erwartet noch `model.models` und scheitert; dies ist kein Nachweis eines Scheiterns des aktuellen Fits.

**Evidenz / Quellen im Projekt:**  
`7c0184a:modeling/gradient_boosting.py`; Diff `33fdffd`; Diff `c95e29f`; aktuell `modeling/gradient_boosting.py:105–157`; S21, S32, S34–S36; R02.

**Offene Fragen:**  
Welche Strategie ist das finale Vergleichsverfahren? Soll der Strategiewechsel selbst untersucht werden? Welche Informationsverfügbarkeit gilt für längere Horizonte?

**Relevanz für die Bachelorarbeit:**  
Modellierung; Mehrschrittstrategie; Entwicklung der Implementierung.

---

### DEC-022: Feste XGBoost-Hyperparameter und quadratische Trainingszielfunktion

**Status:** Rekonstruiert

**Evidenzkategorie:** B

**Themenbereich:** Modellkonfiguration

**Entscheidung:**  
XGBoost trainiert mit 200 Bäumen, Lernrate 0,05, Tiefe 4, Subsample 0,8, Colsample 0,8, `reg:squarederror`, `tree_method="hist"` und standardmäßig Seed 42.

**Kontext / Problemstellung:**  
Der aktuelle Konstruktor stellt Parameter bereit; der Benchmarkentwurf ändert die Seeds.

**Alternativen:**  
Keine belegte Suche oder ausgewertete Hyperparameteralternative. S38 bespricht zeitliche Parameterwahl, aber belegt keine abgeschlossene Optimierung.

**Begründung zum Entscheidungszeitpunkt:**  
Nicht dokumentiert.

**Mögliche wissenschaftliche Begründung:**  
Nachträglicher Begründungsansatz, zu prüfen: Diese Einstellungen können eine Ausgangskonfiguration bilden. Ihre Güte und das Rechenbudget müssten auf einer geeigneten Validierung beurteilt werden.

**Literaturgrundlage:**  
Grundlegende XGBoost-Publikation, Regularisierung und zeitliche Hyperparameteroptimierung noch recherchieren. Keine belastbare Begründung genau dieser Zahlen vorhanden.

**Konkrete Umsetzung:**  
`XGBRegressor` wird mit den genannten Einstellungen instanziiert. `n_lags=12`, `period=12`, `K=3` stehen zwar im Konstruktor, beeinflussen aber im aktuellen Code keine Features.

**Auswirkungen auf das Experiment:**  
Inaktive Parameter könnten eine wirkungslose Parametersuche erzeugen. Die quadratische Trainingszielfunktion ist von der später als primär vorgesehenen MAE-Auswertung zu unterscheiden.

**Evidenz / Quellen im Projekt:**  
`modeling/gradient_boosting.py:15–35,39–88,105–115`; Einführung der Defaults in `c95e29f`; S38, Nutzerzeile 173.

**Offene Fragen:**  
Woher stammen die Zahlen? Welches Suchbudget gilt für beide Verfahren? Welche Parameter dürfen tatsächlich variiert werden?

**Relevanz für die Bachelorarbeit:**  
Implementierung; Hyperparameterwahl und Validierung.

---

### DEC-023: DHR als Fourier-Regression mit nicht saisonalen ARIMA-Fehlern

**Status:** Bestätigt

**Evidenzkategorie:** A

**Themenbereich:** Statistisches Vergleichsverfahren

**Entscheidung:**  
DHR kombiniert Fourier-Regressoren für Tages- und Wochenperioden mit einem nicht saisonalen ARIMA-Fehlerprozess.

**Kontext / Problemstellung:**  
Die Lastreihe besitzt im Projekt untersuchte Tages- und Wochenstruktur; kurzfristige Dynamik soll zusätzlich modelliert werden.

**Alternativen:**  
Das separat verglichene klassische ARIMA wurde verworfen (DEC-016). Eine empirisch geprüfte Alternative zur DHR-Formulierung ist nicht belegt.

**Begründung zum Entscheidungszeitpunkt:**  
S22, Assistentenzeile 32, erklärt ausdrücklich: Fourier-Terme beschreiben wiederkehrende Lastmuster, ARIMA-Fehler kurzfristige Abhängigkeiten; Nutzerzeile 39 beauftragt diese Idee.

**Mögliche wissenschaftliche Begründung:**  
Nachträglicher Begründungsansatz, zu prüfen: Die Trennung saisonaler Basis und Fehlerdynamik erlaubt eine kompakte Spezifikation. Ob sie die deutsche Last ausreichend abbildet, bleibt empirisch offen.

**Literaturgrundlage:**  
L2, im Projektcode und S22 referenziert und erneut geprüft. Es ist ein Modellrahmen, kein Beleg optimaler deutscher Lastprognosen.

**Konkrete Umsetzung:**  
`SARIMAX(..., exog=Fourier, order=self.order, seasonal_order=(0,0,0,0), trend="n")`; Konstante als expliziter Regressor bei `d=0`.

**Auswirkungen auf das Experiment:**  
Die Koeffizienten bleiben zwischen Fits fest. Gemeint ist keine beliebige Variante mit zeitvariierenden Fourier-Koeffizienten. DHR besitzt intern exogene Zeitbasisfunktionen, verlangt aber keine externen Eingangsreihen.

**Evidenz / Quellen im Projekt:**  
`modeling/dynamic_harmonic_regression.py:1–10,38–99`; S22, Zeilen 32,39; `876783d` als erster Commit dieser Klasse; Migration `f1d64b3`.

**Offene Fragen:**  
Ist diese DHR-Definition im Theorieteil eindeutig? Welche Residuenstruktur bleibt nach dem Fit? Welche Parameterwahl ist final?

**Relevanz für die Bachelorarbeit:**  
Modellgrundlagen; DHR mit ARIMA-Fehlern.

---

### DEC-024: Feste Fourier-Phase, eindeutige Frequenzen und Nyquist-Sonderfall

**Status:** Bestätigt

**Evidenzkategorie:** A

**Themenbereich:** Saisonale Repräsentation

**Entscheidung:**  
Die Fourier-Phase basiert auf Stunden seit 2000-01-01 UTC. Gleiche Frequenzen werden dedupliziert; bei Frequenz 0,5 entfällt der auf dem Stundenraster verschwindende Sinusterm.

**Kontext / Problemstellung:**  
Verschiedene Trainingsfenster sollen dieselbe Zeitbasis nutzen; überlappende harmonische Frequenzen dürfen keine redundanten Spalten erzeugen.

**Alternativen:**  
Keine ausdrücklich getestete alternative Basis. Ein Neustart der Phase je Fenster wird in S39 als zu vermeidende Änderung diskutiert.

**Begründung zum Entscheidungszeitpunkt:**  
S22 dokumentiert stabile Phase und Frequenzbereinigung; S39, Assistentenzeile 77, erklärt deren Erhalt. Der Codekommentar erklärt den Nyquist-Sonderfall ausdrücklich.

**Mögliche wissenschaftliche Begründung:**  
Nachträglicher Begründungsansatz, zu prüfen: Eine feste Referenz erleichtert konsistente Interpretation über Fits; das Entfernen identischer Frequenzen vermeidet redundante Regressoren.

**Literaturgrundlage:**  
L2 ist die vorhandene allgemeine Modellgrundlage. Für konkrete numerische Toleranzen und Identifizierbarkeit fehlt eine gesonderte Herleitung.

**Konkrete Umsetzung:**  
`hours`, `np.remainder`, `np.isclose(rtol=1e-12, atol=1e-15)`; Standardperioden 24/168 mit je drei Harmonischen erzeugen zwölf Sinus-/Kosinusspalten plus Konstante.

**Auswirkungen auf das Experiment:**  
Die zusätzlichen Harmonischen sind Oberwellen derselben zwei Grundperioden. Die Frequenzbereinigung ist implementiert; ursprüngliche spezielle DHR-Tests sind heute nicht mehr vorhanden.

**Evidenz / Quellen im Projekt:**  
`modeling/dynamic_harmonic_regression.py:38–61,70–82`; S22, Assistentenzeile 55; S26, Nutzerzeilen 45,55; S39, Assistentenzeile 77; `f1d64b3`.

**Offene Fragen:**  
Werden Perioden/Harmonische vollständig validiert? `zip` kann ungleich lange Parameterlisten still verkürzen. Welche Regressionstests sollen erhalten bleiben?

**Relevanz für die Bachelorarbeit:**  
Modellimplementierung; Fourier-Merkmale.

---

### DEC-025: DHR-Zielwerte mit trainingsabhängigem Maximum skalieren

**Status:** Bestätigt

**Evidenzkategorie:** A

**Themenbereich:** Numerische Modellschätzung

**Entscheidung:**  
DHR teilt die Last durch `max(max(abs(y_train)),1)` und skaliert Vorhersagen anschließend zurück.

**Kontext / Problemstellung:**  
Die Optimierung arbeitet auf relativ großen Lastwerten.

**Alternativen:**  
Nicht dokumentiert.

**Begründung zum Entscheidungszeitpunkt:**  
Der Kommentar `Scaling improves optimization for load values measured in MW` nennt die beabsichtigte numerische Verbesserung ausdrücklich.

**Mögliche wissenschaftliche Begründung:**  
Nachträglicher Begründungsansatz, zu prüfen: Größenanpassung kann numerische Probleme reduzieren. Ein gemessener Vorteil oder eine Konvergenzgarantie ist damit nicht belegt.

**Literaturgrundlage:**  
Keine eigene geprüfte Quelle zur Skalierungsregel im Projekt; numerische SARIMAX-Schätzung und Skalierung recherchieren.

**Konkrete Umsetzung:**  
`scale_` wird nur aus dem jeweils an `_fit` übergebenen `y` berechnet; `_predict` multipliziert mit demselben Faktor. XGBoost besitzt diese Skalierung nicht.

**Auswirkungen auf das Experiment:**  
Die konkrete Umsetzung benutzt keine Zukunftswerte für den Skalierungsfaktor. Die Datenpipeline selbst bleibt unskaliert, und die Fehlerauswertung erfolgt nach Rücktransformation.

**Evidenz / Quellen im Projekt:**  
`modeling/dynamic_harmonic_regression.py:86–99,120–124`; historisch bereits `876783d`; S39, Assistentenzeile 42.

**Offene Fragen:**  
Wurde die Wirkung auf Konvergenz gemessen? Ist die MW-Einheit durch den konkreten Export bestätigt?

**Relevanz für die Bachelorarbeit:**  
Implementierung; numerische Schätzung und Leakage-Vermeidung.

---

### DEC-026: DHR-Startkonfiguration mit je drei Harmonischen und ARIMA(1,0,1)

**Status:** Rekonstruiert

**Evidenzkategorie:** B

**Themenbereich:** Modellkonfiguration

**Entscheidung:**  
Standardwerte sind `periods=(24,168)`, `harmonics=(3,3)`, `order=(1,0,1)`, `maxiter=200` und nominell `minimum_history=168`.

**Kontext / Problemstellung:**  
Das Projekt benötigt eine erste schätzbare DHR-Konfiguration.

**Alternativen:**  
S26 und S38–S39 diskutieren Harmonischenwahl, ARIMA-Ordnung, kürzere Trainingsfenster und geringere Iterationsgrenzen. Eine abgeschlossene Parameterauswahl ist nicht belegt.

**Begründung zum Entscheidungszeitpunkt:**  
Nicht dokumentiert. S22 bezeichnet die Werte ausdrücklich als später zu validierende Startwerte; das erklärt keine optimale Zahl.

**Mögliche wissenschaftliche Begründung:**  
Nachträglicher Begründungsansatz, zu prüfen: Eine begrenzte Basis kann Modellkomplexität und Aufwand beschränken. Genau drei Harmonische und ARIMA(1,0,1) benötigen empirische oder fachliche Begründung.

**Literaturgrundlage:**  
L2 erläutert den Modellrahmen; genaue Parameter sind projektspezifisch und nicht durch das dortige Stromlastbeispiel vorgegeben.

**Konkrete Umsetzung:**  
`model.fit(disp=False,maxiter=self.maxiter)`; `minimum_history` wird gespeichert, aber nicht geprüft. Eine explizite Auswertung von `mle_retvals` oder eine Abbruchregel bei Nichtkonvergenz fehlt.

**Auswirkungen auf das Experiment:**  
200 ist eine Obergrenze, keine gemessene Iterationszahl. Die derzeitige Parameterspezifikation und das Fehlen einer Konvergenzregel begrenzen die Verlässlichkeit eines späteren Vergleichs.

**Evidenz / Quellen im Projekt:**  
`modeling/dynamic_harmonic_regression.py:22–36,63–99`; S22, Assistentenzeile 32; S26, Nutzerzeile 55; S39, Nutzerzeilen 102,159 und Assistentenzeilen 123,152,162.

**Offene Fragen:**  
Welche Parameter wurden auf welchen Daten gewählt? Wie werden Nichtkonvergenz und ungültige Konfigurationen behandelt? Welche Mindesthistorie gilt wirklich?

**Relevanz für die Bachelorarbeit:**  
Implementierung; Hyperparameterwahl; Rechenbudget.

---

### DEC-027: Gemeinsame sktime-Schnittstelle und zeitliche Evaluationswerkzeuge

**Status:** Bestätigt

**Evidenzkategorie:** A

**Themenbereich:** Implementierung und Evaluation

**Entscheidung:**  
Beide Modelle erben von `BaseForecaster` und implementieren `_fit`/`_predict`; die Auswertung nutzt sktime-Splitter und Evaluatoren.

**Kontext / Problemstellung:**  
Die frühere eigene Schnittstelle `fit(df)`/`predict(df)` sollte für eine gemeinsame Auswertung vereinheitlicht werden.

**Alternativen:**  
S34 nennt eine kleine gemeinsame Evaluationsschleife als Alternative; zuvor war ein eigenes `ForecastModel`-Protokoll vorhanden.

**Begründung zum Entscheidungszeitpunkt:**  
S34, Assistentenzeile 27, begründet sktime mit konsistenten zeitlichen Backtests; S35, Nutzerzeile 12, und S39, Nutzerzeilen 12,50, wünschen die Integration beider Modelle ausdrücklich.

**Mögliche wissenschaftliche Begründung:**  
Nachträglicher Begründungsansatz, zu prüfen: Gemeinsame Werkzeuge erleichtern identische Splits und Metriken. Ein Framework beweist allein weder Leakage-Freiheit noch vollständige Kompatibilität eigener Modelle.

**Literaturgrundlage:**  
Versionsgebundene API-Links stehen in S34/S39 als technische Referenzen. L1 ist die vorhandene methodische Evaluationsquelle; eine spezifische sktime-Publikation wurde nicht überprüft.

**Konkrete Umsetzung:**  
`c95e29f` migriert XGBoost, `f1d64b3` DHR. Der alte Protocol-Code bleibt ungenutzt erhalten; dessen Verweis auf `modeling/README.md` zeigt auf eine heute fehlende Datei.

**Auswirkungen auf das Experiment:**  
Die Migration verändert XGBoost methodisch (DEC-021). DHR prognostiziert jetzt vom Fit-Zustand statt bei `predict` implizit eine neu übergebene Historie einzufiltern. Die Runner verwenden `refit`; ein eigener getesteter Update-Vertrag ist nicht vorhanden.

**Evidenz / Quellen im Projekt:**  
`modeling/protocols.py:1–23`; beide Modellklassen; `run_forecasting.py:47–64`; `run_benchmark.py:102–124`; Commits `c95e29f`, `f1d64b3`; S34, S35, S39.

**Offene Fragen:**  
Welche sktime-Fähigkeiten werden verbindlich unterstützt? Sind Updates außerhalb vollständiger Re-Fits vorgesehen? Welche Tests müssen an die Schnittstelle angepasst werden?

**Relevanz für die Bachelorarbeit:**  
Implementierung; einheitlicher Evaluationsablauf.

---

### DEC-028: 24- und 168-Stunden-Horizonte: Forschungsziel und aktueller Stand weichen ab

**Status:** Zu klären

**Evidenzkategorie:** C

**Themenbereich:** Versuchsdesign

**Entscheidung:**  
Als Forschungsziel sind 24 und 168 Stunden belegt. Beide aktuellen Runner konfigurieren ausschließlich 168 Stunden; eine endgültige Festlegung auf nur einen Horizont ist nicht nachgewiesen.

**Kontext / Problemstellung:**  
S23 und S34 verlangen den Vergleich beider Horizonte. Ein früheres Vergleichsskript ist heute weder im Arbeitsbaum noch in den untersuchten Git-Dateibäumen vorhanden.

**Alternativen:**  
S34 schlägt vor, eine 168-Stunden-Prognose zu erstellen und die ersten 24 Stunden gesondert zu bewerten; separate Modelle je Horizont werden ebenfalls diskutiert.

**Begründung zum Entscheidungszeitpunkt:**  
Für die aktuelle Beschränkung auf 168 Stunden: Nicht dokumentiert.

**Mögliche wissenschaftliche Begründung:**  
Nachträglicher Begründungsansatz, zu prüfen: Gemeinsame Ursprünge und ein gesonderter 24-Stunden-Präfix könnten vergleichbare Horizonte liefern. Das ist ein Vorschlag, kein aktuelles Ergebnis.

**Literaturgrundlage:**  
L1 ist der vorhandene Evaluationsrahmen. Literatur zur anwendungsbezogenen Wahl von day-ahead gegenüber week-ahead und zur horizonweisen Abstimmung fehlt.

**Konkrete Umsetzung:**  
`HORIZON=168` in beiden Runnern. Die Modelle können über `fh` andere zukünftige Schritte liefern; allein diese Fähigkeit implementiert noch keine 24-Stunden-Auswertung.

**Auswirkungen auf das Experiment:**  
Ein reiner Wochenmittelwert beantwortet die zweifache Forschungsfrage nicht vollständig. Unterschiedliche Prognosestarts könnten einen Horizontvergleich zusätzlich verändern.

**Evidenz / Quellen im Projekt:**  
`run_forecasting.py:13–15,47–50`; `run_benchmark.py:21–25,102–106`; S23, Nutzerzeile 45; S34, Nutzerzeile 34; historische Assistentenmeldungen S23:65 und S24:38.

**Offene Fragen:**  
Sind beide Horizonte verbindlich? Gleiche Ursprünge oder verschiedene operative Szenarien? Gemeinsame oder horizonweise Parameterwahl?

**Relevanz für die Bachelorarbeit:**  
Forschungsfrage; Prognoseaufgabe; experimentelles Design.

---

### DEC-029: Wachsende Historie im Einzellauf gegenüber festem Fenster im Benchmarkentwurf

**Status:** Rekonstruiert

**Evidenzkategorie:** B

**Themenbereich:** Versuchsdesign

**Entscheidung:**  
`run_forecasting.py` verwendet ein wachsendes Trainingsfenster ab vor 2026-01-01. Der Benchmarkentwurf verwendet feste 104 Wochen Training, 13 Wochen Validierung und 52 Wochen Test mit wöchentlichen Re-Fits.

**Kontext / Problemstellung:**  
Es existieren mehrere historische und aktuelle Auswertungsstände.

**Alternativen:**  
S39 diskutiert kürzere feste Fenster zur Begrenzung des DHR-Aufwands; eine verbindliche Auswahl gegenüber wachsendem Training ist nicht dokumentiert.

**Begründung zum Entscheidungszeitpunkt:**  
Nicht dokumentiert. Der historische Benchmark-Docstring begründet feste Fenster mit einem Methodenvergleich und nennt Giacomini/White; eine dokumentierte Herleitung von genau 104/13/52 Wochen fehlt.

**Mögliche wissenschaftliche Begründung:**  
Nachträglicher Begründungsansatz, zu prüfen: Feste Fenster begrenzen Aufwand und historische Reichweite, wachsende Fenster nutzen mehr Vergangenheit. Beides verändert den Vergleich und muss vor der Auswertung festgelegt werden.

**Literaturgrundlage:**  
L1 vorhanden; konkret die Wahl der Fensterlänge und saisonalen Abdeckung begründen. Historische Autorennamen im Benchmark sind noch keine geprüften Literaturbelege.

**Konkrete Umsetzung:**  
`ExpandingWindowSplitter` versus `SlidingWindowSplitter`; `fh=1..168`, Schritt 168, `strategy="refit"`. Benchmark-Zeiten: Validierung [2025-01-01,2025-04-02), Test [2025-04-02,2026-04-01); frühester Validierungs-Trainingsbeginn 2023-01-04.

**Auswirkungen auf das Experiment:**  
R01 zählt im aktuellen Einzellauf zwölf Wochen/2.016 Stunden bis 2026-03-25 23:00; 144 Stunden bleiben unbewertet. Historisch änderte sich der Testbeginn von 2025-04-01 (`c95e29f`) über 2024-04-01 (`e55c885`) auf 2026-01-01 (`f1d64b3`). Die Benchmarkgrenzen folgen ganzen Wochen, nicht Kalenderjahren.

**Evidenz / Quellen im Projekt:**  
`run_forecasting.py:13–15,43–68`; `run_benchmark.py:21–25,45–53,98–124`; genannte Commits; S38, S39; R01.

**Offene Fragen:**  
Welches Design ist final? Wie werden Reststunden behandelt? Warum nur 13 Validierungswochen und damit nur ein Teil des Saisonverlaufs? Welche Prognosefrequenz entspricht dem Einsatz?

**Relevanz für die Bachelorarbeit:**  
Experimentelles Design; Zeitaufteilung und Wiedertraining.

---

### DEC-030: Unberührte Testphase und abgeschlossene Validierung nicht nachgewiesen

**Status:** Zu klären

**Evidenzkategorie:** C

**Themenbereich:** Interne Validität

**Entscheidung:**  
Der Benchmark fordert Hyperparameterwahl nur auf Validierung. Ein tatsächlich eingefrorener Parametersatz und eine bislang unberührte Testphase sind anhand der Quellen nicht bestätigt.

**Kontext / Problemstellung:**  
Spätere Testabschnitte waren bereits Bestandteil früherer EDA und Auswertungsgespräche.

**Alternativen:**  
S38 diskutiert ein bzw. zwei Jahre Validierung/Test. Der frühere Benchmarktext fordert einmalige Testauswertung; dies ist eine Absichtserklärung.

**Begründung zum Entscheidungszeitpunkt:**  
Für eine tatsächlich schon abgeschlossene Validierung oder einen unberührten Test: Nicht dokumentiert.

**Mögliche wissenschaftliche Begründung:**  
Nachträglicher Begründungsansatz, zu prüfen: Eine klar datierte Festlegung von Parametern und Hauptauswertung kann spätere Auswahl anhand günstiger Ergebnisse begrenzen.

**Literaturgrundlage:**  
L1, Abschnitte 3.5 und 4, ist vorhanden. Die konkrete Testunabhängigkeit muss aus dem Projektablauf belegt werden, nicht durch ein Literaturzitat.

**Konkrete Umsetzung:**  
`build_estimators` kommentiert die Validierungsregel. S37 enthält vom Nutzer gepostete Fold-Ergebnisse ab April 2025; S38 enthält bereits einen Gesamt-MAE und -RMSE. Das EDA-Notebook lädt den gesamten Gold-Bestand.

**Auswirkungen auf das Experiment:**  
Die später als Test vorgesehene Periode überschneidet sich mit betrachteten Ergebnissen. Das ist ein konkretes Risiko nachträglicher Auswahl, aber kein Beweis, dass Parameter tatsächlich anhand dieser Ergebnisse optimiert wurden. Zeitlich spätere Re-Fits mit dann bekannten Beobachtungen sind davon zu unterscheiden.

**Evidenz / Quellen im Projekt:**  
`run_benchmark.py:76–91`; `f1d64b3:run_benchmark.py:1–14`; `eda/eda.ipynb`, Zellen 1–14; S37, Nutzerzeile 57; S38, Nutzerzeilen 173,221,252.

**Offene Fragen:**  
Welche Daten und Ergebnisse wurden für welche Entscheidungen angesehen? Wann wurden Features, Fenster und Hauptmetrik fixiert? Welche ehrliche Rolle erhält die vorhandene Testperiode?

**Relevanz für die Bachelorarbeit:**  
Versuchsdesign; Validität; Grenzen der Ergebnisinterpretation.

---

### DEC-031: Fünf Seeds als Einzelmodelle und als Mittelwertensemble

**Status:** Rekonstruiert

**Evidenzkategorie:** B

**Themenbereich:** Stochastik und Vergleichbarkeit

**Entscheidung:**  
Der Benchmarkentwurf erstellt XGBoost für Seeds 0–4 sowie ein arithmetisches Ensemble aus diesen fünf Mitgliedern; primär soll das Ensemble gegen DHR antreten.

**Kontext / Problemstellung:**  
Der Einzellauf nutzt dagegen den Defaultseed 42.

**Alternativen:**  
Einzelmodelle und Ensemble sind im Entwurf parallel enthalten; Gründe für fünf Seeds oder für die Ensemblehauptrolle sind nicht dokumentiert.

**Begründung zum Entscheidungszeitpunkt:**  
Nicht dokumentiert.

**Mögliche wissenschaftliche Begründung:**  
Nachträglicher Begründungsansatz, zu prüfen: Seedvarianten könnten Stabilität beschreiben; ein Ensemble kann eine andere Prognosemethode bilden. Beides muss getrennt ausgewertet werden.

**Literaturgrundlage:**  
Keine spezifische Seed-/Ensembleliteratur im Projekt. Wiederholbarkeit stochastischer Verfahren, Ensembleaggregation und faire Rechenbudgets recherchieren.

**Konkrete Umsetzung:**  
`XGB_SEEDS=(0,1,2,3,4)`; `EnsembleForecaster(...,aggfunc="mean")`; fünf zusätzliche Einzelmodelle; insgesamt neun Estimator-Einträge einschließlich DHR und zwei Naivbaselines.

**Auswirkungen auf das Experiment:**  
Fünf Seeds sind keine fünf unabhängigen Datenstichproben. Ensembletraining benötigt fünf XGBoost-Fits pro Ursprung; zusätzliche Einzelmodellläufe verdoppeln diese Fits. Laufzeitvergleiche müssen dies berücksichtigen.

**Evidenz / Quellen im Projekt:**  
`run_benchmark.py:26–28,76–93`; `modeling/gradient_boosting.py:25,113`; `f1d64b3`.

**Offene Fragen:**  
Sind Ensemble oder Einzel-XGBoost der Untersuchungsgegenstand? Wie werden Seedstreuung und Rechenbudget berichtet? Warum genau diese Seedmenge?

**Relevanz für die Bachelorarbeit:**  
Experimentelles Design; Wiederholungen; Vergleichbarkeit.

---

### DEC-032: Fehlermaße, Aggregation und Baselines unterscheiden sich zwischen Ständen

**Status:** Rekonstruiert

**Evidenzkategorie:** B

**Themenbereich:** Evaluationsmethodik

**Entscheidung:**  
Der aktuelle Einzellauf berichtet MAE und gepoolten RMSE. Der Benchmarkentwurf konfiguriert MAE, Fold-RMSE, MAPE und MASE mit Wochenperiode sowie Tages- und Wochen-Naivbaselines.

**Kontext / Problemstellung:**  
Bewertet werden Punktprognosen auf gleichen zeitlichen Blöcken; der historische Benchmark bezeichnet wöchentlichen MAE als Hauptverlust.

**Alternativen:**  
S38, Assistentenzeile 78, empfiehlt RMSE als Hauptmetrik; `f1d64b3` setzt stattdessen MAE als primär. Eine dokumentierte Begründung dieser Änderung fehlt.

**Begründung zum Entscheidungszeitpunkt:**  
Nicht dokumentiert.

**Mögliche wissenschaftliche Begründung:**  
Nachträglicher Begründungsansatz, zu prüfen: Mehrere Fehlermaße beschreiben unterschiedliche Eigenschaften; eine vorab festgelegte Hauptmetrik kann nachträgliche Auswahl begrenzen.

**Literaturgrundlage:**  
L1 vorhanden. Für die konkrete Hauptmetrik, MASE-Skalierung und die operative Gewichtung fehlt die projektspezifische Begründung.

**Konkrete Umsetzung:**  
`run_forecasting`: Mittel der Fold-MAE und Quadratwurzel aus Mittel der Fold-MSE. Historischer Benchmark: gepoolter RMSE aus Einzelprognosen. Aktuell `MeanSquaredError(square_root=True)` im Benchmark liefert Fold-RMSE; dessen Mittel ist allgemein nicht gleich dem gepoolten RMSE.

**Auswirkungen auf das Experiment:**  
Die Gewichte sind bei vollen 168-Stunden-Folds gleich. MAPE-Quotienten und Prozentwerte dürfen nicht verwechselt werden; der historische Export multiplizierte mit 100. Eine explizite aktuelle Nullwertregel fehlt. MASE ist von einer direkten Verbesserung gegenüber der Testbaseline zu unterscheiden.

**Evidenz / Quellen im Projekt:**  
`run_forecasting.py:58–68`; `run_benchmark.py:79–80,115–120`; `f1d64b3:run_benchmark.py`, Funktionen `accuracy_summary`, `forecasts_from_benchmark`; S38, Assistentenzeile 78.

**Offene Fragen:**  
Welche Metrik ist primär und warum? Welche Aggregation/Einheiten gelten? Wie werden Nullwerte, kleine MASE-Nenner, Lastspitzen und saisonale Teilgruppen behandelt?

**Relevanz für die Bachelorarbeit:**  
Evaluationsmethodik; Baselines; Ergebnisaggregation.

---

### DEC-033: Historischer gepaarter Verlusttest ist kein bestätigtes finales Inferenzverfahren

**Status:** Zu klären

**Evidenzkategorie:** C

**Themenbereich:** Statistische Auswertung

**Entscheidung:**  
`f1d64b3` implementiert einen als Diebold-Mariano/Giacomini-White bezeichneten Vergleich wöchentlicher MAE-Differenzen mit 95-%-Intervall. Im aktuellen Arbeitsstand sind die Testfunktionen entfernt.

**Kontext / Problemstellung:**  
Das historische Skript nennt eine zweiseitige primäre Hypothese DHR gegen XGBoost-Ensemble und weitere explorative Vergleiche.

**Alternativen:**  
S38 diskutiert Signifikanztests ergänzend zu Fehlermaßen. Eine endgültige Entscheidung über einen abhängigkeitstauglichen Test ist nicht belegt.

**Begründung zum Entscheidungszeitpunkt:**  
Der historische Docstring begründet `horizon=1` mit nicht überlappenden Wochenblöcken. Diese Begründung ist dokumentiert, aber ihre hinreichende Gültigkeit nicht gezeigt.

**Mögliche wissenschaftliche Begründung:**  
Nachträglicher Begründungsansatz, zu prüfen: Gepaarte Verluste je Ursprung können Unterschiede ausdrücken. Nicht überlappende Zielblöcke garantieren keine unkorrelierten wöchentlichen Verlustdifferenzen, etwa bei gemeinsamen Trainingsdaten und persistierenden Lastmustern.

**Literaturgrundlage:**  
L1 enthält statistische Evaluation. Der historische Code nennt Diebold/Mariano (1995), Harvey/Leybourne/Newbold (1997) und Giacomini/White (2006); vollständige Originalquellen und Eignung wurden hier nicht verifiziert und müssen vor Verwendung recherchiert werden.

**Konkrete Umsetzung:**  
Historisch: `diebold_mariano_test`, ungewichtete Autokovarianzen bis `horizon-1`, Korrektur und t-Verteilung; Default 1. Ergänzend ACF/Ljung-Box bis Lag 4. Aktuell bleiben nur Konstanten und `PairedLossTest`-Dataclass.

**Auswirkungen auf das Experiment:**  
Ein p-Wert dieses Entwurfs wäre ohne Prüfung der Abhängigkeit nicht als abgesicherte Evidenz zu interpretieren. Diagnostik allein korrigiert die Varianzschätzung nicht; mehrere explorative Vergleiche brauchen eine transparente Rolle.

**Evidenz / Quellen im Projekt:**  
`f1d64b3:run_benchmark.py:1–14,117–174` sowie `differential_diagnostics`, `compare`; lokaler Diff; aktuell `run_benchmark.py:27–42`; S38, Assistentenzeile 78.

**Offene Fragen:**  
Welche inferenzielle Frage wird geprüft? Wie werden Abhängigkeit, Stichprobengröße, Mehrfachvergleiche und praktische Effektgröße berücksichtigt? Soll der Test überhaupt Teil der Arbeit werden?

**Relevanz für die Bachelorarbeit:**  
Evaluationsmethodik; statistische Unsicherheit.

---

### DEC-034: Fehler nach exakter Lead Time auswerten

**Status:** Bestätigt

**Evidenzkategorie:** A

**Themenbereich:** Detaillierte Fehleranalyse

**Entscheidung:**  
Historisch wurde MAE für exakte Leads 1,6,12,24,48,72,120,168 implementiert; der spätere Benchmark berechnete alle Leads. Diese Exporte fehlen im aktuellen Arbeitsstand.

**Kontext / Problemstellung:**  
Ein Gesamtfehler der Woche zeigte dem Nutzer zu wenig darüber, wie die Güte innerhalb des Horizonts variiert.

**Alternativen:**  
Exakte Leads, Tagesaggregate und kumulierte Horizontfehler werden in den Gesprächen voneinander unterschieden.

**Begründung zum Entscheidungszeitpunkt:**  
S37, Nutzerzeilen 46,57, fordert ausdrücklich feinere Fehler als den Wochenwert; S24, Nutzerzeile 9, spezifiziert die gewünschte Lead-Tabelle. S24 erklärt die Nutzung nur der Wochenprognosen zur Vermeidung von Doppelzählung.

**Mögliche wissenschaftliche Begründung:**  
Nachträglicher Begründungsansatz, zu prüfen: Ein Leadprofil kann Fehlerfortpflanzung und unterschiedliche Kurz-/Langfristgüte beschreiben. Einzelne Leads benötigen ausreichend viele vergleichbare Ursprünge.

**Literaturgrundlage:**  
Keine spezifische, im Projekt geprüfte Lead-Auswertungsquelle; L1 liefert allgemeinen Evaluationskontext. Literatur für horizontspezifische Güte noch ergänzen.

**Konkrete Umsetzung:**  
S24 berichtet `lead_time_mae.csv`; historischer Benchmark: `pivot_table(index="horizon",values="abs_error",aggfunc="mean")`. Aktueller Einzellauf berechnet nur Gesamt-MAE/RMSE.

**Auswirkungen auf das Experiment:**  
MAE bei h+24 ist etwas anderes als MAE über h+1 bis h+24. Eine erste Tagesauswertung beantwortet eine andere Frage als ein einzelner Stundenlead.

**Evidenz / Quellen im Projekt:**  
S24, Nutzerzeile 9 und Assistentenzeilen 27,38; S37, Nutzerzeilen 46,57; `f1d64b3:run_benchmark.py`, Block `horizon_mae`; lokaler Diff.

**Offene Fragen:**  
Welche Leads, Tagesgruppen und Horizonte werden vorab festgelegt? Wo werden dazu Einzelprognosen gespeichert? Wie werden fehlende Ursprünge behandelt?

**Relevanz für die Bachelorarbeit:**  
Evaluationsmethodik; Fehlerstruktur nach Prognosehorizont.

---

### DEC-035: Python-/Bibliotheksumgebung und Tests als begrenzte Reproduzierbarkeitsbasis

**Status:** Rekonstruiert

**Evidenzkategorie:** B

**Themenbereich:** Reproduzierbarkeit

**Entscheidung:**  
Das Projekt nutzt Python ab 3.12, uv-Lockdatei und pytest. Einige Tests prüfen lokale Silver-/Gold-Daten, Featuretests verwenden kleine synthetische Daten.

**Kontext / Problemstellung:**  
Umgebung und grundlegende Datenannahmen sollen wiederholbar überprüfbar sein.

**Alternativen:**  
Alternative Konfigurationen wie YAML/Pydantic und eine Polars-Loaderumstellung werden in S07/S11 diskutiert, sind aktuell aber nicht die realisierte Konfiguration.

**Begründung zum Entscheidungszeitpunkt:**  
Nicht dokumentiert. S06/S09 betreffen Testeinrichtung und Nutzbarkeit, begründen keine vollständige wissenschaftliche Reproduzierbarkeitsstrategie.

**Mögliche wissenschaftliche Begründung:**  
Nachträglicher Begründungsansatz, zu prüfen: Ein Lockfile und reproduzierbare Prüfungen können Softwarevariation begrenzen. Sie archivieren keine Daten, Hardware oder finalen Experimente.

**Literaturgrundlage:**  
Keine spezifische Reproduzierbarkeitsliteratur im Projekt; geeignete Forschungssoftware- und Experimentdokumentationsleitlinien recherchieren.

**Konkrete Umsetzung:**  
`pyproject.toml` setzt `testpaths=["tests"]`, `pythonpath=["."]`. R01 gleicht zentrale installierte Versionen mit `uv.lock` ab. Historische `quality_check/`-Pfade in AGENTS.md sind überholt.

**Auswirkungen auf das Experiment:**  
R02: 10 Tests bestehen, ein veralteter XGBoost-Trainingstest scheitert. DHR- und frühere Cleaning-/Vergleichstests sind aktuell nicht vorhanden. Hardware, Parallelisierung und Laufzeitumgebung früherer Experimente sind nicht hinreichend dokumentiert.

**Evidenz / Quellen im Projekt:**  
`pyproject.toml:6–29`; `.python-version`; `uv.lock`; `tests/`; `AGENTS.md`; `.pytest_cache/v/cache/nodeids` als undatierter Hinweis; S06–S09; R01/R02.

**Offene Fragen:**  
Welche Hardware und Threadzahl gelten? Wie werden lokale Daten für andere reproduzierbar bereitgestellt? Welche früheren Tests sollen wieder verfügbar sein?

**Relevanz für die Bachelorarbeit:**  
Implementierung; Reproduzierbarkeit und Qualitätssicherung.

---

### DEC-036: Experimentartefakte und Metadaten historisch vorgesehen, aktuell nicht gespeichert

**Status:** Rekonstruiert

**Evidenzkategorie:** B

**Themenbereich:** Ergebnisprovenienz

**Entscheidung:**  
Der Commitbenchmark schrieb Einzelprognosen, Scores, Ursprungs-/Leadfehler, Zusammenfassungen, Tests und Metadaten. Diese Speicherung wurde im lokalen Arbeitsstand entfernt.

**Kontext / Problemstellung:**  
Nachvollziehbare Zuordnung von Ergebnissen zu Modellkonfiguration, Datensatz und Softwarestand ist erforderlich.

**Alternativen:**  
S13 diskutiert Datenversionen. Historische Ergebnisprovenienz und die heutige reine Berechnung sind nachweisbare Varianten; Gründe für die Entfernung sind nicht dokumentiert.

**Begründung zum Entscheidungszeitpunkt:**  
Nicht dokumentiert.

**Mögliche wissenschaftliche Begründung:**  
Nachträglicher Begründungsansatz, zu prüfen: Gespeicherte Einzelprognosen und Metadaten ermöglichen eine prüfbare Nachberechnung. Eine bloße `dirty`-Markierung reproduziert lokale Änderungen noch nicht.

**Literaturgrundlage:**  
Keine spezifische Provenienzquelle im Projekt; Literatur/Leitlinien zur Archivierung vollständiger Forschungsläufe recherchieren.

**Konkrete Umsetzung:**  
Historisch `data/results/benchmark_{period}` mit `scores.csv`, `forecasts.csv`, `origin_mae.csv`, `horizon_mae.csv`, `summary.csv`, `tests.csv`, `metadata.json`. Metadaten enthielten Git-Hash/Dirty-Status, Versionen und Parameter, aber keinen Datensatzhash. Aktuell bleibt `results` lokal und ungespeichert.

**Auswirkungen auf das Experiment:**  
Bei der Bestandsaufnahme sind keine entsprechenden Ergebnisdateien vorhanden. `main()` greift im aktuellen Benchmark auf undefiniertes `args.period` zu; die frühere Argumentverarbeitung fehlt. Der Benchmark ist dadurch derzeit nicht direkt ausführbar.

**Evidenz / Quellen im Projekt:**  
`f1d64b3:run_benchmark.py`, Funktionen `git_state`, `main`; aktueller `run_benchmark.py:96–125`; lokaler Diff; Dateiinventur R01; Arbeitsstand-SHA-256 im Research Log.

**Offene Fragen:**  
War die Kürzung ein Zwischenstand? Welche Ergebnisdateien existieren außerhalb dieses Repositories? Welche Kombination aus Datenhash, Code, Konfiguration und Umgebung soll archiviert werden?

**Relevanz für die Bachelorarbeit:**  
Implementierung; Reproduzierbarkeit; Ergebnisverwaltung.

---

### DEC-037: Revidierte Daten und reale Verfügbarkeit am Prognosestart sind ungeklärt

**Status:** Zu klären

**Evidenzkategorie:** C

**Themenbereich:** Datengrundlage und externe Validität

**Entscheidung:**  
Die Nutzung später exportierter bzw. aktualisierter Lastdaten als vermeintlich damals sofort verfügbare Historie ist möglich; ein historischer Echtzeitdatenbestand ist nicht nachgewiesen.

**Kontext / Problemstellung:**  
Quellen überlappen mit unterschiedlichen Werten; Rohdateien besitzen teilweise `CreateDate`/`UpdateDate`, die im Panel verworfen werden. Die Features verwenden jüngste vergangene Lasten ohne Veröffentlichungsmodell.

**Alternativen:**  
Keine nachweislich erwogene Variante mit historischen Datenständen oder explizitem Publikationsverzug.

**Begründung zum Entscheidungszeitpunkt:**  
Nicht dokumentiert.

**Mögliche wissenschaftliche Begründung:**  
Nachträglicher Begründungsansatz, zu prüfen: Ein retrospektiver Vergleich auf einem fixierten Datenstand kann ein legitimes Untersuchungsziel sein. Ein Anspruch operativer Echtzeitprognose benötigt zusätzlich nachgewiesene Verfügbarkeit.

**Literaturgrundlage:**  
L3 und die vorhandenen Rohmetadaten reichen für diesen Nachweis nicht aus. Anbieterinformationen zu Veröffentlichung, Revision und Datenständen recherchieren.

**Konkrete Umsetzung:**  
Zeitbasierte Splits beschränken Messzeitpunkte. Sie kontrollieren nicht, wann diese Messwerte veröffentlicht oder revidiert wurden. `select_rellevant_columns` entfernt Aktualisierungsmetadaten.

**Auswirkungen auf das Experiment:**  
Zeitlich korrekter Modellcode kann trotzdem eine unrealistische Informationsbasis simulieren. Das ist ein zu prüfendes Risiko, kein nachgewiesener Leakage-Vorfall.

**Evidenz / Quellen im Projekt:**  
`ingestion/load_raw.py:55–56`; R01, Bronze-Header; S13, Assistentenzeile 63 zu abweichenden Lieferungen; `modeling/gradient_boosting.py:46–68`; DEC-003/018/019.

**Offene Fragen:**  
Wann waren Lasten tatsächlich verfügbar? Sind Werte nachträglich revidiert? Wird ein retrospektiver Methodenvergleich oder ein operativer Einsatzanspruch formuliert?

**Relevanz für die Bachelorarbeit:**  
Datengrundlage; Informationsverfügbarkeit; Limitationen.

---

Wichtigste Entscheidungen:
CSV-Daten erhalten im Überlappungsjahr 2019 Vorrang gegenüber Excel.
Sechs Zeitstempel werden anhand der Intervallfelder korrigiert; UTC und Intervallanfang bleiben fachlich zu bestätigende Annahmen.
Gold enthält strukturell lückenlose 98.591 Stunden.
Die Excel-Daten weisen Abdeckung 98 aus, die CSV-Daten Abdeckung 100. Die Pipeline übernimmt durchgehend Value und verwirft diese Abdeckungsinformation. Eine harmonisierte Messgrundlage ist damit noch nicht nachgewiesen.
Abschließende Laufzeitprüfungen wurden historisch entfernt; intern erzeugte Auditspalten werden nicht gespeichert.





