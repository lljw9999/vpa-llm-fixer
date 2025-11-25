#!/usr/bin/env python3
"""
Draft Generator - Generates k candidate answers using Ollama.
"""

import logging
from typing import List, Dict, Any

# Import from parent package
try:
    from ollama_client import OllamaClient
except ImportError:
    # Fallback for direct execution
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
    from ollama_client import OllamaClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DraftGenerator:
    """Generates multiple candidate answers for a given question."""

    def __init__(
        self,
        model: str = "qwen3:1.7b",
        base_url: str = "http://127.0.0.1:11434"
    ):
        """
        Initialize the draft generator.

        Args:
            model: Ollama model to use
            base_url: Ollama API base URL
        """
        self.client = OllamaClient(base_url=base_url, model=model)
        self.model = model
        self.base_url = base_url

    def generate(
        self,
        question: str,
        k: int = 3,
        temperature_range: tuple = (0.6, 0.9)
    ) -> List[Dict[str, Any]]:
        """
        Generate k diverse candidate answers.

        Args:
            question: The question to answer
            k: Number of candidates to generate (default: 3)
            temperature_range: (min, max) temperature for diversity

        Returns:
            List of candidate dictionaries with 'text', 'temperature', 'metadata'
        """
        if k < 1:
            raise ValueError("k must be at least 1")

        print(f"\n🎯 Generating {k} candidate answers...")
        print(f"📝 Question: {question}")
        print(f"🤖 Model: {self.model}")
        print(f"🌐 Ollama API: {self.base_url}")
        print("-" * 60)

        candidates = []
        temp_min, temp_max = temperature_range

        for i in range(k):
            # Vary temperature across candidates for diversity
            if k == 1:
                temperature = (temp_min + temp_max) / 2
            else:
                temperature = temp_min + (temp_max - temp_min) * (i / (k - 1))

            print(f"\n🔄 Generating candidate {i+1}/{k} (temp={temperature:.2f})...")

            try:
                response = self.client.ask(question, temperature=temperature)

                # Guard against empty responses
                if not response or not response.strip():
                    logger.warning(f"Candidate {i+1} returned empty response, skipping")
                    print(f"⚠️ Candidate {i+1} returned empty response, skipping")
                    continue

                candidate = {
                    "id": i + 1,
                    "text": response,
                    "temperature": temperature,
                    "metadata": {
                        "model": self.model,
                        "question": question
                    }
                }

                candidates.append(candidate)
                print(f"✅ Candidate {i+1}: {response[:80]}...")

            except Exception as e:
                logger.error(f"Error generating candidate {i+1}: {e}", exc_info=True)
                print(f"❌ Error generating candidate {i+1}: {e}")
                # Continue to next candidate

        print(f"\n✨ Generated {len(candidates)}/{k} candidates successfully")
        return candidates


def main():
    """Example usage."""
    generator = DraftGenerator()

    # Example question
    question = "What is machine learning?"

    # Generate 3 candidates
    candidates = generator.generate(question, k=3)

    # Print results
    print("\n" + "=" * 60)
    print("GENERATED CANDIDATES")
    print("=" * 60)

    for candidate in candidates:
        print(f"\nCandidate {candidate['id']} (temp={candidate['temperature']:.2f}):")
        print(f"{candidate['text']}\n")
        print("-" * 60)


if __name__ == "__main__":
    main()
