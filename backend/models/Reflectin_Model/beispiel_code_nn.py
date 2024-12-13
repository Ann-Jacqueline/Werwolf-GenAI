import openai
from transformers import pipeline

#TODO: Spielerin weiß nur ihre eigene Rolle??

# Reflection Model mit NN-Integration
class ReflectionModel:
    def __init__(self, global_history, api_key):
        """
        Initialisiert das Reflection Model mit einer GPT-API und einem vortrainierten Modell für Klassifikationen.

        Args:
            global_history (dict): Die Historie des Spiels.
            api_key (str): API-Schlüssel für OpenAI.
        """
        self.global_history = global_history
        openai.api_key = api_key
        # Vortrainiertes Modell für Textklassifikation
        self.classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

    def generate_reflection_prompt(self):
        """
        Erzeugt einen Prompt basierend auf der Spielhistorie.

        Returns:
            str: Der generierte Prompt.
        """
        prompt = "Basierend auf dem bisherigen Spielverlauf und den Spielerrollen: \n"

        # Rollen hinzufügen
        roles = self.global_history.get("roles", {})
        for player, role in roles.items():
            prompt += f"- Spieler {player} hat die Rolle: {role}\n"

        # Ereignisse nach Priorität sortieren und einfügen
        events = self.global_history.get("events", [])
        prioritized_events = sorted(events, key=lambda e: e.get("priority", 0), reverse=True)
        for event in prioritized_events:
            prompt += f"- {event['description']} (Priorität: {event['priority']})\n"

        prompt += "Was wäre die beste Strategie für die nächste Phase?"
        return prompt

    def get_gpt_response(self, prompt):
        """
        Ruft die GPT-4 API auf, um eine Antwort zu erhalten.

        Args:
            prompt (str): Der Eingabeprompt.

        Returns:
            str: Die Antwort von GPT-4.
        """
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content']

    def classify_gpt_output(self, gpt_output):
        """
        Klassifiziert die GPT-Ausgabe mithilfe eines vortrainierten NLP-Modells.

        Args:
            gpt_output (str): Die GPT-Ausgabe.

        Returns:
            dict: Klassifikationsergebnisse.
        """
        labels = ["offensive", "defensive", "neutral"]  # Mögliche Strategien
        classification = self.classifier(gpt_output, candidate_labels=labels)
        return classification


# Token Scoring Model mit NN-Integration
class TokenScoringModel:
    def __init__(self):
        """
        Initialisiert das Token Scoring Model.
        """
        # Zusätzliche Modelle oder externe API-Calls könnten hier integriert werden
        pass

    def score_tokens(self, gpt_output, classifications):
        """
        Bewertet Tokens basierend auf der Klassifikation und Relevanz.

        Args:
            gpt_output (str): Der GPT-Text.
            classifications (dict): Klassifikationsdaten aus dem Reflection Model.

        Returns:
            list: Bewertete Tokens.
        """
        tokens = gpt_output.split(". ")  # Text in Sätze aufteilen
        scored_tokens = []

        for token in tokens:
            score = 0

            # Bewertung basierend auf Klassifikation
            if "offensive" in classifications['labels']:
                score += classifications['scores'][classifications['labels'].index("offensive")] * 10
            if "defensive" in classifications['labels']:
                score += classifications['scores'][classifications['labels'].index("defensive")] * 5

            scored_tokens.append({"token": token, "score": score})

        return scored_tokens
    #TODO: Versteht der Agent die Punkte oder ist das nur für uns?


# Beispielhafter Workflow mit NN-Integration
if __name__ == "__main__":
    # Beispielhafte Global History Daten
    global_history_data = {
        "roles": {
            "A": "Dorfbewohner",
            "B": "Werwolf",
            "C": "Seher"
        },
        "events": [
            {"description": "Spieler A hat Spieler B beschuldigt.", "priority": 2},
            {"description": "Spieler C hat einen Vorschlag gemacht.", "priority": 1},
            {"description": "Spieler D wurde eliminiert.", "priority": 3}
        ]
    }

    # Reflection Model mit NN
    api_key = "your_openai_api_key_here"  # OpenAI API-Key einfügen
    reflection_model = ReflectionModel(global_history_data, api_key)
    prompt = reflection_model.generate_reflection_prompt()
    print("Generated Prompt:", prompt)  # Generierter Prompt

    gpt_output = reflection_model.get_gpt_response(prompt)  # GPT-4 API-Antwort abrufen
    print("GPT Output:", gpt_output)

    classifications = reflection_model.classify_gpt_output(gpt_output)  # Ausgabe klassifizieren
    print("Classifications:", classifications)

    # Token Scoring Model mit NN
    token_scoring_model = TokenScoringModel()
    scored_tokens = token_scoring_model.score_tokens(gpt_output, classifications)
    print("Scored Tokens:", scored_tokens)  # Bewertete Tokens
