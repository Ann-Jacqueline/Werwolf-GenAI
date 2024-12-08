### To-Do-Liste: Laura (23.11.2024)

<ul>
  <li><input type="checkbox"> Rollen Beschreibung pro Agents, um Stance und Strategie Foundation zu bauen</li>
</ul>

### To-Do-Liste:  AJ (23.11.2024)

<ul>
  <li><input type="checkbox"> Custom neuronales Netz gucken, wie die WIU-Funktion implementiert werden kann</li>
  <li><input type="checkbox"> Tokenization</li>
  <li><input type="checkbox"> Struktur von Datenfluss (falls wir GPT-4o benutzen) </li>
  <li><input type="checkbox" checked style="accent-color: blue;"> Abstract und Conclusion des Experiments</li>

</ul>

### To-Do-Liste: Seli (23.11.2024)

<ul>
  <li><input type="checkbox"> Sonderrollen-Beschreibung, die komplex (templates) sind</li>
  <li><input type="checkbox"> Paper highlight</li>
</ul>



## 03.12.2024
LSA MHNN -> Laura-Seli-AJ Multi-Head Neuronales Netz
Angepasste initial game_states für jeder rolle : special variablen
prompt templates for the dynamische Prompt vom LSA MHNN
moderator agent -> makes summaries  to feed to player agents that are awake -> before they fall asleep
last_statement : key-Value paar -> rolle-prompt
history deactivation when they are asleep? 
lovers become allys because if their lover dies they die 
jäger erstmal raus um Funktionsredundanzen zu vermeiden
dynamic prompt: ich- perspektive, summary of game state --> 
weitergeleitet to llama-3 --> line 1 of the diskussion generiert --> 
historie for every player updated --> 
next player who wants to discuss goes throught the same schritte again (reflektionslayer, dynamic prompt, llama-3, argumentgenerierung)

### 03.12.2024 - AJ Notes
- Refectionlayer -> Refelction model = Transormer Model prompt templates für die dynamic LSA MHNN "contextual bounding component
- LlaMA pretrained Model use nur für Textgenerierung
- Abstimmungslayer - 
- Token-Scoring Layer -> Token-Scoring Model =  ein Neuronales netz that scores the LlaMa output based on predefined criteria (coherence,alignment, strategy)
- Global History Layer -> Global History Model = Tracks historcal cntext and strategic patterns using LSTM
- Controller (Orchestrator) manages the flow of data between components, Updates game state and ensures itirative processing

#### Iterative Nature
The MHNN operates in a loop (reflection → llama → scoring → reflection → history) rather than a strictly feed-forward fashion.
----------------------------------------------------------------------------------


### Ideensammelung 
Custom Head neuronales netzt!!!

Minimal 8 Spieler

(Dynamische) Anzahl an Agents

Immer 8 Spieler inkl. 1 mensch

Moderator auch agent braucht auch description

Maximal 4 Werwölfe

**Immer 2 Werwölfe**

Sonderollen:

Amor

Hexe/Jäger

Seherin

Sonderollen werden nach benutzten ihrer Fähigkeit Dorfbehwohner

Hardcoding der Spielregeln und der Reihenfolge wenn welche Sonderolle in der Nacht aufwacht

Hardcoding der Rollen

Modell verweist zufällig die Rollen auf alle Agent

Für jede Rolle eine Base description wo die grundlegenden Rolleninformationen und Grundstrategien in natürlicher Sprache stehen. Daraus wird die fortlaufende Strategie gebaut





