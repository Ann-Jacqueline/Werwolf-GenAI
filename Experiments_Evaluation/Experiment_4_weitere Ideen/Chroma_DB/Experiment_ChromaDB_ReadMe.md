# Experiment 3: ChromaDB Integration

## Aufbau der Komponenten und Funktionalität

Im Rahmen von Experiment 3 wurde **ChromaDB** als nicht-relationale Datenbanklösung evaluiert. Der Aufbau und die Funktionalität gliederten sich in folgende Komponenten:

1. **Datenbank-Client**:
   - **ChromaDB-Client** wurde mit `duckdb+parquet` als Implementierung konfiguriert.
   - Daten wurden persistent im Verzeichnis `./chroma_storage` gespeichert.

2. **Sammlungen**:
   - **Agents Collection**: Verwaltung der Agentendaten (z. B. Rollen, Namen).
   - **Events Collection**: Speicherung von Spielereignissen mit Informationen zu Runden und Wichtigkeit.
   - **Game State Collection**: Speicherung von Spielzuständen (z. B. verbleibende Spieler, Spielphase).

3. **GameController**:
   - Verwaltung der gesamten Spielabläufe, einschließlich:
     - **Agenten-Registrierung**: Speichern von Rollen und Namen in der Datenbank.
     - **Rolleninitialisierung**: Zufällige Zuweisung von Spielerrollen.
     - **Spielzustandsspeicherung**: Persistente Speicherung des aktuellen Spielstatus.
     - **Ereignisprotokollierung**: Speicherung wichtiger Spielereignisse mit Gewichtung.
     - **Phasenmanagement**: Implementierung der Nacht- und Tagphasen.

## Spielflow

Der Spielflow folgte einem klaren Schema:
1. Initialisierung der Agenten und Zuweisung von Rollen.
2. Verwaltung der Spielphasen, einschließlich:
   - Nachtphase: Aktionen der Werwölfe, wie das Eliminieren eines Spielers.
   - Tagphase: Diskussionen und Abstimmungen unter den Spielern.
3. Protokollierung und Überwachung des Spielverlaufs über die Datenbank.
4. Persistente Speicherung aller relevanten Daten in den entsprechenden ChromaDB-Sammlungen.

## Gründe warum wir uns gegen ChromaDB entschieden haben

Nach der Implementierung und Evaluierung der ChromaDB-Lösung haben wir uns entschieden, diese nicht weiter zu verwenden. 
Die Entscheidung wurde aus folgenden Gründen getroffen:

1. **Schwierigkeiten mit der Verwaltung einer nicht-relationalen Datenbank**:
   - Die Abwesenheit echter SQL Queries erschwerte das Monitoring und die Verwaltung der Daten.
   - Komplexe Abfragen und Analysen der Daten waren im Vergleich zu relationalen Datenbanken umständlicher.

2. **Probleme mit dem Chroma-Setup**:
   - Chroma hatte Probleme `chroma migrate`auszuführen, aber brauchte es um richtig zu funktionieren also waren wir da, setup-technisch blockiert.
   - Probleme mit der Speicherdatei (`storage file`) traten auf, wodurch wir die Komponenten nicht richtig verwenden konnten.

## Fazit

Aufgrund dieser Herausforderungen haben wir beschlossen, die ChromaDB-Integration nicht weiterzuverfolgen. 
Stattdessen werden haben wir uns für eine SQLite 3 Datenbank entschieden, da sie in PyCharm intergiert ist und wir mit ihr besseres Monitoring und Query Searches machen können.