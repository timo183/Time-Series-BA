# Zuordnung zum Methodikkapitel

Arbeitsgrundlage vom **29.10.2026** zu [Decision Log](decisions.md) und [Research Log](research_log.md). Die Struktur folgt dem belegten Vorhaben eines empirischen Vergleichs von DHR mit ARIMA-Fehlern und XGBoost für deutsche Stromlast. Ein finaler Titel und eine endgültige Forschungsfrage sind nicht dokumentiert.

Die folgenden Textbausteine sind **Entwürfe**, keine vollständig wissenschaftlich belegten Methodikabschnitte. `[PRÜFEN]` bezeichnet ungeklärte Fakten oder verbindlich festzulegende Regeln; `[QUELLE ERFORDERLICH]` bezeichnet fehlende wissenschaftliche oder exportbezogene Belege. Belegte Softwareparameter benötigen nicht automatisch einen Literaturbeleg; ihre fachliche Auswahl gegebenenfalls schon.

Die 37 Einträge umfassen **13 explizit begründete Entscheidungen (A)**, **20 aus der Umsetzung rekonstruierte Entscheidungen (B)** und **vier ungeklärte Festlegungen (C)**. Kategorie A besagt, dass eine Begründung dokumentiert ist, nicht dass sie bereits wissenschaftlich hinreichend geprüft wurde.

## 1. Forschungsfrage und Prognoseaufgabe

**Zugeordnete Entscheidungen:** DEC-016, DEC-017, DEC-021, DEC-028, DEC-037.

**Bereits erkennbar:** Vergleich zweier Modellfamilien auf einer deutschen stündlichen Lastreihe; separates klassisches ARIMA wurde ausdrücklich ausgeschlossen. 24 und 168 Stunden wurden als Prognosehorizonte verlangt. Die aktuellen Runner evaluieren ausschließlich 168 Stunden. S25 diskutiert einen Titel, bestätigt aber keine endgültige Fassung.

**Dokumentierte Umsetzung:** Ein univariater XGBoost-Forecaster und eine DHR-Klasse; Punktprognosen, keine ausgewerteten Prognoseintervalle. Die aktuelle XGBoost-Architektur ist ein rekursives Ein-Modell-Verfahren und unterscheidet sich von der früheren Architektur mit 24 Zieluhrzeitmodellen.

**Vorhandene Begründungen:** Die Merkmalsverfügbarkeit des früheren Tagesmodells und der saisonale DHR-Modellrahmen sind dokumentiert. Warum gerade diese Modellfamilien die Forschungsfrage angemessen beantworten und warum separates ARIMA entfällt, ist nicht begründet.

**Benötigte Literatur:** Grundlegende XGBoost-Quelle, Vergleichsliteratur zur kurzfristigen Stromlastprognose und direkte/rekursive Mehrschrittstrategien `[QUELLE ERFORDERLICH]`. L2 beschreibt den vorhandenen DHR-Rahmen; die konkrete Auswahl bedarf zusätzlicher Argumentation.

**Offene methodische Fragen:** Beide Horizonte oder nur Woche? Prognose täglich oder wöchentlich? Uhrzeit der Erstellung? Univariate Prognose als bewusste Einschränkung? Retrospektiver Vergleich auf revidierten Daten oder Nachbildung eines realen Informationsstands?

**In der Arbeit anzugeben:** Untersuchungsobjekt und Lastdefinition, Horizonte und Aktualisierungsrhythmus, Informationsmenge am Ursprung, zu vergleichende Verfahren einschließlich Ensembles/Baselines und Reichweite der Aussagen.

**Textbaustein:**

