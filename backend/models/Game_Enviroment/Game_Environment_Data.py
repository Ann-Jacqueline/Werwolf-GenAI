# You have to sign up and get an API key: https://platform.openai.com/signup
from openai import OpenAI
import os

# Den API-Key aus der Umgebungsvariable laden
api_key = os.getenv("YOUR_API_KEY")
if not api_key:
    raise ValueError("Umgebungsvariable 'YOUR_API_KEY' ist nicht gesetzt!")

# OpenAI-Client initialisieren
client = OpenAI(api_key=api_key)

# Testaufruf (optional, z. B. um das Modell abzufragen)
print("OpenAI-Client erfolgreich initialisiert.")



# Pricing: https://openai.com/pricing
# Harry Potter "Chamber of Secrets" is about 100K tokens (GPT 3.5: ~ 5 cents)


# Set limits: https://platform.openai.com/account/billing/limits
# Check usage: https://platform.openai.com/account/usage


# OpenAI API documentation: https://platform.openai.com/docs/introduction/overview

response = client.chat.completions.create(
  model="gpt-4o",
  messages=[
    {"role": "system", "content": "Wer bist du?"}
  ]
)

print(response.choices[0].message.content)