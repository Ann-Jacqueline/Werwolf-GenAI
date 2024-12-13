# Ziel der Simulation
- Das Ziel ist es, automatisch Werwolf-Spiele zu simulieren, um Daten für das Training der Multi-Agenten-Modelle zu generieren.
- Diese simulierten Spiele liefern wichtige Datensätze wie:
- Spielzustände -> Game_States
- Agentenentscheidungen -> GPT Outputs 
- Diskussionslogs
- Voting-Ergebnisse  
- Spielzusammenfassungen -> Round Summaries

##  Bestandteile des Game Environments

#### a) Game Controller (Orchestrator)
- Aufgabe: Verwaltet das gesamte Spiel und überwacht alle Aktionen.
- Funktion: Startet neue Phasen (Tag/Nacht), initiiert die Spielrunden und aktualisiert den Spielstatus.
- Verbindung: Interagiert mit dem Persistent und Tentative Global History Model.

#### b) Agenten-Modelle
- Aufgabe: Agieren als eigenständige Spieler.
- Funktion: Generieren basierend auf den Spielzuständen und ihrer spezifischen Rolle (Werwolf, Dorfbewohner etc.) Entscheidungen und Aktionen.

- 
#### c) Game State Management
- Persistent Game State: Speichert permanente Spielzustände wie vergangene Runden, eliminierte Spieler und strategische Notizen.
- Tentative Game State: Speichert temporäre Informationen, wie aktuelle Diskussionslogs, Agentenausgaben und Beobachtungen während einer Spielrunde.

#### d) Voting & Elimination System
- Aufgabe: Verarbeitet Diskussionslogs und stimmt basierend auf den Vorschlägen ab.
- Funktion: Generiert die Abstimmungsergebnisse, eliminiert Spieler und speichert die Ergebnisse im Persistent Game State.

#### e) Logger & Dataset Collector
- Aufgabe: Speichert automatisch alle relevanten Aktionen, Entscheidungen und Ergebnisse.
- Funktion: Erzeugt strukturierte Datensätze, die für das Training exportiert werden.


##  Workflow der Simulation

####  1. Spielstart durch den Orchestrator
- Initialisiert das Spiel mit zufälliger Rollenzuweisung und erzeugt einen initialen Spielzustand.
- 
#### 2.Nachtphase – Simulation
- Die Werwölfe werden aktiviert und fällen Entscheidungen.
- Aktionen wie Amor, Seherin und Hexe werden simuliert.
- Datenaufzeichnung: Aktionen und Ergebnisse werden im Tentative Game State protokolliert.


#### 3.Tagphase – Simulation
- Diskussion zwischen Agenten wird simuliert.
- GPT-API-Aufrufe: Generieren Ausgaben und simulieren Gespräche. (Fehlt noch / Tenetative Llama API?)
- Voting-Entscheidungen werden getroffen.


#### 4. Abstimmung und Eliminierung
- Voting-Modell entscheidet über die Eliminierung.
- Zusammenfassung Summary wird erstellt und im persistent Game State gespeichert.


#### 5. Endrunde
- Wenn die Siegbedingungen erfüllt sind, wird das Spiel beendet.
- Datenexport: Alle Aktionen, Entscheidungen und Logs werden für das Training gespeichert.



### Technische Implementierung
##### a) Simulations-Framework
- Python-Skripte: Steuern die Simulation.
- API-Aufrufe: Integrieren GPT-4 für dynamische Textgenerierung.
- Logging-System: Speichert relevante Aktionen und Statusänderungen.
##### b) Datenexport für das Training
- Speicherung in JSON-, CSV- oder SQL-Datenbanken.
- Automatisierte Datensätze: Enthalten Agenten-Ausgaben, Diskussionen und Abstimmungen.
- Datensatzaufbau: Geeignet für Reinforcement Learning und strategische Trainingsszenarien.

#### Vorteile der Simulation
- Automatische Datenerstellung: Kein manuelles Spielen erforderlich.
- Vielfältige Datensätze: Unterschiedliche Spielszenarien für robustes Modelltraining.
- Skalierbarkeit: Unbegrenzte Spielsimulationen für massiven Datensatzaufbau.
#### Nächste Schritte
- Simulationsskript erstellen: Für Spielinitiation, Phasenmanagement und Agentenaktionen.
- Automatisierte API-Aufrufe: Für Textgenerierung durch GPT-4.
- Datenmanagement & Speicherung: Für die Datenbeschaffung und das Training.