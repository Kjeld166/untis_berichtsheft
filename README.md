# WebUntis Berichtsheft Export

Mit diesem Programm kannst du deine eingetragenen WebUntis-Unterrichtsthemen als CSV-Datei exportieren. Die Anmeldung erfolgt mit deinem privaten WebUntis-Konto direkt im Browser. Das Programm speichert dein Passwort nicht.

Die fertigen Dateien enthalten persönliche Schul- und Unterrichtsdaten. Teile sie nicht öffentlich und lade keine CSV- oder TXT-Exporte auf GitHub hoch.

## Was du bekommst

- eine CSV-Datei mit Datum, Wochentag, Fach, Uhrzeit und Thema
- wahlweise eine TXT-Datei nach der Vorlage `formart.txt`
- keine Speicherung von Benutzername oder Passwort
- eine lokale Browser-Sitzung in deinem Windows-Benutzerprofil

## Voraussetzungen

Du brauchst:

- Windows
- Microsoft Edge oder einen von Playwright installierten Chromium-Browser
- Python 3.10 oder neuer
- dein privates WebUntis-Benutzerkonto
- die WebUntis-Adresse deiner Schule
- gegebenenfalls die Proxy-Adresse deiner Schule oder deines Netzwerks

## 1. Projekt herunterladen

1. Öffne die GitHub-Seite dieses Projekts.
2. Klicke oben rechts auf **Code**.
3. Klicke auf **Download ZIP**.
4. Entpacke die ZIP-Datei in einen normalen Ordner, zum Beispiel `Dokumente`.
5. Öffne den entpackten Projektordner.

Alternativ kannst du das Projekt in GitHub Desktop oder mit Git herunterladen.

## 2. Python installieren

Wenn Python noch nicht installiert ist:

1. Öffne https://www.python.org/downloads/
2. Lade die neueste Windows-Version herunter.
3. Starte die Installation.
4. Aktiviere **Add Python to PATH**.
5. Wähle **Install Now**.

Prüfe danach in PowerShell:

```powershell
python --version
```

## 3. Terminal im Projektordner öffnen

1. Öffne den entpackten Projektordner.
2. Klicke oben in die Adresszeile des Explorers.
3. Gib `powershell` ein und drücke Enter.

Alternativ kannst du mit der rechten Maustaste in den Ordner klicken und **Terminal öffnen** wählen.

Alle folgenden Befehle müssen im Projektordner ausgeführt werden.

## 4. Virtuelle Umgebung erstellen und aktivieren

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Wenn PowerShell die Ausführung blockiert, einmalig für die aktuelle Sitzung erlauben:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Am Anfang der Eingabezeile sollte jetzt `(.venv)` stehen.

## 5. Abhängigkeiten installieren

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m playwright install chromium
```

Eine andere Möglichkeit ist Playwrights Chromium-Browser zusammen mit Microsoft Edge zu verwenden. Das Programm sucht zuerst nach Microsoft Edge und verwendet diesen Browser, sofern verfügbar.

## 6. Persönliche WebUntis-Daten vorbereiten

Drei Werte musst du gegebenenfalls anpassen:

- `--url`: die Adresse deiner WebUntis-Schule
- `--start`: Montag oder ein beliebiger Tag der ersten gewünschten Schulwoche
- `--year-id`: die Schuljahr-ID deiner Schule

Für die hier verwendete Schule lautet die Adresse:

```text
https://bszet.webuntis.com
```

Für eine andere Schule ersetzt du sie durch deine eigene WebUntis-Adresse.

Die Schuljahr-ID ist keine Passworteinstellung. Sie wird für die API-Abfrage benötigt. Das Standardprogramm verwendet zunächst `30`. Wenn deine Schule einen anderen Wert verwendet, übergibst du ihn mit `--year-id <ID>`.

## 7. Proxy einstellen

Nur verwenden, wenn dein Netzwerk einen Proxy verlangt.

PowerShell:

```powershell
$env:HTTP_PROXY="http://proxy.example.de:80"
$env:HTTPS_PROXY="http://proxy.example.de:80"
```

Der Proxy kann auch direkt beim Aufruf angegeben werden:

```powershell
python .\webuntis_browser_export.py --proxy "http://proxy.example.de:80"
```

## 8. Schüleransicht verwenden

Dies ist die empfohlene Ansicht für dein privates Benutzerkonto:

```powershell
python .\webuntis_browser_export.py --timetable-view my-student --start 2026-10-26 --weeks 4 --output export.csv
```

Die Ansicht `my-student` öffnet für den ersten Tag zum Beispiel:

```text
https://bszet.webuntis.com/timetable/my-student?date=2026-10-26
```



## 9. Mit deinem privaten Konto anmelden

1. Das Programm öffnet Microsoft Edge oder Chromium.
2. Melde dich dort mit deinem privaten WebUntis-Benutzernamen und deinem privaten Passwort an.
3. Warte, bis die Stundenplanseite vollständig geladen ist.
4. Kehre zum Terminal zurück.
5. Drücke dort Enter.

Das Programm schreibt dein Passwort nicht in eine Datei und verwendet es nicht als Kommandozeilenparameter.

## 10. Zeitraum ändern

`--start` bedeutet den ersten Tag der gewünschten ersten Woche. Es kann Montag oder ein beliebiger anderer Tag dieser Woche sein. Das Programm beginnt immer mit dem Montag dieser Woche.

Beispiel für acht Wochen ab dem 26. Oktober 2026:

```powershell
python .\webuntis_browser_export.py --timetable-view my-student --start 2026-10-26 --weeks 8 --output berichtsheft.csv
```

## 11. Andere WebUntis-Adresse verwenden

```powershell
python .\webuntis_browser_export.py --url "https://DEINE-SCHULE.webuntis.com" --timetable-view my-student --start 2026-10-26 --weeks 4 --year-id 30 --output export.csv
```

Ersetze `DEINE-SCHULE.webuntis.com` durch deine eigene Adresse.
Am BSZET lautet die Adresse zum Beispiel: ```https://bszet.webuntis.com/```

