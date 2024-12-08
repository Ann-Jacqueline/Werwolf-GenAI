# Workflow of the LSA MHNN Models - English

## 1. Orchestrator
- **Trigger:** Initiates the dynamic prompt generation process at the start of each phase (day or night).
- **Interaction:**
  - Sends a trigger to the Reflection Model at the start of a new phase.
  - Receives the final game state from the Persistent Global History Model to determine if a new phase should begin or if the game should end.

## 2. Reflection Model
- **Purpose:** Scrapes relevant game state information and generates a dynamic prompt for LLAMA based on:
  - Persistent global history (at the start of a new phase).
  - Tentative global history (during ongoing discussions).
- **Trigger:**
  - At the start of a new phase, triggered by the Orchestrator.
  - During discussions, triggered by updates from the Tentative Global History Model.
- **Interaction:**
  - Scrapes the game state (persistent or tentative).
  - Generates a dynamic prompt and sends it to LLAMA.

## 3. LLAMA
- **Purpose:** Processes the dynamic prompt from the Reflection Model and generates a single line of natural language output based on strategy and context.
- **Interaction:**
  - Receives the dynamic prompt from the Reflection Model.
  - Sends raw output to the Token Scoring Model for optimization.
  - Outputs are added to the Tentative Global History Model alongside black box observations.

## 4. Token Scoring Model
- **Purpose:** Optimizes LLAMA's output for coherence, strategy, and alignment with game objectives. Ensures temporal coherence and rejects invalid outputs.
- **Interaction:**
  - Receives raw LLAMA output, evaluates, and optimizes it.
  - Sends optimized output to the Tentative Global History Model for inclusion.
  - Performs validation against the Persistent Global History Model for temporal consistency.

## 5. Tentative Global History Model - Short-Term-Memory
- **Purpose:** Acts as a cache during discussions, temporarily storing LLAMA's outputs and black box observations of other agents.
- **Trigger:** Continuously updated during the discussion phase.
- **Interaction:**
  - Stores outputs from the Token Scoring Model and observations from other agents.
  - Triggers the Reflection Model to reprompt LLAMA with updated information.
  - At the end of the discussion, sends the full discussion log to the Voting Model.
  - Gets cleared after the Voting Model has made a decision.

## 6. Voting Model
- **Purpose:** Finalizes the discussion by making a collective decision based on the discussion log.
- **Trigger:** Activated at the end of a discussion phase when the Tentative Global History Model sends the log.
- **Interaction:**
  - Receives the full discussion log from the Tentative Global History Model.
  - Summarizes the discussion and final decision.
  - Sends the summary and final decision to the Persistent Global History Model.

## 7. Persistent Global History Model - Long-Term-Memory
- **Purpose:** Stores the permanent game state, including summaries of discussions, decisions, and observations from previous rounds.
- **Interaction:**
  - Receives summaries and final decisions from the Voting Model.
  - Provides historical data to the Reflection Model at the start of a new phase.
  - Sends the final game state to the Orchestrator to trigger a new phase or end the game.

## Feedback Loops

### Discussion Phase
- **Flow:** Reflection Model → LLAMA → Token Scoring Model → Tentative Global History Model → Reflection Model.
- **Details:** This loop continues dynamically until the discussion ends.

### End of Discussion Phase
- **Flow:** Tentative Global History Model → Voting Model → Persistent Global History Model → Orchestrator.

### Start of a New Phase
- **Flow:** Persistent Global History Model → Orchestrator → Reflection Model.

## Key Improvements
- Added Tentative Global History Model as a cache to keep discussions lightweight and streamlined.
- Temporal coherence checks implemented in the Token Scoring Model and validated against the Persistent Global History.
- Adjusted roles for the Reflection Model to scrape only from the relevant history (persistent at phase start, tentative during discussions).
- Black box observations integrated dynamically into the Tentative Global History Model for real-time strategy updates.
------------------------------------------------------------------------------------------------------------------------


# Workflow der Modelle - Deutsch

## 1. Orchestrator
- **Auslöser:** Startet die Generierung des dynamischen Prompts zu Beginn jeder Phase (Tag oder Nacht).
- **Interaktion:**
  - Sendet einen Auslöser an das Reflektionsmodell zu Beginn einer neuen Phase.
  - Empfängt den finalen Spielstatus vom Persistenten Globalen Historienmodell, um festzustellen, ob eine neue Phase beginnen oder das Spiel enden soll.

## 2. Reflektionsmodell
- **Zweck:** Extrahiert relevante Spielstatusinformationen und erstellt ein dynamisches Prompt für LLAMA basierend auf:
  - Persistenter globaler Historie (zu Beginn einer neuen Phase).
  - Tentativer globaler Historie (während laufender Diskussionen).
