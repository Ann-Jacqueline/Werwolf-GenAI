from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch

# Check if CUDA is available
print("CUDA Available:", torch.cuda.is_available())

# Load model through Hugging Face API with constraints
pipe = pipeline(
    "text-generation",
    model="meta-llama/Llama-3.3-70B-Instruct",
    device_map="auto",  # Automatically use GPU if available
    torch_dtype=torch.float16,  # Use half-precision for reduced memory
    use_auth_token=True
)

# Limit CPU threads if needed
torch.set_num_threads(4)

# Send a test request
response = pipe("Who are you?", max_length=50, num_return_sequences=1)

# Print the response
print("API Call Test Output:", response)