```text

## 12. TXT-Datei nach Vorlage erstellen

Am besten die CSV-Datei in KI einfügen und Fromatierung erstellen lassen. Dafür bietet sich die format.md als hilfestellung an, diese ist an die IHK-Forlage ausgerichtet**

Die Vorlage befindet sich in `formart.md`. Fachkürzel werden dort bereits in lange Namen umgewandelt, zum Beispiel:

- `eng1` → Englisch
- `MA1` → Mathematik
- `DIT06` → LF06
- `rus1` → Russisch

Für Russisch zeigt das Programm den Originaltext und kann bekannte Übersetzungen in Klammern ergänzen.

## Alle Optionen anzeigen

```powershell
python .\webuntis_browser_export.py --help
```

Wichtige Optionen:

- `--url`: WebUntis-Basisadresse
- `--start`: erster gewünschter Zeitraumstag im Format `YYYY-MM-DD`
- `--weeks`: Anzahl aufeinanderfolgender Wochen
- `--year-id`: Schuljahr-ID
- `--output`: Name der CSV-Ausgabedatei
- `--timetable-view`: `my-student` oder `my-class`
- `--translate-russian`: russische Themen optional mit LibreTranslate übersetzen
- `--proxy`: Proxy-Adresse
- `--profile-dir`: eigener Browser-Profilordner

## Exportregeln

- Stunden ohne eingetragenes Unterrichtsthema werden nicht exportiert.
- Dieselbe Stunde mit Datum, Start- und Endzeit wird nur einmal ausgegeben.
- Ein Eintrag mit Thema wird einem leeren Eintrag vorgezogen.
- Die CSV wird als UTF-8 mit BOM gespeichert.
- Die CSV kann in Excel geöffnet werden.

## Häufige Fehler

### `ModuleNotFoundError: No module named 'requests'`

Die virtuelle Umgebung wurde nicht vorbereitet oder die Abhängigkeiten fehlen.

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Wenn die virtuelle Umgebung beschädigt ist:

```powershell
Remove-Item -Recurse -Force .venv
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m playwright install chromium
```

### `RequestsDependencyWarning`

Die Abhängigkeit `charset-normalizer` oder `chardet` fehlt. Installiere die Requirements erneut:

```powershell
python -m pip install --upgrade -r requirements.txt
```

### `DLL load failed ... greenlet`

Das Problem kann durch eine beschädigte virtuelle Umgebung entstehen. Erstelle die Umgebung neu.

Wenn die virtuelle Umgebung unter einem sehr langen Windows-Pfad Probleme macht, kann das Programm auch mit dem normalen Python-Interpreter gestartet werden:

```powershell
C:/Program Files/Python314/python.exe .\webuntis_browser_export.py --timetable-view my-student --start 2026-10-26 --weeks 4 --output export.csv
```

Zuerst müssen die Abhängigkeiten für diesen Interpreter installiert werden:

```powershell
C:/Program Files/Python314/python.exe -m pip install -r requirements.txt
C:/Program Files/Python314/python.exe -m playwright install chromium
```

### HTTP 403

HTTP 403 bedeutet meistens:

- du bist noch nicht richtig angemeldet
- dein Konto darf diese Ansicht nicht verwenden
- die Schuljahr-ID stimmt nicht
- die Klassenansicht `my-class` wird von deinem Konto nicht unterstützt

Dann zuerst mit `my-student` testen:

```powershell
python .\webuntis_browser_export.py --timetable-view my-student --start 2026-10-26 --weeks 4 --output export.csv
```

### Browser bleibt leer oder Anmeldung klappt nicht

- Browser vollständig schließen
- Programm erneut starten
- Anmeldung erneut durchführen
- den Profilordner gegebenenfalls löschen oder mit `--profile-dir` einen neuen Ordner verwenden

## Tests

```powershell
python -m pytest -q
```

## Datenschutz

- Das Programm speichert keine Zugangsdaten.
- Die Browser-Sitzung wird lokal im Profilordner gespeichert.
- CSV- und TXT-Dateien können persönliche Schul- und Unterrichtsdaten enthalten.
- Diese Dateien nicht auf GitHub hochladen.
- Vor einem Commit immer prüfen, dass keine Exportdateien, Browserprofile oder Zugangsdaten enthalten sind.

## Lizenz

MIT. Siehe `LICENSE`.