> Die Untersuchung vergleicht eine Fourier-Regression mit ARIMA-Fehlern und einen XGBoost-basierten rekursiven Forecaster anhand einer deutschen stündlichen Lastreihe. Die betrachteten Prognosehorizonte werden auf [PRÜFEN: 24 und 168 Stunden oder ausschließlich 168 Stunden] festgelegt. Die Auswahl der Verfahren wird anhand ihrer Eignung für diese Prognoseaufgabe begründet [QUELLE ERFORDERLICH]. Der Vergleich bezieht sich auf [PRÜFEN: retrospektiv verfügbare oder zum jeweiligen Prognosestart tatsächlich verfügbare] Messwerte.

## 2. Datengrundlage und Auswahl der Zielvariable

**Zugeordnete Entscheidungen:** DEC-001, DEC-002, DEC-003, DEC-008, DEC-037.

**Bereits getroffen:** Deutschlandfilter, Dateien ab 2015, CSV-Priorität ab 2019, Zielvariable `Value`, Analysefenster bis Ende März 2026.

**Dokumentierte Umsetzung:** Zwei Excel-Blätter plus acht CSV-Dateien; nur Excel vor 2019 bleibt erhalten. Die ältere Datei 2006–2015 liegt lokal vor, wird aber nicht verwendet. Der Export verwarf `Cov_ratio`, `Value_ScaleTo100` und Aktualisierungsmetadaten.

**Vorhandene Begründungen:** Quellenpriorität wegen überlappender, unterschiedlicher Werte ist belegt. Anfangsjahr, Startstunde 01:00 und Wahl der unskalierten Zielspalte sind nicht begründet.

**Wichtiger aktueller Befund:** R01 zeigt in allen 40.895 deutschen Zeilen der verwendeten Excel-Datei Abdeckung 98 und Unterschiede zwischen `Value` und `Value_ScaleTo100`. In sämtlichen deutschen CSV-Zeilen 2019–2026 ist die Abdeckung 100 und beide Wertspalten sind identisch. Auch eine bloße Umstellung der überlappenden Excel-Werte auf die skalierte Spalte erzeugt keine Übereinstimmung mit der CSV. Eine harmonisierte Messgrundlage ist daher noch nicht nachgewiesen.

**Benötigte Literatur/Quellendokumentation:** Exportbezogene Lastdefinition, Einheit, Bedeutung der Abdeckung und Hochrechnung, geografischer Geltungsbereich, Revisionspraxis `[QUELLE ERFORDERLICH]`. L3 liefert historischen Kontext; der konkrete moderne Export muss gesondert belegt werden.

**Offene methodische Fragen:** Sind Messniveaus vor/nach 2019 vergleichbar? Wie wird mit Abdeckung 98 verfahren? Warum 2015-01-01 01:00 als Start? Wann wurden verwendete Messwerte verfügbar und revidiert?

**In der Arbeit anzugeben:** Originaldateien und Bezugsquelle, Abruf-/Versionsstand, Deutschlandauswahl, Ein- und Ausschlusskriterien, Zeitraum, Einheit, Quellenpriorität, Abdeckungsproblem und dessen tatsächliche Lösung oder Einschränkung.

**Textbaustein:**

> Die Datenpipeline verwendet deutsche Beobachtungen aus einer Excel-Lieferung für 2015–2019 und jährlichen CSV-Exporten ab 2019. Im Überlappungsbereich erhält die CSV Vorrang. Die bisherige Implementierung übernimmt die Spalte `Value`; die Excel-Daten weisen eine Abdeckung von 98, die CSV-Daten von 100 aus. [PRÜFEN: Vor dem finalen Vergleich ist die fachliche Vergleichbarkeit dieser Messgrundlagen zu bestätigen bzw. eine begründete Harmonisierung festzulegen.] Die genaue Definition der Last und ihrer Einheit wird anhand der konkreten Exportdokumentation beschrieben [QUELLE ERFORDERLICH].

## 3. Datenaufbereitung, Zeitachse und Qualitätssicherung

**Zugeordnete Entscheidungen:** DEC-004, DEC-005, DEC-006, DEC-007, DEC-009, DEC-010, DEC-011, DEC-012.