- **Auslöser:**
  - Zu Beginn einer neuen Phase, ausgelöst durch den Orchestrator.
  - Während Diskussionen, ausgelöst durch Aktualisierungen des Tentativen Globalen Historienmodells.
- **Interaktion:**
  - Extrahiert den Spielstatus (persistent oder tentativ).
  - Generiert ein dynamisches Prompt und sendet es an LLAMA.

## 3. LLAMA
- **Zweck:** Verarbeitet das dynamische Prompt vom Reflektionsmodell und erzeugt eine einzelne Zeile natürlicher Sprachausgabe basierend auf Strategie und Kontext.
- **Interaktion:**
  - Empfängt das dynamische Prompt vom Reflektionsmodell.
  - Sendet Roh-Ausgabe an das Token-Scoring-Modell zur Optimierung.
  - Ausgaben werden zusammen mit Blackbox-Beobachtungen dem Tentativen Globalen Historienmodell hinzugefügt.

## 4. Token-Scoring-Modell
- **Zweck:** Optimiert die LLAMA-Ausgabe für Kohärenz, Strategie und Ausrichtung an den Spielzielen. Überprüft die zeitliche Kohärenz und verwirft ungültige Ausgaben.
- **Interaktion:**
  - Empfängt Roh-Ausgabe von LLAMA, bewertet und optimiert sie.
  - Sendet optimierte Ausgabe an das Tentative Globale Historienmodell.
  - Validiert gegen die Persistente Globale Historie für zeitliche Konsistenz.

## 5. Temporäres Globales Historienmodell - Kurzzeitgedächtnis
- **Zweck:** Dient als Cache während Diskussionen und speichert vorübergehend LLAMA-Ausgaben und Blackbox-Beobachtungen anderer Agenten.
- **Auslöser:** Wird kontinuierlich während der Diskussionsphase aktualisiert.
- **Interaktion:**
  - Speichert Ausgaben vom Token-Scoring-Modell und Beobachtungen anderer Agenten.
  - Löst das Reflektionsmodell zur Neugenerierung eines Prompts aus.
  - Sendet am Ende der Diskussion das vollständige Diskussionsprotokoll an das Abstimmungsmodell.
  - Wird nach der Entscheidung des Abstimmungsmodells gelöscht.

## 6. Abstimmungsmodell
- **Zweck:** Finalisiert die Diskussion, indem es auf Basis des Diskussionsprotokolls eine kollektive Entscheidung trifft.
- **Auslöser:** Wird am Ende der Diskussionsphase aktiviert, wenn das Tentative Globale Historienmodell das Protokoll sendet.
- **Interaktion:**
  - Empfängt das vollständige Diskussionsprotokoll vom Tentativen Globalen Historienmodell.
  - Fasst die Diskussion und die finale Entscheidung zusammen.
  - Sendet die Zusammenfassung und Entscheidung an das Persistente Globale Historienmodell.

## 7. Persistentes Globales Historienmodell - Langzeitgedächtnis
- **Zweck:** Speichert den permanenten Spielstatus, einschließlich Zusammenfassungen von Diskussionen, Entscheidungen und Beobachtungen aus vorherigen Runden.
- **Interaktion:**
  - Empfängt Zusammenfassungen und finale Entscheidungen vom Abstimmungsmodell.
  - Stellt historische Daten für das Reflektionsmodell zu Beginn einer neuen Phase bereit.
  - Sendet den finalen Spielstatus an den Orchestrator, um eine neue Phase zu starten oder das Spiel zu beenden.

## Feedback-Schleifen

### Diskussionsphase
- **Ablauf:** Reflektionsmodell → LLAMA → Token-Scoring-Modell → Temporäres Globales Historienmodell → Reflektionsmodell.
- **Details:** Dieser Zyklus läuft dynamisch, bis die Diskussion endet.

### Ende der Diskussionsphase
- **Ablauf:** Tentatives Globales Historienmodell → Abstimmungsmodell → Persistentes Globales Historienmodell → Orchestrator.

### Start einer neuen Phase
- **Ablauf:** Persistentes Globales Historienmodell → Orchestrator → Reflektionsmodell.

## Verbesserungen
- Einführung des Tentativen Globalen Historienmodells als Cache zur Vereinfachung und Verschlankung der Diskussionen.
- Zeitliche Kohärenzprüfungen im Token-Scoring-Modell implementiert und gegen die Persistente Globale Historie validiert.
- Reflektionsmodell so angepasst, dass es nur relevante Historien (persistent bei Phasenstart, tentativ während Diskussionen) abruft.
- Blackbox-Beobachtungen dynamisch in das Tentative Globale Historienmodell integriert, um Echtzeit-Strategieanpassungen zu ermöglichen.
