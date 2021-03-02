# Census Münzexport

## Über dieses Projekt

Ursprünglich sollten aus einem SQL-Export der Datenbank unter http://www.census.de/ die in den Erfurter Strada-Bänden beinhalteten Münzen extrahiert werden. Später gab es immer wieder ähnliche Anfragen für spezifische Datenexporte  an das Census-Team. Da es über den Exporter der easydb 4 zu kompliziert schien, wurde dieses Python-Projekt aufgesetzt, um solche Exporte zu erzeugen. Der Output erfolgt als XML.

Die ursprünglichen Anforderungen für die Datenextraktion lauteten:
* Finde alle dritten Kinder vom Wien-Dok (alle vierten Kinder vom Gotha-Dok), die mit einem Monument verlinkt sind. Gib jedes Dokument einmal aus, mit den IDs aller verlinkten Monumente.
* Perspektivisch: Je erstem Kind dieser zwei Doks eine extra XML-Datei erzeugen.
* Am besten wäre, wenn alles nach der ersten Angabe ("name") sortiert wäre. Dazu ist es wohl notwendig, nicht nach der allerobersten ID in Wien bzw. Gotha zu suchen, die alle Einzelbände zusammenfasst, sondern nach den nächsttieferen IDs der einzelnen Bände, denn für die wird es ja getrennte XML-Volltexte geben, außerdem werden nur so Dopplungen bzw. Probleme beim Sortieren wegen gleichlautenden "names" ausgeschlossen.
* Benötigte Felder:
"name" aus "cs_document"; zugehörige "id" mit Präfix "CensusID"; "id" des verlinkten Monuments aus "cs_monument" mit Präfix "CensusID"; zugehöriger "label_name" (ggf. fortlaufend "id" und "label_name" weiterer verlinkter Monumente)
* D.h. mehrere Exporte mit jeweils indivdueller "Ausgangs-ID". 

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

## License

This repository is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

The developers are in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

See http://www.gnu.org/licenses/.

## Credits

© 2018-2020 by Berlin-Brandenburg Academy of Sciences and Humanities

Developed by TELOTA, a DH working group of the Berlin-Brandenburg Academy of Sciences and Humanities http://www.bbaw.de/telota telota@bbaw.de. Lead Developer: Oliver Pohl