**Bereits getroffen:** Formatspezifische Parser, explizite Typen, Bronze/Silver/Gold, vorläufige UTC-/Intervallstartinterpretation, sechs gezielte Zeitkorrekturen, Zeitraumfilterung und Sortierung. Lasten werden nicht interpoliert, gemittelt oder statistisch beschnitten.

**Dokumentierte Umsetzung:** Siehe `ingestion/load_raw.py`, `preprocessing/data_cleaning.py`, Loader und Writer. Vorhandenes Gold enthält 98.591 Stunden; R01 kann es im Speicher aus Silver reproduzieren. Nach der Korrektur werden nur `DateUTC` und `Value` gespeichert.

**Vorhandene Begründungen:** Trennzeichen-/Schemafehler sind dokumentiert; sechs Konflikte wurden anhand abweichender Intervallbeschriftungen untersucht. Die falsche Gleichsetzung wiederholter Lastwerte mit Duplikaten wurde ausdrücklich korrigiert. UTC wird in der README nur als durch den Spaltennamen gestützte Annahme bezeichnet.

**Abweichungen, die im Methodiktext sichtbar bleiben müssen:** Die abschließende Laufzeitprüfung auf eindeutigen, vollständigen Stundenindex entfiel in `ed2dee2`. Historisch vorgesehenes Audit und Intervallfelder werden nicht ins aktuelle Gold geschrieben. Separate Integrationstests bestehen für den vorhandenen Datenstand, ersetzen aber keine automatische Exportbedingung. Die README beschreibt diese Punkte teilweise anders.

**Benötigte Literatur:** Zeitstempelsemantik des konkreten Exports, Umgang mit fehlerhaften Messungen, echte versus Schlüsselduplikate und gegebenenfalls Lastausreißer `[QUELLE ERFORDERLICH]`. Eine historische CET/CEST-Richtlinie bestätigt den späteren Export nicht automatisch.

**Offene methodische Fragen:** Können UTC und Intervallanfang extern bestätigt werden? Sind die sechs Korrekturen unabhängig plausibilisiert? Welche Prüfschritte werden künftig verbindlich? Wo bleibt der Auditnachweis? Wie werden zukünftige echte Lücken behandelt?

**In der Arbeit anzugeben:** Tatsächliche Transformationsreihenfolge, Zeitkonvention samt Unsicherheit, genaue Korrekturregel und Zahl der Änderungen, zwei ausgeschlossene Anfangsstunden, Verhalten bei ungültigen Werten, Sortierung, Gold-Schema und ausführbare Qualitätskontrollen.

**Textbaustein:**

> Die eingelesenen Zeitstempel werden als UTC-Intervallanfänge interpretiert. Diese Exportannahme ist noch durch eine spezifische Quellenbeschreibung zu bestätigen [PRÜFEN; QUELLE ERFORDERLICH]. Für sechs Konflikte in den Jahren 2019–2024 ordnet die Implementierung eine unter 03:00 geführte Beobachtung dem Intervall 02:00–03:00 zu, sofern die Intervallfelder dieses Intervall ausweisen. Die Lastwerte werden dabei nicht verändert. Nach Zeitraumfilterung und Sortierung enthält das vorhandene Gold-Panel 98.591 Beobachtungen. [PRÜFEN: Verbindliche abschließende Indexvalidierung und persistente Dokumentation der Korrekturen ergänzen oder die bestehende Einschränkung ausdrücklich angeben.]

## 4. Explorative Analyse und ihre Rolle bei der Modellentwicklung

**Zugeordnete Entscheidungen:** DEC-013, DEC-014, DEC-015; Verbindung zu DEC-030.

**Bereits umgesetzt:** Jahresgetrennte Monats-/Wochentags-/Stundenmittel, ADF mit AIC-Lagauswahl, ACF/PACF, additive Tageszerlegung und robuste MSTL mit Tages-/Wochenperioden.

