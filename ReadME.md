
# **WerewolfIQ: Das Werwolf-Spiel mit Köpfchen - GenAI App**

<img src="WerwolfIQ_Logo.png" alt="Image" style="width:80%; height:auto;">

## Dieses Projekt wurde im Rahmen des Unternehmensoftware-Kurses unter der Leitung von Prof. Dr. Axel Hochstein entwickelt.


### WerewolfIQ ist eine KI-gestützte Umsetzung des klassischen Werwolf-Spiels, basierend auf einer modularen Architektur, die Skalierbarkeit, Flexibilität und Konsistenz ermöglicht.  

---

## **Autoren**
- **Ann-Jacqueline Kaldjob (AJ)**  
- **Laura Porbadnik**  
- **Seli Tusha**  

---

## **1. Übersicht der Experimente**
#### Während der Entwicklung von WerwolfIQ haben mehrere Experimente zu Verbesserung unsere App durchgeführt: 

### **Experiment 1: Werwolf-Spiel mit ChatGPT**
- **Ziel: Testen, ob ChatGPT den Spielfluss und Multi-Agenten-Interaktionen koordinieren kann.** 
- **Ergebnisse:**
  - ChatGPT konnte Rollen spielen, hatte jedoch erhebliche Probleme mit Logik und Kontinuität.
  
- **Hauptprobleme:**
  - **Player Choice Bias (PCB):** ChatGPT priorisierte Entscheidungen des menschlichen Spielers, auch wenn sie unlogisch waren.
  - **Narrative Role Switch (NRS):** Rollen wurden spontan verändert, um Entscheidungen des Spielers zu unterstützen.
  - **Logikfehler:** Fehler in den Sonderrollen (z. B. Amor), Diskussionsrunden nach Spielende und unplausible Anschuldigungen unter Spielern, inklusive Werwölfen.
- **Fazit:** ChatGPT ist nicht in der Lage, den komplexen Spielfluss von Werwolf eigenständig und konsistent zu koordinieren.
Fehler bei Sonderrollen und falsche Fortsetzung des Spiels nach Spielende. 

###### Mehr Infos Hier: [ChatGPT_Lab_Experiment_1.md](Experiments_Evaluation/Experiment_1_Anfang/ChatGPT_Lab_Experiment_1.md)

---

### **Experiment 2: Simulation des Spiels in einem zentralen Script**
- **Ziel: Aufbau einer ersten Simulation-Architektur von werwolfIQ**
- **Herausforderungen:**
  - Unklare Übergänge zwischen Tag- und Nachtphasen.
  - Statische Antworten von GPT, die Diskussionen unnötig verlängerten.
- **Fazit:** Eine umfassendere Architektur war notwendig, um Konsistenz und Flexibilität zu gewährleisten.

###### Mehr Infos Hier: [Evaluation2 - Zwischenstand.md](Experiments_Evaluation/Experiment_2_LSA_MHNN/Evaluation2%20-%20Zwischenstand.md)

---

### **Experiment 3: Modulare Architektur - LSA MMA (Multi Modular Architecture) (Aktueller Stand)**
- **Ziel:** Implementierung einer skalierbaren, modularen Architektur mit Unterstützung für **Latent State Alignment (LSA)**.
- **Ergebnisse:**
  - Die Struktur ermöglicht die Verfolgung von Spielen, Phasen, Spielern und Interaktionen.
  - Unterstützt wichtige Funktionen wie Speicherung von Eingaben, Eliminierungen und Spielmetadaten.
  - **Herausforderung:** Integration der Datenbank und dem Frontend mit dem Backend wurde noch nicht abgeschlossen.
- **Fazit:** Die Architektur ist robust und bietet eine Grundlage für zukünftige Erweiterungen, einschließlich der Integration eines Frontends und einer optimierten Datenbanklösung.

---

### **Experiment 4 (Zukünftig): Frontend und ChromaDB**
- **Ziel:**
   - Integration eines FrontendInteraction-Moduls zur Echtzeit-Kommunikation zwischen Frontend und Backend.
   - Erneute Implementierung und Optimierung von ChromaDB für persistente und latente Zustandsverfolgung.
- **Erwartete Vorteile:**
   - FrontendInteraction-Modul: Reibungsloser Spielfluss durch Echtzeit-Updates und benutzerfreundliche Schnittstelle.
   - ChromaDB: Verbesserte Speicherung von Spielhistorien und Zustandsanalysen durch latente Speicherabfragen.

###### Mehr Infos Hier:

###### Chroma: [Experiment_ChromaDB_ReadMe.md](Experiments_Evaluation/Experiment_4_weitere%20Ideen/Chroma_DB/Experiment_ChromaDB_ReadMe.md)
###### FrontendInteraction: [FrontendInterAction_README.md](Experiments_Evaluation/Experiment_4_weitere%20Ideen/FrontendInterAction_README.md)
## **2. Modulübersicht**

### **2.1 Orchestrator**
- **Funktion**:  
  - Zentraler Controller, der den gesamten Spielfluss koordiniert.  
  - Verwaltet die Abfolge der Phasen und delegiert Aufgaben an andere Module.  
- **Details**:  
  - Initialisiert den Spielstatus (über GameState).  
  - Ruft die Module für Reflexion, Abstimmung und Konsensprüfung auf.  
  - Kommuniziert mit dem Moderator-Modul, um Spieler zu informieren.  

---

### **2.2 GameState-Modul**
- **Funktion**:  
  - Speicherung und Verwaltung aller relevanten Spieldaten.  
  - Stellt Methoden zur Manipulation des Status bereit.  
