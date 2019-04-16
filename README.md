# Census Münzexport

## Voraussetzung

* (getestet mit) Python 3.6.5
* Es wird davon ausgegangen, dass die PostgresQL-Datenbank bereits eingerichtet ist.

## Installation mit pipenv

Falls noch nicht geschehen, sollte `pipenv` installiert werden:

```bash
pip install --user pipenv
```

Im Projektverzeichnis kann dann die virtuelle Python-Umgebung installiert und geladen werden:

```bash
pipenv install
pipenv shell
```

Nun ist die Umgebung mit allen Abhängigkeiten geladen. `python` lädt nun nun nicht mehr einfach den Systeminterpreter, sondern den der virtuellen Umgebung.

## Einrichtung des Skripts

Im Verzeichnis `config` liegt die Datei `env.example.py`. Diese im selben Ordner kopieren zu `env.py`. In dieser Datei wird die Datenbankverbindung gespeichert. 

```
DB_HOST = "localhost"
DB_PORT = 5432
DB_DATABASE = "easydb-census"
DB_USERNAME = "user"
DB_PASSWORD = ""
```

## Ausführen

Das Skript kann mit Python ausgeführt werden:

```
python src/muenzexport.py
```

Der Output wird im Verzeichnis `out?` hinterlegt.

## Weiteres

In `sql/` liegen vorformulierte Beispielanfragen für die verschiedenen Hierarchiestufen. 
Die Anfragen in dem Ordner sind nicht direkt ins Hauptskript `muenzexport.py` eingebunden.