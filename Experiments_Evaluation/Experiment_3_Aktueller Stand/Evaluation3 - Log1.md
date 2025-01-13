
# Werwolf-Backendbeschreibung



# Werwolf-Frontendbeschreibung



# Werwolf-Datenbankbeschreibung

Die Datenbank dient der Verwaltung eines Werwolf-Spiels und speichert Informationen über Spiele, Phasen, Spieler und deren Interaktionen. Die Entitäten und deren Attribute sind wie folgt:
---

## Game (Spiel)
Diese Tabelle speichert Informationen über jedes Spiel.

- **game_id**: Eine eindeutige Identifikation für jedes Spiel. Wird mit dem Start jedes Spiels generiert.
- **title**: Der Titel des Spiels, z. B. "Werwolf Game 1".
- **started_at**: Zeitstempel, wann das Spiel gestartet wurde.
- **ended_at**: Zeitstempel, wann das Spiel beendet wurde.
- **winner_role**: Die gewinnende Rolle, z. B. "Werwölfe" oder "Dorfbewohner".
- **num_players**: Die Gesamtanzahl der Spieler, die an diesem Spiel teilnehmen. Muss bevor Start ausgefüllt werden.

---

## Player (Spieler)
Diese Tabelle verwaltet alle Spieler des Spiels.

- **player_id**: Eine eindeutige Identifikation für jeden Spieler.
- **game_id**: Verweis auf das Spiel, zu dem der Spieler gehört.
- **player_name**: Der Name des Spielers (menschlich oder KI-generiert).
- **player_role**: Die zugewiesene Rolle des Spielers, z. B. "Werwolf", "Dorfbewohner".
- **eliminated_at_phase**: Die Phase, in der der Spieler eliminiert wurde, falls zutreffend.
- **is_human**: Boolean-Wert, der angibt, ob der Spieler ein Mensch ist (True/False). Wer einen menschlichen Namen hat, ist automatisch human.

---

## Phase
Diese Tabelle speichert Details zu den einzelnen Phasen eines Spiels.

- **phase_id**: Eine eindeutige Identifikation für jede Phase.
- **game_id**: Verweis auf das Spiel, zu dem die Phase gehört.
- **phase_name**: Name der Phase, z. B. "Tag" oder "Nacht".
- **eliminated_player_id**: Verweis auf den Spieler, der in dieser Phase eliminiert wurde.

---

## Phase_Eliminations
Diese Tabelle dokumentiert die Eliminierungen während der Phasen.

- **elimination_id**: Eine eindeutige Identifikation für jede Eliminierung.
- **phase_id**: Verweis auf die Phase, in der die Eliminierung stattgefunden hat.
- **eliminated_player_id**: Verweis auf den eliminierten Spieler.

---

## Prompt_Responses
Diese Tabelle speichert die Eingaben und Antworten während des Spiels.

- **id**: Eine eindeutige Identifikation für jede Eingabe/Ausgabe.
- **game_id**: Verweis auf das zugehörige Spiel.
- **phase_id**: Verweis auf die Phase, in der die Eingabe/Ausgabe erfolgt ist.
- **player_id**: Verweis auf den Spieler, der die Eingabe gemacht hat (oder NULL, wenn es der Moderator ist).
- **prompt**: Die gestellte Frage oder Eingabe.
- **response**: Die Antwort auf die Eingabe.
- **created_at**: Zeitstempel, wann die Eingabe/Ausgabe erstellt wurde.

---

## Zusammenfassung
Die Struktur ermöglicht eine umfassende Verfolgung von Spielen, Phasen, Spielern und deren Interaktionen. 
Sie unterstützt alle wichtigen Vorgänge im Werwolf-Spiel, einschließlich der Speicherung von Eingaben und Antworten, Eliminierungen und Spielmetadaten.
Diese Struktur würde auch eine große Hilfe für uns sein, um Zwischenevaluationen durchzuführen. 
Leider konnten wir diese Datenbank nicht mit dem Backend des Spiels integrieren, aber es bleibt auf jeden Fall eine zukünftige To-Do.
