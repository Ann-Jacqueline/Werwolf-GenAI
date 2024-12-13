from transformers import AutoTokenizer, AutoModelForCausalLM
from backend.config.config import game_config

# Load LLaMA model
tokenizer = AutoTokenizer.from_pretrained(game_config.MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(game_config.MODEL_NAME)

def generate_strategy(role):
    """
    Generate a dynamic strategy for a given role using LLaMA 3.

    Args:
        role (str): The role for which to generate a strategy.

    Returns:
        str: Generated strategy in natural language.
    """
    base_strategy = game_config.ROLE_DESCRIPTIONS[role]["strategy"]
    prompt = f"Role: {role}\nBase Strategy: {base_strategy}\nDynamic Strategy:"

    # Tokenize input
    inputs = tokenizer(prompt, return_tensors="pt")

    # Generate strategy
    output = model.generate(
        inputs["input_ids"],
        max_length=150,
        temperature=game_config.GENERATION_TEMPERATURE,
        top_k=game_config.GENERATION_TOP_K,
        top_p=game_config.GENERATION_TOP_P
    )

    return tokenizer.decode(output[0], skip_special_tokens=True)

# Example usage
if __name__ == "__main__":
    role = "werewolf"
    print(f"Dynamic Strategy for {role}:")
    print(generate_strategy(role))
