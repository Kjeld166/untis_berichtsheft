# WebUntis Berichtsheft Export

Dieses Python-Skript liest Unterrichtsstunden und eingetragene Unterrichtsthemen aus der WebUntis-Weboberfläche aus und speichert sie als CSV. Die Anmeldung erfolgt manuell im geöffneten Browser; das Skript speichert keine WebUntis-Zugangsdaten.

## Voraussetzungen

- Python 3.10 oder neuer
- Ein WebUntis-Zugang und die URL deiner Schule
- Microsoft Edge oder ein von Playwright installierter Chromium-Browser
- Bei Netzwerkzugriff über einen Proxy: die Proxy-Adresse

## Installation

Repository herunterladen oder klonen und in den Projektordner wechseln. Danach eine virtuelle Umgebung anlegen und Abhängigkeiten installieren.

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### Git Bash oder andere Bash-Shell

```bash
python -m venv .venv
source .venv/Scripts/activate
python -m pip install -r requirements.txt
```

Falls kein passender Browser auf dem Rechner installiert ist, kann Playwright Chromium installieren:

```powershell
python -m playwright install chromium
```

## Export starten

Passe URL, Schuljahr-ID und Zeitraum an deine Schule an. Die URL ist die Basisadresse deiner WebUntis-Instanz, zum Beispiel `https://meine-schule.webuntis.com`. Die Schuljahr-ID findest du in WebUntis beziehungsweise in den API-Anfragen deiner Instanz.

### Ohne Proxy

```powershell
python .\webuntis_browser_export.py --url "https://meine-schule.webuntis.com" --start 2026-08-31 --weeks 4 --year-id 30 --output unterricht.csv
```

### Mit Proxy

Der Proxy kann direkt beim Aufruf angegeben werden:

```powershell
python .\webuntis_browser_export.py --url "https://meine-schule.webuntis.com" --start 2026-08-31 --weeks 4 --year-id 30 --output unterricht.csv --proxy "http://proxy.example:80"
```

Alternativ lässt sich der Proxy für die aktuelle Shell-Sitzung als Umgebungsvariable setzen.

PowerShell:

```powershell
$env:HTTP_PROXY = "http://proxy.example:80"
$env:HTTPS_PROXY = "http://proxy.example:80"
python .\webuntis_browser_export.py --url "https://meine-schule.webuntis.com" --start 2026-08-31 --weeks 4 --year-id 30 --output unterricht.csv
```

Git Bash:

```bash
export http_proxy=http://proxy.example:80
export https_proxy=http://proxy.example:80
python webuntis_browser_export.py --url "https://meine-schule.webuntis.com" --start 2026-08-31 --weeks 4 --year-id 30 --output unterricht.csv
```

Das Skript öffnet WebUntis im Browser. Melde dich dort an und drücke danach im Terminal Enter. Die Proxy-Angabe muss gegebenenfalls durch die Proxy-Adresse des eigenen Netzwerks ersetzt werden.

## Optionen

- `--url`: WebUntis-Basisadresse; alternativ `WEBUNTIS_URL`
- `--start`: beliebiger Tag der ersten Schulwoche im Format `YYYY-MM-DD`
- `--weeks`: Anzahl aufeinanderfolgender Wochen
- `--year-id`: Schuljahr-ID; alternativ `WEBUNTIS_YEAR_ID`
- `--output`: Zieldatei für die CSV
- `--proxy`: Proxy-Server, zum Beispiel `http://proxy.example:80`; alternativ `HTTP_PROXY` oder `HTTPS_PROXY`
- `--profile-dir`: lokaler Ordner für die Browser-Login-Sitzung

Alle Optionen können mit `python webuntis_browser_export.py --help` angezeigt werden. Die Standardwerte für URL und Schuljahr-ID beziehen sich auf die ursprüngliche Installation und sollten für andere Schulen angepasst werden.

## Exportregeln und Ergebnis

Stunden ohne eingetragenes Unterrichtsthema werden ausgelassen. Falls WebUntis eine Stunde mehrfach mit demselben Datum sowie derselben Start- und Endzeit liefert, wird sie nur einmal exportiert. Ein Zeitblock mit Thema bleibt dabei gegenüber einem ansonsten identischen Eintrag ohne Thema erhalten.

Die CSV enthält Datum, Wochentag, Fach, Beginn, Ende und Unterrichtsthema. Sie wird als UTF-8 mit BOM gespeichert und kann beispielsweise mit Excel geöffnet werden. Der Export nennt pro Woche, wie viele leere Themen und Dubletten ausgelassen wurden.

## Tests

```powershell
python -m pytest -q
```

## Datenschutz und GitHub

Die CSV-Datei kann persönliche Unterrichtsdaten enthalten und wird deshalb nicht versioniert. Auch virtuelle Umgebungen und lokale Testdateien sind per `.gitignore` ausgeschlossen. Prüfe vor dem Hochladen immer, dass keine Zugangsdaten, persönlichen CSV-Exporte oder lokalen Konfigurationsdateien enthalten sind.

## Lizenz

MIT. Siehe [LICENSE](LICENSE).