**Dokumentierte Beobachtungen:** Gespeichertes aktuelles Notebook zählt 98.591 Werte; es zeigt ADF −21,230530745378385 bei gerundeter p-Ausgabe 0,0. Frühere Chats enthalten andere ADF-Werte. Die Ergebnisse gehören deshalb jeweils zu ihrem belegten Artefakt; ein identischer Datenstand wird nicht unterstellt.

**Vorhandene Begründungen:** Nutzerwunsch nach zusätzlichen Saisonprofilen und Diskussion mehrerer saisonaler Faktoren. Keine ausreichende Dokumentation einer aus diesen Ergebnissen abgeleiteten optimalen Modellordnung.

**Benötigte Literatur:** ADF-Annahmen und Lagwahl, Grenzen von Einheitswurzeltests, saisonale Diagnostik und MSTL `[QUELLE ERFORDERLICH]`. L2 ist ein allgemeiner saisonaler Modellbezug.

**Offene methodische Fragen:** Welche EDA wurde vor welchen Modellentscheidungen durchgeführt? Soll sie künftig ausschließlich Training/Validierung betreffen? Wurde die additive Annahme geprüft? Werden Modellresiduen von Rohreihen-ACF/PACF unterschieden?

**In der Arbeit anzugeben:** Zeitraum je EDA, Datenstand und Plotaggregation, Testeinstellungen und begrenzte Interpretation, Unterschied zwischen Beschreibung und zur Modellwahl verwendeter Analyse. Die Zerlegung ist derzeit keine ML-Transformation.

**Textbaustein:**

> Die explorative Analyse untersucht Monats-, Wochentags- und Stundenprofile sowie Einheitswurzel- und Autokorrelationsdiagnostik. Zusätzlich werden additive Tageskomponenten und eine robuste Mehrperiodenzerlegung dargestellt. Diese Verfahren dienen bislang der Beschreibung; die resultierenden Komponenten werden nicht als Forecast-Merkmale verwendet. [PRÜFEN: Für modellleitende Auswertungen ist der zulässige Entwicklungszeitraum festzulegen.] Die Interpretation des ADF-Ergebnisses wird auf die geprüfte Nullhypothese und Testkonfiguration begrenzt [QUELLE ERFORDERLICH].

## 5. Modellimplementierung und Merkmalsbasis

**Zugeordnete Entscheidungen:** DEC-017, DEC-018, DEC-019, DEC-020, DEC-021, DEC-022, DEC-023, DEC-024, DEC-025, DEC-026, DEC-027.

**Bereits umgesetzt:** Einheitliche sktime-Basisklasse; DHR mit Fourier-Saisonalität und ARIMA-Fehlern; ein gemeinsames rekursives XGBoost-Modell mit fünf Lastmerkmalen. Beide bekommen die Lastreihe, DHR zusätzlich deterministisch aus der Zeit berechnete Regressoren.

**Technische Angaben für die Arbeit:**

| Bestandteil | Nachgewiesene Umsetzung |
|---|---|
| XGBoost-Lags | 24, 48, 168 Stunden vor der Zielstunde |
| XGBoost-Mittelwerte | 24/168 Stunden, Ende am Vortag um 23:00 UTC; innerhalb eines Zieltags konstant |
| XGBoost-Training | Nur vollständige Feature-/Zielzeilen; ein Regressor über alle Uhrzeiten |
| XGBoost-Mehrschrittprognose | Eigene Vorhersagen werden in temporäre Historie geschrieben; keine wahren Zielwerte der gerade prognostizierten Woche |
| XGBoost-Defaults | 200 Bäume, Lernrate 0,05, Tiefe 4, Subsample/Colsample je 0,8, quadratischer Fehler, Histogrammverfahren |
| Inaktive XGBoost-Parameter | `n_lags`, `period`, `K` ändern aktuell keine Merkmale |
| DHR-Saisonalität | 24/168 Stunden, je drei Harmonische; im Default zwölf Fourier-Spalten plus Konstante |
| DHR-Fehlerprozess | `order=(1,0,1)`, keine saisonale ARIMA-Komponente |
| DHR-Zeitbasis | Stunden seit 2000-01-01 UTC; doppelte Frequenzen entfernt, Nyquist-Sinus ausgelassen |
| DHR-Skalierung | Maximum der absoluten Trainingslast, mindestens 1; Rücktransformation bei Prognose |
| DHR-Schätzung | `maxiter=200`; `minimum_history=168` ist derzeit nicht erzwungen; keine explizite Konvergenzregel |
| Historischer Unterschied | 24 Zieluhrzeitmodelle wurden durch ein gemeinsames Modell ersetzt; dies ist mehr als eine API-Änderung |

