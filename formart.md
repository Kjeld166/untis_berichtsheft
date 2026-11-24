# Stoffplan-Format (kompakt)

## Ausgabeformat

```text
{weekday}, {date}

{subject}: {zusammenfassung}
{subject}: {zusammenfassung}
{subject}: {zusammenfassung}
...
```

## Beispiel

```text
Montag, 26.10.2026

Englisch: Sustainable Lifestyle, Sportsucht, Adverbien, Schreibaufgabe
Ethik: Präferenzutilitarismus nach Singer
LF11: Aktivitätsdiagramme
Deutsch: Stilmittel, Iphigenie, Klassik


Dienstag, 27.10.2026

LF06: Grundlagen Marketing
Englisch: Stellungnahme zu Nile Wilson und Sportlererfahrungen
Russisch: LK nachholen, verbessern und auswerten
Mathematik: Augenblicksgeschwindigkeit und Differentialquotient
```

## Fachzuordnung

| Kürzel | Ausgabe |
|----------|----------|
| eng1 | Englisch |
| eth1 | Ethik |
| deu1 | Deutsch |
| rus1 | Russisch |
| MA1 | Mathematik |
| phy1 | Physik |
| spo1 | Sport |
| ggk1 | Gemeinschaftskunde |
| lit1 | Literatur |
| kun1 | Kunst |
| DIT06 | LF06 |
| DIT07 | LF07 |
| DIT08 | LF08 |
| DIT09 | LF09 |
| DIT10 | LF10 |
| DIT11 | LF11 |

## Regeln

- Wochentag und Datum immer anzeigen.
- Eine Zeile pro Fach.
- Keine Uhrzeiten.
- Keine Leerzeilen zwischen Fächern.
- DIT-Fächer in LF-Fächer umwandeln.
- Russisch-Themen ins Deutsche übersetzen.
- Keine HTML-Tags ausgeben.
- Keine abgeschnittenen Wörter.
- Keine `...`.
- Themen semantisch zusammenfassen.
- Die wichtigsten Lerninhalte müssen erhalten bleiben.
- Zielwert: maximal ca. 75 Zeichen pro Fachzeile.
- Wenn mehr Platz benötigt wird, sinnvolle Zusammenfassung statt Abschneiden.
- Prüfungsthemen, Leistungskontrollen und Klausuren besonders hervorheben.

## Zusammenfassungsprinzip

**Schlecht**

```text
Gemeinschaftskunde: Vortrag zum Politikzyklus. Methodentraining zur Klausurvorbereitung: Analys
```

**Gut**

```text
Gemeinschaftskunde: Politikzyklus, Klausurvorbereitung, Darstellungsanalyse
```

**Schlecht**

```text
Literatur: Textkonzeption für eine Kurzgeschichte zum Thema 'Generationenkonflikt'/Ste
```

**Gut**

```text
Literatur: Kurzgeschichte zum Generationenkonflikt planen
```