# Census Münzexport

## Über dieses Projekt

Timo Strauch hat das Census-LOD-Team gebeten für Wolfram Zieger von ATOS einen Export der in den Erfurter Strada-Bänden beinhalteten Münzen vorzubereiten. Da es über den Exporter der easydb 4 zu kompliziert schien, wurde dieses Python-Projekt aufgesetzt, um den Export zu erzeugen. Der Output erfolgt als XML.

Genaue Anforderungen siehe https://redmine.bbaw.de/issues/10232. Weitere Abklärungen dazu erfolgten per Mail u.ä.

## Remotes

* git.bbaw.de: @git.bbaw.de:/git/census/census_api.git@
* "Gitea":https://telotawebdev.bbaw.de/gitea/telota/census-muenzexport

## Voraussetzung

* (getestet mit) Python 3.6.5
* Es wird davon ausgegangen, dass die PostgresQL-Datenbank bereits eingerichtet ist.

## Klonen

Das Repository kann geklont werden mit:

<pre><code class="bash">
git clone git.bbaw.de:/git/census/census_api.git
</code></pre>

## Installation mit pipenv

Falls noch nicht geschehen, sollte @pipenv@ installiert werden:

<pre><code class="bash">
pip install --user pipenv
</code></pre>

Im Projektverzeichnis kann dann die virtuelle Python-Umgebung installiert und geladen werden:

<pre><code class="bash">
pipenv install
pipenv shell
</code></pre>

Nun ist die Umgebung mit allen Abhängigkeiten geladen. @python@ lädt nun nun nicht mehr einfach den Systeminterpreter, sondern den der virtuellen Umgebung.

## Einrichtung des Skripts

Im Verzeichnis @config@ liegt die Datei @env.example.py@. Diese im selben Ordner kopieren zu @env.py@. Darin die Angaben für deine Datenbankverbindung eintragen.

<pre><code class="python">
DB_HOST = "localhost"
DB_PORT = 5432
DB_DATABASE = "easydb-census"
DB_USERNAME = "user"
DB_PASSWORD = ""
</code></pre>

(Port scheint ein Default-Postgres-Port zu sein, ist aber irrelevant, d.h. wird nicht abgefragt)

## Ausführen

Das Skript kann mit Python ausgeführt werden:

<pre><code class="bash">
python src/muenzexport.py
</code></pre>

Der Output wird im Verzeichnis @out/@ hinterlegt.

## Weiteres

*Aufbau des Repos*

Das eigentlich Skript ist genau eine Datei: @src/muenzexport.py@

Alle Angaben zu den abzufragenden Objekten sind in einer csv-Datei abgelegt und werden vom Prozess dort rausgezogen.

In @sql/@ liegen vorformulierte Beispielanfragen für die verschiedenen Hierarchiestufen (für Testen und Debuggen der Anfragen, um sie dann in das Hauptskript zu kopieren).
Die Anfragen in dem Ordner sind nicht direkt ins Hauptskript @muenzexport.py@ eingebunden.

@out@-Verzeichnis: Dort liegen die resultierenden XML.

*Algorithmus (Grundaufbau)*

* Hole Objektinfos aus csv.
* Starte mit den csv-Infos eine SQL-Abfrage und lege den Output in ein python-Objekt (key-value-Paare).
* Starte mit weiteren Infos aus csv eine weitere SQL-Abfrage und lege den Output in ein weiteres python-Objekt.
* ggf. usw. ...
* Wenn alle benötigten Infos in python-Objekten sind, erstelle aus diesen Objekten eine Baum-Struktur, indem du bei den untersten Blättern beginnst und die Objekte mit "append" ineinander einfügst, bis du dich zur Wurzel hochgearbeitet hast.
* Wenn das Baum-Python-Objekt komplett ist, wandle es in XML um.
* Schreibe das xml in das Output-Verzeichnis.

*Code-Erklärungen*

"etree":https://docs.python.org/2/library/xml.etree.elementtree.html (XML-Library für Python)
.text = Inhalt eines XML-Elements