**Vorhandene Begründungen:** Lag-/Mittelwertauswahl aus Verfügbarkeit beim früheren Tagesforecast, stabile Fourierbasis, numerische DHR-Skalierung und konsistente Evaluationsschnittstelle. Die konkreten Hyperparameter und die Aufgabe der 24 Modelle sind nicht hinreichend fachlich begründet.

**Benötigte Literatur:** L2 als vorhandene DHR-Grundlage; XGBoost-Originalarbeit, direkte/rekursive Prognose, Lag- und Fensterwahl, numerische Schätzung und Konvergenz `[QUELLE ERFORDERLICH]`.

**Offene methodische Fragen:** Welche aktuelle Architektur gilt final? Weshalb Mittelwerte weiter tageweise fixieren? Wie werden Merkmalsunterschiede kontrolliert oder als Bestandteil der Verfahren interpretiert? Welche Parameter werden auf Validierung gewählt? Wie groß sind effektive Trainingsmengen nach Warm-up?

**In der Arbeit anzugeben:** Mathematische Definitionen aller Merkmale, Prognoseablauf, Information je Schritt, DHR-Spezifikation einschließlich Skalierung, reale aktive Hyperparameter, Bibliotheken und tatsächlich implementierte Validierung. Revisionsgeschichte nur aufnehmen, wenn sie Vergleichsergebnisse oder Designentscheidungen erklärt.

**Textbaustein:**

> Das XGBoost-Modell verwendet drei Last-Lags und zwei vor dem jeweiligen UTC-Zieltag endende Mittelwerte. Es wird gemeinsam über alle Stunden trainiert und erzeugt Mehrschrittprognosen rekursiv, indem vorhergesagte Werte für spätere Featureberechnungen zur Verfügung stehen. DHR modelliert tägliche und wöchentliche Struktur durch Fourier-Terme sowie verbleibende Dynamik durch ARIMA-Fehler. Der Skalierungsfaktor wird ausschließlich aus dem jeweiligen Training berechnet. [PRÜFEN: Final aktive Hyperparameter und deren Auswahlverfahren angeben.] Die Auswahl der Merkmals- und Prognosestrategien wird fachlich begründet [QUELLE ERFORDERLICH].

## 6. Experimentelles Design und Parameterwahl

**Zugeordnete Entscheidungen:** DEC-028, DEC-029, DEC-030, DEC-031; Verbindungen zu DEC-020/022/026/037.

**Bereits implementiert:** Zeitgeordnete Splits mit vollständigen Re-Fits und wöchentlichen, nicht überlappenden 168-Stunden-Zielblöcken. Es bestehen jedoch zwei unterschiedliche Runnerdesigns.

| Aspekt | Aktueller Einzellauf | Benchmarkentwurf |
|---|---|---|
| Verfahren | XGBoost, Seed 42 | DHR, fünf XGBoost-Seeds, deren Mittelwertensemble, zwei saisonale Naivmodelle |
| Trainingshistorie | Wachsend, alle vorhandenen Werte vor jeweiligem Ursprung | Fest 104 Wochen |
| Bewertungszeit | Konfiguriert Januar–März 2026 | Validierung Januar bis 02.04.2025; Test 02.04.2025 bis vor 01.04.2026 |
| Horizonte | 168 Stunden | 168 Stunden |
| Tatsächliche Abdeckung | Nur zwölf volle Wochen; sechs Resttage bleiben aus | 13 bzw. 52 Wochen beabsichtigt, kein belegter kompletter Lauf |
| Ausführbarkeit | Vorhandener Runner; hier kein Forecastlauf gestartet | Lokal undefiniertes `args.period`; nicht direkt ausführbar |
| Finale Festlegung | Nicht nachgewiesen | Nicht nachgewiesen |

