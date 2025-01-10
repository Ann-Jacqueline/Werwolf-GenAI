import random
import logging
import time
from openai import OpenAI
import os


class GPTInteraction:
    """
    Handles interactions with the GPT model.
    """

    def __init__(self, logger=None, max_attempts=3, api_key=None, global_history=None):
        """
        Initializes the GPTInteraction module.

        Args:
            logger: Logger for logging interactions. Defaults to a new logger if None.
            max_attempts: Maximum retry attempts for valid suggestions.
            api_key: Optional API key for GPT interaction. Defaults to environment variable.
            global_history: GlobalHistoryModel instance for recording interactions. Optional.
        """
        self.api_key = api_key or os.getenv("YOUR_API_KEY")
        if not self.api_key:
            raise ValueError("API key is not provided.")
        self.client = OpenAI(api_key=self.api_key)
        self.logger = logger or logging.getLogger(__name__)
        self.max_attempts = max_attempts
        self.global_history = global_history

    def get_suggestion(self, prompt, valid_targets=None, prompt_type="general"):
        """
        Requests a suggestion from GPT based on the given prompt.

        Args:
            prompt (str): The input prompt for GPT.
            valid_targets (list, optional): A list of valid targets for validation.
            prompt_type (str): Type of the prompt for logging purposes.

        Returns:
            str: A valid response from GPT or a fallback suggestion.
        """
        attempts = 0
        delay = 1  # Initial delay in seconds

        while attempts < self.max_attempts:
            try:
                # Send request to GPT
                response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "system", "content": prompt}]
                )
                suggestion = response.choices[0].message.content.strip()

                # Log interaction
                self.logger.info({
                    "event": "GPT interaction",
                    "prompt_type": prompt_type,
                    "response": suggestion,
                    "valid_targets": valid_targets,
                    "attempt": attempts + 1
                })

                # Validate response
                if valid_targets and not self._validate_suggestion(suggestion, valid_targets):
                    self.logger.warning(f"Invalid suggestion: {suggestion}")
                else:
                    # Record to global history
                    if self.global_history:
                        self.global_history.record_event(
                            "gpt_interaction",
                            {
                                "prompt_type": prompt_type,
                                "prompt": prompt,
                                "response": suggestion,
                                "valid_targets": valid_targets,
                                "valid": True
                            }
                        )
                    return suggestion

            except Exception as e:
                self.logger.error(f"Error during GPT interaction: {e}")

            # Retry with exponential backoff
            attempts += 1
            self.logger.info(f"Retrying GPT interaction (Attempt {attempts}/{self.max_attempts})")
            time.sleep(delay)
            delay *= 2

        # Fallback suggestion
        fallback = self.fallback_suggestion(valid_targets)
        self.logger.error(f"All attempts failed. Returning fallback suggestion: {fallback}")
        if self.global_history:
            self.global_history.record_event(
                "gpt_interaction",
                {
                    "prompt_type": prompt_type,
                    "prompt": prompt,
                    "response": fallback,
                    "valid_targets": valid_targets,
                    "valid": False
                }
            )
        return fallback

    def fallback_suggestion(self, valid_targets):
        """
        Provides a fallback suggestion when all attempts fail.

        Args:
            valid_targets (list): List of valid targets for fallback selection.

        Returns:
            str: A fallback suggestion.
        """
        if valid_targets:
            return random.choice(valid_targets)
        return "No valid targets available."

    @staticmethod
    def _validate_suggestion(suggestion, valid_targets):
        """
        Validates the GPT response based on provided targets.

        Args:
            suggestion (str): The GPT response to validate.
            valid_targets (list): List of valid targets or criteria.

        Returns:
            bool: True if the suggestion is valid, False otherwise.
        """
        if not suggestion or not valid_targets:
            return False

        # Check for direct matches with valid targets
        return any(
            f"Player {target}" in suggestion or suggestion.strip() == target
            for target in valid_targets
        )