# You have to sign up and get an API key: https://platform.openai.com/signup
from openai import OpenAI
client = OpenAI(api_key="")


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