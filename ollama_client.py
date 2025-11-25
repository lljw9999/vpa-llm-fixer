#!/usr/bin/env python3
"""
Simple Ollama API Client for interacting with local Ollama models.

Usage:
    from ollama_client import OllamaClient

    client = OllamaClient()
    response = client.ask("What is machine learning?")
    print(response)
"""

import requests
import json
import logging
from typing import Optional, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class OllamaClient:
    """Client for interacting with Ollama API."""

    def __init__(
        self,
        base_url: str = "http://127.0.0.1:11434",
        model: str = "qwen3:1.7b",
        temperature: float = 0.7,
        timeout: int = 60
    ):
        """
        Initialize Ollama client.

        Args:
            base_url: Base URL for Ollama API (default: http://127.0.0.1:11434)
            model: Model name to use (default: qwen3:1.7b)
            temperature: Sampling temperature 0.0-1.0 (default: 0.7)
            timeout: Request timeout in seconds (default: 60)
        """
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.temperature = temperature
        self.timeout = timeout
        self.generate_url = f"{self.base_url}/api/generate"
        self.chat_url = f"{self.base_url}/api/chat"

    def ask(
        self,
        prompt: str,
        stream: bool = False,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        system: Optional[str] = None
    ) -> str:
        """
        Ask a question to the model and get a response.

        Args:
            prompt: The question or prompt to send to the model
            stream: Whether to stream the response (default: False)
            temperature: Override default temperature for this request
            max_tokens: Maximum number of tokens to generate
            system: System prompt to set context/behavior

        Returns:
            The model's response as a string

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": stream,
            "options": {}
        }

        # Add optional parameters
        if temperature is not None:
            payload["options"]["temperature"] = temperature
        elif self.temperature != 0.7:  # Only add if not default
            payload["options"]["temperature"] = self.temperature

        if max_tokens is not None:
            payload["options"]["num_predict"] = max_tokens

        if system is not None:
            payload["system"] = system

        try:
            logger.debug(f"Sending request to {self.generate_url} with model {self.model}")
            response = requests.post(
                self.generate_url,
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()

            result = response.json()
            answer = result.get("response", "").strip()

            # Guard against empty responses
            if not answer:
                logger.warning(f"Empty response from Ollama for prompt: {prompt[:50]}...")
                raise RuntimeError("Ollama returned an empty response")

            logger.debug(f"Received response: {answer[:100]}...")
            return answer

        except requests.exceptions.Timeout:
            logger.error(f"Request timed out after {self.timeout}s")
            raise RuntimeError(f"Ollama API request timed out after {self.timeout}s")
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection error: {e}")
            raise RuntimeError(f"Cannot connect to Ollama at {self.base_url}. Is Ollama running?")
        except requests.exceptions.RequestException as e:
            logger.error(f"Ollama API request failed: {e}")
            raise RuntimeError(f"Ollama API request failed: {e}")

    def chat(
        self,
        messages: list,
        stream: bool = False,
        temperature: Optional[float] = None
    ) -> str:
        """
        Use the chat API with conversation history.

        Args:
            messages: List of message dicts with 'role' and 'content' keys
                     Example: [{"role": "user", "content": "Hello!"}]
            stream: Whether to stream the response (default: False)
            temperature: Override default temperature for this request

        Returns:
            The model's response as a string

        Example:
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "What is Python?"}
            ]
            response = client.chat(messages)
        """
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": stream,
            "options": {}
        }

        if temperature is not None:
            payload["options"]["temperature"] = temperature
        elif self.temperature != 0.7:
            payload["options"]["temperature"] = self.temperature

        try:
            logger.debug(f"Sending chat request to {self.chat_url} with model {self.model}")
            response = requests.post(
                self.chat_url,
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()

            result = response.json()
            message = result.get("message", {})
            answer = message.get("content", "").strip()

            # Guard against empty responses
            if not answer:
                logger.warning("Empty response from Ollama chat API")
                raise RuntimeError("Ollama chat API returned an empty response")

            logger.debug(f"Received chat response: {answer[:100]}...")
            return answer

        except requests.exceptions.Timeout:
            logger.error(f"Chat request timed out after {self.timeout}s")
            raise RuntimeError(f"Ollama chat API request timed out after {self.timeout}s")
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Chat connection error: {e}")
            raise RuntimeError(f"Cannot connect to Ollama at {self.base_url}. Is Ollama running?")
        except requests.exceptions.RequestException as e:
            logger.error(f"Ollama chat API request failed: {e}")
            raise RuntimeError(f"Ollama chat API request failed: {e}")

    def list_models(self) -> list:
        """
        List all available models.

        Returns:
            List of available model names
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=self.timeout
            )
            response.raise_for_status()

            result = response.json()
            models = result.get("models", [])
            return [model.get("name") for model in models]

        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to list models: {e}")

    def is_available(self) -> bool:
        """
        Check if Ollama API is available.

        Returns:
            True if API is reachable, False otherwise
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=5
            )
            return response.status_code == 200
        except:
            return False


# Convenience function for quick usage
def ask_ollama(prompt: str, model: str = "qwen3:1.7b") -> str:
    """
    Quick helper function to ask a question.

    Args:
        prompt: Question to ask
        model: Model to use (default: qwen3:1.7b)

    Returns:
        Model's response

    Example:
        >>> answer = ask_ollama("What is 2+2?")
        >>> print(answer)
    """
    client = OllamaClient(model=model)
    return client.ask(prompt)


def main():
    """Example usage and interactive mode."""
    print("=" * 60)
    print("Ollama Python Client")
    print("=" * 60)

    # Create client
    client = OllamaClient()

    # Check if Ollama is available
    print(f"\nChecking Ollama availability at {client.base_url}...")
    if not client.is_available():
        print("❌ Ollama is not available. Make sure it's running!")
        print("   Start it with: ollama serve")
        return

    print("✓ Ollama is available!")

    # List available models
    print("\nAvailable models:")
    try:
        models = client.list_models()
        for model in models:
            marker = "→" if model == client.model else " "
            print(f"  {marker} {model}")
    except Exception as e:
        print(f"  Could not list models: {e}")

    # Example questions
    print(f"\nUsing model: {client.model}")
    print("\n" + "=" * 60)
    print("Example Questions:")
    print("=" * 60)

    examples = [
        "What is machine learning in one sentence?",
        "Explain Python in 20 words.",
        "What is 25 * 4?"
    ]

    for i, question in enumerate(examples, 1):
        print(f"\nQ{i}: {question}")
        try:
            answer = client.ask(question)
            print(f"A{i}: {answer}")
        except Exception as e:
            print(f"❌ Error: {e}")

    # Interactive mode
    print("\n" + "=" * 60)
    print("Interactive Mode (type 'quit' or 'exit' to stop)")
    print("=" * 60)

    while True:
        try:
            prompt = input("\nYou: ").strip()

            if not prompt:
                continue

            if prompt.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break

            response = client.ask(prompt)
            print(f"Bot: {response}")

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
