# WebUntis Berichtsheft Export

Ein kleines Projekt zum Export von Stunden aus WebUntis als CSV-Datei, damit Informationen zu Datum, Fach, Uhrzeit und Unterrichtsthema einfach weiterverarbeitet werden können.

## Inhalt dieses Ordners

- `webuntis_browser_export.py` – Hauptscript für den Browser-Export
- `requirements.txt` – benötigte Python-Abhängigkeiten
- `.env.example` – Beispiel für Umgebungsvariablen
- `LICENSE` – Lizenzinformationen
- `PRIVACY.md` – Datenschutzerklärung

## Voraussetzungen

- Python 3
- WebUntis-Zugang
- Internetzugang
- lokaler Browser mit WebUntis-Login

## Schnellstart

```powershell
python -m pip install -r requirements.txt
python webuntis_browser_export.py --start 2026-08-31 --weeks 4 --year-id 30 --output webuntis_4_wochen_export.csv
```

Das Skript öffnet WebUntis im Browser, du meldest dich dort manuell an und bestätigst danach in der Konsole mit Enter. Anschließend wird die CSV-Datei erstellt.

## Beispiel für die CSV-Ausgabe

```csv
date,weekday,subject,start,end,lesson_topic
2026-08-31,Montag,KL,07:15,08:45,Belehrungen
2026-08-31,Montag,eth1,09:15,10:45,Klassischer Utilitarismus Bentham
```

## Hinweis

Die Datei wird als UTF-8 mit BOM gespeichert. Das Projekt ist für den schulischen Gebrauch gedacht und wurde als praktische Lösung für Berichtshefte bzw. Auswertungen entwickelt.

## Lizenz

Das Projekt steht unter der MIT-Lizenz. Weitere Informationen findest du in der Datei `LICENSE`.