**Vorhandene Begründungen:** Gemeinsame Backtests und keine wahren zukünftigen Lastwerte im rekursiven Horizont. Rechenaufwand als möglicher Grund für kürzere Historie wurde diskutiert. Exakte Fensterlängen, Seedanzahl, Testgrenzen und Ensemblehauptrolle sind nicht ausreichend begründet.

**Benötigte Literatur:** L1 als vorhandener Evaluationsbezug; spezifische Herleitung der saisonalen Abdeckung, Fensterwahl und fairer Rechenbudgets `[QUELLE ERFORDERLICH]`.

**Offene methodische Fragen:** Finale Fenster und Prognoseursprünge? Gleiche Historie je Verfahren und Behandlung des XGBoost-Warm-ups? Gemeinsames oder horizonweises Tuning? Abschließendes Testprotokoll trotz bereits betrachteter 2025/2026-Ergebnisse? Umgang mit Reststunden und Nichtkonvergenz? Single-XGBoost oder Ensemble als Hauptverfahren?

**In der Arbeit anzugeben:** Exakte inklusive/exklusive Datumsgrenzen; Trenngrenzen zwischen Entwicklung, Validierung und Auswertung; Informationsstand und Re-Fit-Regel; Parameterraum, Suchbudget und Auswahlmetrik; Seeds und deren Rolle; Umgang mit fehlgeschlagenen Fits und unvollständigen letzten Blöcken. Wochenblöcke sind keine unabhängigen Wiederholungen allein aufgrund fehlender zeitlicher Überlappung.

**Textbaustein:**

> Die Auswertung erfolgt an zeitlich geordneten Prognoseursprüngen. Vor jedem Ursprung werden die Verfahren ausschließlich mit den bis dahin zulässigen Beobachtungen neu geschätzt. [PRÜFEN: Festes 104-Wochen-Fenster oder wachsende Historie verbindlich festlegen.] Parameter und primäre Auswertung werden anhand von [PRÜFEN: exakt benannter Entwicklungs-/Validierungsphase] gewählt. Teile der später diskutierten Testperiode wurden bereits explorativ und in früheren Backtests betrachtet; deren Rolle für die Modellentwicklung wird transparent angegeben. Eine vollständig unberührte Testphase wird ohne entsprechenden Nachweis nicht behauptet.

## 7. Evaluationsmetriken, Baselines und Unsicherheit

**Zugeordnete Entscheidungen:** DEC-032, DEC-033, DEC-034; Verbindung zu DEC-028/031.

**Bereits umgesetzt oder historisch nachgewiesen:** MAE/RMSE im Einzellauf; saisonale Tages-/Wochenbaselines, MAPE und MASE im Benchmarkentwurf; frühere exakte Lead-Auswertung und ein historischer gepaarter Verlusttest.

**Dokumentierte Unterschiede:** Der Einzellauf berechnet gepoolten RMSE aus mittlerem Fold-MSE. Ein Mittel aus Fold-RMSE würde allgemein ein anderes Ergebnis liefern. Historischer Benchmark-MAPE-Export gab Prozent aus, aktuelle sktime-Metrik und spätere Darstellung müssen einheitlich festgelegt werden. Die frühere RMSE-Hauptmetrikempfehlung wurde durch MAE im Benchmarkentwurf ersetzt, ohne belegte Begründung.

**Vorhandene Begründungen:** Feinere Lead-Auswertung soll Unterschiede innerhalb der Woche sichtbar machen. Die Zahl mehrerer Metriken und die primäre Auswahl selbst sind nicht ausreichend fachlich begründet.

