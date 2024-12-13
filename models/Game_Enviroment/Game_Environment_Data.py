import openai

# Set your API key
openai.api_key = "YOUR_API_KEY_HERE"  # Replace with your actual API key

# Define the model name
model_name = "gpt-4o"

# Create a test request
response = openai.ChatCompletion.create(
    model=model_name,
    messages=[{"role": "user", "content": "Who are you?"}],
    max_tokens=50,
    temperature=0.7
)

# Print the response
print("API Call Test Output:", response.choices[0].message.content.strip())
