# Workflow im Kontext des LSA-MHA-Systems

### Global Orchestrator (Startpunkt):
Aufgabe: Der Orchestrator aktiviert und deaktiviert und koordiniert Modelle. Prompted Modelle Daten weiterzugeben. Es enthält nur allgeimeine Spielinfos -> welches Modell ist an -> Controller

Connection mit FE -> weil dadurch alles aktiviert wird

Global History Model gibt Orchestrator Signal, dass es sich im finalen Status befindet und dann Nacht- oder Tagphase gestartet wird getriggert durch Voting Modell.

Dafür macht AJ 100 Epochen Durchlauf für Modelle für DS-Generierung


### Reflection Model:
Gewichtungen?: Eliminierungsinfos -> hoch gewichtet, Aktualität der Info schwerer gewichtet, als ältere Info
Aufgabe: Dieses Modell analysiert die globalen Daten und generiert einen Prompt, um GPT-4o zu befragen -> Input = GameState mit allen Infos -> es soll dynamisch ein Prompt generiert werden, jeder Agent soll einmal reflektieren -> es soll ein Satz Output generiert werden -> Vermeidung von Diskussion
Beispiel: Basierend auf den Rollen (z. B. Werwolf, Seher) und priorisierten Ereignissen wird eine Strategiefrage gestellt: „Du bist Werwolf, wen schlägst du vor zu eliminieren in der Nacht?“ -> Output von GPT "Ich schlage Spielerin C vor." -> OBACHT auf Spielrunden (in 1.Spielrunde gibt es keine Information)
hier GPT, der sagt, ich bin Werwolf oder Dorfbewohner, wir arbeiten noch nicht mit echtem Output
Weitergabe: Die verarbeiteten Daten (Output) werden an das Token Scoring Model geschickt.
Nebeninfo: Du hast ein Veto in der Abstimmung, wenn du der Diskussion zuerst beitrittst

### Token Scoring Model:
GPT soll uns einen Satz geben, der Diskussion einleitet -> zB.: "ich will Spielerin A elminieren"
Verarbeitung: Die GPT-Antwort wird klassifiziert (offensiv vs. defensiv) und Konflikte (z. B. widersprüchliche Strategien) werden erkannt.
Aufgabe: Bewertet die Vorschläge von GPT basierend auf Relevanz, Erfolgsaussicht und Konfliktfreiheit (temporäre Konflikte) -> keine Referenzierung auf Kontexte, die nicht existieren -> wenn wir Inkonsistenz bemerken, hier sind logische Inkonsistenzen -> bleib konsistent
Beispiel: „Zusammenarbeit mit Spieler C“ könnte einen hohen Score bekommen, während „Angreifen und Verteidigen gleichzeitig“ einen reduzierten Score hat. -> strategische Spielzüge belohnen
Weitergabe: Die Ergebnisse werden in zwei Kategorien aufgeteilt:

Voting Model: Für Entscheidungen (z. B. wer eliminiert wird).
FindMyTeammate Model: Für die Suche nach Verbündeten.

### FindMyTeammate Model:
Aufgabe: Identifiziert potenzielle Teammitglieder basierend auf den Scoring-Daten.
Beispiel: Spieler C wird als wahrscheinlicher Verbündeter hervorgehoben.
Weitergabe: Unterstützt das Voting Model mit Zusatzinformationen.

### Voting Model:
Aufgabe: Trifft die finale Entscheidung basierend auf den Diskussionen (passieren im Voting Model selbst) und Scoring-Ergebnissen (??bekommt das Voting Model die Infos aus dem Token Scoring Model??). -> hier kommen alle Aussagen zusammen 
Beispiel: Spieler A wird aufgrund der Aussagen der anderen Agents und Abstimmungen eliminiert. 
Weitergabe: Der Entscheidungsoutput wird an das Global History Model zurückgemeldet.
+++Fail-Safe, dass Spiel nicht unendlich läuft -> schnelle Aktivierung der Agents+++ -> höhere Chance auf höheren Score, wenn man zuerst in Diskussion eintritt ODER dass Moderatorin eingeschaltet wird, um es zu steuern, wenn es zu lange geht ODER Timer pro Diskusison
Generiert noch Zusammenfassung -> weiter an Global History (wer eliminiert wurde und welche Rolle + Zusammenfassung der Diskussion)

### Global History Model (Memory):
Aufgabe: Speichert die Entscheidungen und den aktuellen Status des Spiels (z. B. wer eliminiert wurde).
Weitergabe: Sendet den aktualisierten Zustand zurück an den Orchestrator, um die nächste Phase einzuleiten.

### Zyklus-Wiederholung:
Der Orchestrator startet die nächste Spielphase basierend auf dem aktualisierten Spielstatus.