**Benötigte Literatur:** L1 als vorhandener Bezug. Für ein endgültiges Inferenzverfahren sind die im historischen Code nur genannten Originalarbeiten tatsächlich zu prüfen `[QUELLE ERFORDERLICH]`. Der Codeverweis auf Diebold/Mariano bzw. Giacomini/White ersetzt diese Prüfung nicht.

**Offene methodische Fragen:** Primär MAE oder RMSE? Gepoolte Gewichte und Einheit? MAPE-Nullwertregel und MASE-Nenner? 24-Stunden-Präfix oder exakter h+24-Fehler? Welche Vergleiche sind primär/explorativ? Wie wird zeitliche Abhängigkeit der Verlustdifferenzen berücksichtigt? Welcher praktisch relevante Unterschied soll untersucht werden?

**In der Arbeit anzugeben:** Formeln, Aggregationsebene und Einheiten; gleiche Zielzeitpunkte je Verfahren; Baselineberechnung; Tabellen/Plots nach Lead und gegebenenfalls Teilgruppen; praktische Effektgröße, Unsicherheit und Gültigkeitsbedingungen. Fünf Seeds ersetzen keine unabhängigen Prognoseursprünge.

**Textbaustein:**

> Als primäres Fehlermaß wird [PRÜFEN: fachlich begründete Metrik] vor der abschließenden Auswertung festgelegt. Ergänzend werden [PRÜFEN: festgelegte sekundäre Metriken] sowie Fehler nach Prognoselead berichtet. Der RMSE wird aus den zusammengefassten quadrierten Einzelfehlern berechnet. Die Methoden werden auf denselben Ursprüngen mit saisonalen Naivprognosen verglichen. [PRÜFEN: Ob eine zusätzliche inferenzielle Prüfung erfolgt und wie ihre zeitliche Abhängigkeit berücksichtigt wird.] Nicht überlappende Zielblöcke werden nicht ohne weitere Prüfung als unabhängige Stichproben behandelt.

## 8. Reproduzierbarkeit, Artefakte und Grenzen

**Zugeordnete Entscheidungen:** DEC-005, DEC-011, DEC-012, DEC-027, DEC-035, DEC-036; Verbindungen zu allen daten-/designabhängigen Entscheidungen.

**Bereits vorhanden:** Versionskontrolle, Lockfile, Python-Vorgabe, kleine Featuretests, lokale Datenintegrationstests. R01 dokumentiert nun Hashes der Rohdateien/Panels und zentrale Bibliotheksversionen.

**Dokumentierte Umsetzung:** Silver überspringt existierende Ausgaben, Gold überschreibt sie. Daten sind Git-ignoriert. Historischer Benchmarkexport enthielt Parameter, Paketversionen und Gitstatus; dieser Export fehlt heute. Ein Git-Hash plus `dirty=True` bildet den lokalen Diff nicht vollständig ab.

**Vorhandene Begründungen:** Qualitätsprüfungen sollten verhindern, dass ungültige Daten als Gold gespeichert werden; gemeinsame Schnittstellen sollten die Auswertung vereinheitlichen. Es fehlt eine vollständige implementierte Regel für archivierte Forschungsläufe.

**Benötigte Literatur:** Forschungssoftware- und Datenprovenienzleitlinien `[QUELLE ERFORDERLICH]`. Technische API-Referenzen sollten zur tatsächlich verwendeten Version gehören.

**Offene methodische Fragen:** Hardware/Threads, Konvergenz- und Fehlerprotokolle, dauerhafte Datenversionen, Umgang mit lokalen Änderungen, Pfad/Verfügbarkeit früherer Ergebnisartefakte und Chatquellen. Die lokale Untersuchung belegt keine Hardware früherer Läufe.