- **Details**:  
  - **Datenelemente**:  
    - Rollen der Spieler.  
    - Gesprächsprotokolle.  
    - Eliminierte Spieler.  
  - **Beispielmethoden**:  
    - `initialize_roles(player_ids)`: Verteilt Rollen basierend auf Spielregeln.  
    - `add_to_conversation_log(player_id, statement)`: Speichert Aussagen der Spieler.  
    - `get_valid_targets(current_player)`: Gibt basierend auf Spielstatus und Rolle mögliche Ziele zurück.  

---

### **2.3 Reflection-Modul**
- **Funktion**:  
  - Führt latente Zustandsanalysen (LSA) durch, um unsichtbare Spielinformationen wie Vertrauen und Allianzen abzuleiten.  
  - Liefert kontextuelle Handlungsempfehlungen.  
- **Details**:  
  - Analysiert Gesprächsverläufe und Spielhistorie.  
  - **Beispielmethoden**:  
    - `reflect(player, round_number)`: Generiert rollenspezifische Empfehlungen.  
    - `analyze_latent_states(game_state)`: Ermittelt Werte wie Vertrauen und Misstrauen.  
  - **Ergebnis**:  
    - Liefert GPT-Agenten relevante Informationen für strategische Entscheidungen.  


### **2.3.1  Latent State Alignment (LSA)**

### **Definition**
LSA ermöglicht die Ableitung unsichtbarer Zustände wie Vertrauen, Misstrauen und Allianzen 
aus Gesprächsprotokollen und Spielverläufen.

### Integration in die Module
Reflection-Modul:
Analyse latenter Zustände zur Unterstützung strategischer Entscheidungen.
Beispiel: Ermittlung von Verdachtswerten basierend auf Aussagen und Verhaltensmustern.

###### Mehr Infos Hier:[Latent_State_Alignment_fuer_RM_Modul.md](backend/models/LSA_MMA_Module/Latent_State_Alignment_fuer_RM_Modul.md)

---

### **2.4 PromptBuilder-Modul**
- **Funktion**:  
  - Erstellung von GPT-Prompts basierend auf Phase, Rolle und Spielsituation.  
- **Details**:  
  - Generiert Prompts für verschiedene Szenarien (Tag-/Nachtphasen).  
  - **Beispielmethoden**:  
    - `build_night_prompt(player, game_state)`: Erstellt Prompts für Werwölfe während der Nachtphase.  
    - `build_day_prompt(player, game_state)`: Generiert Diskussionsthemen für Tagphasen.  
  - Integriert Warnungen wie "Keine Vorkenntnisse verfügbar in der ersten Nacht".  

---

### **2.5 GPTInteraction-Modul**
- **Funktion**:  
  - Schnittstelle zu GPT zur Abfrage von Empfehlungen und Entscheidungen.  
- **Details**:  
  - Verarbeitet Prompts und validiert Antworten.  
  - **Beispielmethoden**:  
    - `get_suggestion(prompt, valid_targets)`: Filtert gültige Entscheidungen aus GPT-Antworten.  
  - Integriert Fehlerbehandlung und Logging zur Überprüfung der Interaktionen.  

---

### **2.6 Moderator-Modul**
- **Funktion**:  
  - Steuerung der Übergänge zwischen Phasen und Kommunikation mit Spielern.  
- **Details**:  
  - **Beispielmethoden**:  
    - `handle_phase_transition(phase, round_number)`: Verwaltet Phasenübergänge.  
    - `announce_elimination(player, role)`: Informiert Spieler über Eliminierungen.  

---

### **2.7 Voting-Modul**
- **Funktion**:  
  - Verwaltung der Abstimmungs- und Diskussionsphasen.  
- **Details**:  
  - Organisiert Diskussionen und Konsensfindung.  
  - **Beispielmethoden**:  
    - `resolve_votes(votes)`: Aggregiert Stimmen und eliminiert Spieler.  
    - `night_phase(round_number)`: Führt Diskussionen und Entscheidungen der Werwölfe durch.  

---

### **2.8 ConsensusChecker-Modul**
- **Funktion**:  
  - Überprüfung der Gesprächsprotokolle auf Konsensentscheidungen.  
- **Details**:  
  - Identifiziert Übereinstimmungen oder Konflikte in Aussagen.  
  - **Beispielmethoden**:  
    - `check_consensus(game_state, current_player)`: Analysiert Gesprächsverläufe auf Konsens.  

---

### **2.9 GlobalHistory-Modul**
- **Funktion**:  
  - Archiviert den Spielverlauf und erstellt Zusammenfassungen.  
- **Details**:  
  - **Beispielmethoden**:  
    - `archive_game_state(game_state)`: Speichert den aktuellen Status.  
    - `record_event(event_type, details)`: Protokolliert Ereignisse für spätere Auswertung.  

---

## **3. Vorteile der modularen Architektur**
- **Flexibilität**: Leicht anpassbar an neue Rollen und Strategien.  
- **Skalierbarkeit**: Unterstützt Erweiterungen wie Frontend-Integration.  
- **Transparenz**: Fehler und Inkonsistenzen können schnell identifiziert werden.
- **Separation of Concern (SoC)**: Jedes Modul trägt klare, in sich abgekapselte Funktionen und Aufgaben. 
Somit können die Entwicklungszyklen, durch paralleles Arbeiten beschleunigt werden. 

---

## **4. Zusammenfassung**
Die detaillierte, modulare Architektur von WerewolfIQ ermöglicht es, den Spielfluss präzise und konsistent zu gestalten. 
Durch die Integration von LSA, robusten Datenmodulen, im MMicroservice Style, und einer klar definierten Kommunikation zwischen Komponenten wird das Projekt zu einer skalierbaren Grundlage für zukünftige Erweiterungen, wie die Einbindung eines Frontends und einer optimierten Datenbanklösung.  