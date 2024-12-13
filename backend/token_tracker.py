from transformers import AutoTokenizer

class TokenTracker:
    def __init__(self, model_name, token_limit = 30000):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.token_limit = token_limit
        self.token_usage = 0

    def count_tokens(self, prompt, response):
        """Zählt die Anzahl der Tokens für Eingabe und Ausgabe"""
        input_tokens = len(self.tokenizer.tokenize(prompt))
        output_tokens = len(self.tokenizer.tokenize(response))
        total_tokens = input_tokens + output_tokens
        self.token_usage += total_tokens
        return total_tokens, input_tokens, output_tokens

    def is_limit_reached(self):
        """Überprüft, ob das Token Limit erreicht ist"""
        return self.token_usage >= self.token_limit

    def get_usage(self):
        """Gibt aktuellen Tokenverbrauch an"""
        return self.token_usage

if __name__=="__main__":
        tracker = TokenTracker("meta-llama/Llama-2-13b-chat-hf")

        prompt = "Beispielprompt"
        response = "Das ist eine Beispielantwort"

        input_tokens, output_tokens, total_tokens = tracker.count_tokens(prompt, response)
        print(f"Prompt: {prompt}")
        print(f"Response: {response}")
        print(f"Eingabetokens: {input_tokens}, Ausgabetokens: {output_tokens}, Gesamtokens {total_tokens}")
        print(f"Tokenverbrauch gesamt: {tracker.get_usage()} / {tracker.token_limit}")