**In der Arbeit anzugeben:** Reproduktionsbefehle und ihre Voraussetzungen, aktive Versionen, Daten-/Code-/Konfigurationszuordnung, Seeds, Hardware und Rechenbudget, gespeicherte Einzelprognosen und Diagnostik, tatsächliche Testergebnisse und bekannte Grenzen.

**Textbaustein:**

> Die Softwareumgebung wird durch Projektkonfiguration und uv-Lockdatei beschrieben. Die für einen finalen Lauf verwendeten Daten-, Code- und Konfigurationsstände werden [PRÜFEN: verbindliches Archivierungsschema festlegen] gemeinsam referenziert. Die Bestandsprüfung vom 29.10.2026 ergab zehn bestandene Tests und einen nicht an die neue XGBoost-Architektur angepassten Test. [PRÜFEN: Vor dem finalen Vergleich einen aktuellen Prüfstand, Hardware, Parallelisierung und Umgang mit Schätzfehlern dokumentieren.] Historische Pilotberichte werden von finalen Vergleichsergebnissen getrennt.

## Vorrangige Klärungen

1. **Welche Messgrundlage soll gelten?** Bedeutung von Abdeckung 98 gegenüber 100, Wahl `Value` versus `Value_ScaleTo100`, Lastdefinition, UTC und Intervallanfang anhand der konkreten Exporte bestätigen. Die sechs Korrekturen daran prüfen.
2. **Was ist die endgültige Prognoseaufgabe?** 24 und/oder 168 Stunden, tägliche oder wöchentliche Ursprünge, Erstellungsuhrzeit und tatsächlich verfügbare Lasten festlegen.
3. **Welches Vergleichsdesign ist verbindlich?** Rekursives Einzel-XGBoost oder Seedensemble, DHR-Spezifikation, Fensterlänge, Parameterwahl und Budget bestimmen; ausdrücklich dokumentieren, welche 2025/2026-Ergebnisse bereits gesehen wurden.
4. **Welche Auswertung beantwortet die Forschungsfrage?** Hauptmetrik, Baselines, Aggregation, Leads, Reststunden, Konvergenzfehler und gegebenenfalls abhängigkeitstaugliche Inferenz vor der abschließenden Auswertung festlegen.
5. **Welche Qualitäts- und Provenienznachweise gehören zum finalen Lauf?** Vollständige Gold-Validierung, persistentes Korrekturaudit, Daten-/Codehashes, Konfiguration, Einzelprognosen, aktuelle Tests und Hardware dokumentieren; frühere Ergebnisdateien gegebenenfalls wiederfinden.

## Noch fehlende Begründungen und Literatur nach Priorität

| Bedarf | Konkrete Lücke | Betroffene Entscheidungen |
|---|---|---|
| Mess- und Zeitsemantik | Exportdefinition, Abdeckung/Hochrechnung, Intervallbezug, Revision und Publikationsverzug | DEC-001/002/003/006/007/008/037 |
| Modellwahl | Warum DHR und XGBoost, warum univariat, warum diese Mehrschrittstrategie | DEC-016/017/021/023 |
| Parameter und Merkmale | Lags nach Strategiewechsel, tagesfixierte Mittelwerte, Baumparameter, Harmonische und ARIMA-Ordnung | DEC-018–022/024–026 |
| Design | Finale Horizonte, Fensterlänge, Datumsgrenzen, 13 Validierungswochen, Seeds und Vergleichsbudget | DEC-028–031 |
| Auswertung | Fachliche Hauptmetrik, MAPE-/MASE-Regeln, Aggregation und statistische Abhängigkeit | DEC-032–034 |
| Diagnostik und Reproduzierbarkeit | ADF/MSTL, aktuelle Qualitätsschranken, Audit und Laufarchivierung | DEC-005/009–015/035/036 |

Die vorhandenen Werke L1–L3 sind Ansatzpunkte. Sie ersetzen keine noch fehlende projektspezifische Auswahlbegründung, keinen Nachweis einer unberührten Testphase und keine Bestätigung ungeklärter Exportsemantik.

