# Reflection Model
class ReflectionModel:
    def __init__(self, global_history):
        """
        Initialisiert das Reflection Model mit den notwendigen Daten aus dem Global History Model.

        Args:
            global_history (dict): Das Spielprotokoll, das als Grundlage für die Reflexion dient.
        """
        self.global_history = global_history  # Speicherung der Spielhistorie zur späteren Verwendung

    def generate_reflection_prompt(self):
        """
        Erzeugt einen Prompt basierend auf der bisherigen Spielhistorie, Spielerrollen und priorisierten Ereignissen.

        Returns:
            str: Der generierte Prompt für GPT.
        """
        prompt = "Basierend auf dem bisherigen Spielverlauf und den Spielerrollen: \n"  # Einstieg in den Prompt

        # Spielerrollen einfügen
        roles = self.global_history.get("roles", {})  # Spielerrollen aus der Historie abrufen
        for player, role in roles.items():
            prompt += f"- Spieler {player} hat die Rolle: {role}\n"  # Jede Rolle zur Prompt-Ausgabe hinzufügen

        # Ereignisse priorisieren und einfügen
        events = self.global_history.get("events", [])  # Ereignisliste aus der Historie abrufen
        prioritized_events = sorted(events, key=lambda e: e.get("priority", 0),
                                    reverse=True)  # Nach Priorität sortieren
        for event in prioritized_events:
            prompt += f"- {event['description']} (Priorität: {event['priority']})\n"  # Ereignisse zur Prompt-Ausgabe

        prompt += "Was wäre die beste Strategie für die nächste Phase?"  # Abschlussfrage für die Strategie
        return prompt

    def process_gpt_output(self, gpt_output):
        """
        Verarbeitet die Ausgabe von GPT, klassifiziert Erkenntnisse und identifiziert Konflikte.

        Args:
            gpt_output (str): Der generierte Text von GPT.

        Returns:
            dict: Eine strukturierte Version des Outputs.
        """
        insights = gpt_output.split(". ")  # GPT-Antwort in einzelne Sätze aufteilen
        classifications = {"defensive": [], "offensive": []}  # Kategorien für Klassifizierung vorbereiten
        conflicts = []  # Liste für erkannte Konflikte

        for insight in insights:  # Durch alle Erkenntnisse iterieren
            if "verteidigen" in insight or "abwarten" in insight:
                classifications["defensive"].append(insight)  # Defensiv klassifizieren
            elif "angreifen" in insight or "kooperieren" in insight:
                classifications["offensive"].append(insight)  # Offensiv klassifizieren

        if "angreifen" in gpt_output and "abwarten" in gpt_output:
            conflicts.append("Konflikt zwischen Angriff und Verteidigung erkannt.")  # Konflikt identifizieren

        return {
            "reflection": gpt_output,  # Original GPT-Ausgabe
            "actionable_insights": insights,  # Aufgeteilte Sätze
            "classifications": classifications,  # Defensiv/Offensiv-Klassifikation
            "conflicts": conflicts  # Identifizierte Konflikte
        }


# Token Scoring Model
class TokenScoringModel:
    def __init__(self):
        """
        Initialisiert das Token Scoring Model.
        """
        pass  # Keine speziellen Initialisierungen notwendig

    def score_tokens(self, gpt_output):
        """
        Bewertet die Tokens basierend auf ihrer Relevanz, Wahrscheinlichkeit des Erfolgs und Konflikten.

        Args:
            gpt_output (dict): Der von GPT generierte und vom Reflection Model verarbeitete Output.

        Returns:
            list: Eine Liste von bewerteten Tokens.
        """
        tokens = gpt_output["actionable_insights"]  # Holen der zu bewertenden Tokens
        scored_tokens = []  # Ergebnisliste vorbereiten

        for token in tokens:  # Durch jedes Token iterieren
            score = 0  # Basiswert des Scores
            if "defensive" in gpt_output["classifications"] and token in gpt_output["classifications"]["defensive"]:
                score += 10  # Defensivstrategien erhalten +10 Punkte
            if "offensive" in gpt_output["classifications"] and token in gpt_output["classifications"]["offensive"]:
                score += 15  # Offensivstrategien erhalten +15 Punkte

            # Konflikte reduzieren den Score
            if token in gpt_output["conflicts"]:
                score -= 5  # Konflikte ziehen 5 Punkte ab

            scored_tokens.append({"token": token, "score": score})  # Token mit Score speichern

        return scored_tokens

    def send_to_next_model(self, scored_tokens):
        """
        Sendet die bewerteten Tokens an das FindMyTeammate Model oder Voting Model mit getrennten Empfehlungen.

        Args:
            scored_tokens (list): Eine Liste von bewerteten Tokens.

        Returns:
            dict: Daten für das nächste Model.
        """
        voting_recommendations = []  # Empfehlungen für das Voting Model
        teammate_recommendations = []  # Empfehlungen für das FindMyTeammate Model

        for token_data in scored_tokens:  # Durch jedes bewertete Token iterieren
            if token_data["score"] > 10:
                voting_recommendations.append(token_data)  # Hohe Scores gehen an Voting Model
            else:
                teammate_recommendations.append(token_data)  # Niedrigere Scores an FindMyTeammate Model

        return {
            "voting_recommendations": voting_recommendations,  # Strukturierte Empfehlungen für Voting Model
            "teammate_recommendations": teammate_recommendations  # Strukturierte Empfehlungen für Teammate Model
        }


# Beispielhafter Workflow
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

    # Reflection Model
    reflection_model = ReflectionModel(global_history_data)
    prompt = reflection_model.generate_reflection_prompt()
    print("Generated Prompt:", prompt)  # Ausgabe des generierten Prompts

    # GPT Integration (Simuliert)
    gpt_output = "Strategie 1: Zusammenarbeit mit Spieler C. Strategie 2: Spieler A meiden. Strategie 3: Abwarten."

    # Verarbeitung der GPT-Ausgabe
    processed_output = reflection_model.process_gpt_output(gpt_output)
    print("Processed Output:", processed_output)  # Ausgabe der verarbeiteten Daten

    # Token Scoring Model
    token_scoring_model = TokenScoringModel()
    scored_tokens = token_scoring_model.score_tokens(processed_output)
    print("Scored Tokens:", scored_tokens)  # Ausgabe der bewerteten Tokens

    # Weitergabe der Daten
    next_model_data = token_scoring_model.send_to_next_model(scored_tokens)
    print("Data for Next Model:", next_model_data)  # Ausgabe der Daten für das nächste Modell