### Beispiel für den Workflow (vereinfacht):
Orchestrator: „Spieler B hat Spieler A beschuldigt; Spieler D wurde eliminiert.“
Reflection Model: „Wie sollte Spieler C handeln?“ → GPT-Antwort: „Spieler C sollte Spieler B unterstützen.“
Token Scoring Model: „Unterstützung von Spieler B“ erhält 15 Punkte.
FindMyTeammate Model: Identifiziert Spieler B als potenziellen Verbündeten.
Voting Model: Spieler A wird mit den meisten Stimmen eliminiert.
Global History Model: Aktualisiert den Status: „Spieler A eliminiert.“
Der Workflow bleibt dynamisch und wiederholt sich, bis das Spiel endet. Soll ich noch einen spezifischen Teil vertiefen?


# Konzept für API-Integration in jedem Modell

### Reflection Model:
Aufgabe der API: Der API-Call könnte genutzt werden, um GPT-4 dynamisch zu fragen, basierend auf dem Spielverlauf, welche Strategien sinnvoll sind.
API-Integration: Nutze einen openai.ChatCompletion-Call, um basierend auf dem generierten Prompt direkt GPT-Output zu erhalten.
### Token Scoring Model:
Aufgabe der API: Eine API-Instanz könnte externe Analysen verwenden (z. B. semantische Analyse oder eine externe Scoring-API), um Tokens genauer zu bewerten.
API-Integration: Beispielsweise könnte eine Gewichtung oder Priorisierung von GPTs Vorschlägen durch NLP-Tools oder spezialisierte ML-Modelle unterstützt werden.
Voting Model:
Aufgabe der API: Eine API könnte Wahrscheinlichkeiten berechnen (z. B. wer Werwolf ist) oder direkt Entscheidungsprozesse simulieren.
API-Integration: Das Modell könnte einen Service nutzen, der Vorschläge oder Abstimmungen optimiert.
### FindMyTeammate Model:
Aufgabe der API: Die API könnte genutzt werden, um Datenbankabfragen durchzuführen oder externe Modelle zu verwenden, um Verbündete zu identifizieren.
API-Integration: Dies könnte ein einfacher Call sein, der Teamplayer mit hoher Wahrscheinlichkeit auflistet.
Vorteile
Flexibilität: Jedes Modell arbeitet unabhängig und kann bei Bedarf mit spezialisierten Datenquellen oder Modellen interagieren.
Modularität: Jedes Modell bleibt klar abgegrenzt und kann unabhängig skaliert werden.
Erweiterbarkeit: Man könnte externe APIs austauschen oder erweitern, ohne das gesamte System anzupassen.

## Beispielcode

    import openai

    class ReflectionModel:
    def __init__(self, global_history, api_key):
        self.global_history = global_history
        openai.api_key = api_key

    def generate_reflection_prompt(self):
        prompt = "Basierend auf dem bisherigen Spielverlauf: \n"
        for event in self.global_history.get("events", []):
            prompt += f"- {event['description']} (Priorität: {event['priority']})\n"
        prompt += "Welche Strategie ist die beste für die nächste Phase?"
        return prompt

    def get_gpt_response(self, prompt):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content']

# "Einbau" von NNs

Was bedeutet das für euch?

### Keine manuelle Layer-Definition nötig:
Die neuronalen Netzwerke sind bereits trainiert und betriebsbereit. Wir greifen nur auf die APIs zu und geben den jeweiligen Eingabeprompt (z. B. Spielverlauf, Rollen) oder Daten (z. B. Text für Klassifikationen) weiter.
### Dynamische Verarbeitung durch APIs:
Der GPT-4 API Call übernimmt die komplexe Aufgabe, basierend auf unserem Prompt Vorschläge zu generieren.
Das BART-basierte Klassifikationsmodell klassifiziert den GPT-Output automatisch, ohne dass wir explizite Regeln (wie manuelle Schlüsselwörter) definieren müssen.
### Unsere Aufgabe – Struktur vorgeben:
Wir definieren die Logik und Reihenfolge der Modelle im Workflow (z. B. welche Daten von GPT an das Token Scoring weitergeleitet werden).
Die Struktur (wie der Prompt oder die Klassifikationslabels) bestimmt, wie die APIs agieren.
### Vorteil dieser Architektur:
Effizienz: Ihr könnt euch auf die Workflow-Logik konzentrieren, ohne ein neuronales Netz von Grund auf trainieren zu müssen.
Skalierbarkeit: Änderungen am Modell können einfach durch Modifikation der Eingabedaten oder Prompts vorgenommen werden.
Zukunftssicher: Neue Versionen der APIs (z. B. GPT-5) lassen sich nahtlos einbinden.

