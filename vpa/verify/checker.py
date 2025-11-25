#!/usr/bin/env python3
"""
Verifier - Simple checks for candidate quality.
"""

from typing import List, Dict, Any, Optional
import re
import logging
from .code_executor import CodeExecutor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SimpleVerifier:
    """Simple verifier with basic quality checks."""

    def __init__(self):
        """Initialize the verifier."""
        self.executor = CodeExecutor()

    def verify(self, candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Verify candidates with simple quality checks.

        Args:
            candidates: List of candidate dictionaries

        Returns:
            List of candidates with added 'score' and 'checks' fields
        """
        if not candidates:
            logger.warning("No candidates to verify")
            return []

        print(f"\n🔍 Verifying {len(candidates)} candidates...")
        print("=" * 60)

        verified = []

        for candidate in candidates:
            text = candidate.get('text', '')

            # Guard against empty or missing text
            if not text or not text.strip():
                logger.warning(f"Candidate {candidate.get('id', '?')} has empty text, skipping")
                continue

            # Run checks
            checks = {
                'length': self._check_length(text),
                'completeness': self._check_completeness(text),
                'coherence': self._check_coherence(text),
                'format': self._check_format(text)
            }
            
            # Code execution check (optional, only if code blocks exist)
            code_score = self._check_code_execution(text)
            if code_score is not None:
                checks['code_exec'] = code_score

            # Calculate composite score (0.0 to 1.0)
            score = sum(checks.values()) / len(checks)

            # Add to candidate
            verified_candidate = candidate.copy()
            verified_candidate['score'] = score
            verified_candidate['checks'] = checks
            verified_candidate['rank'] = 0  # Will be set later

            verified.append(verified_candidate)

            # Print results
            print(f"\n📊 Candidate {candidate['id']}:")
            print(f"   Score: {score:.2f}")
            print(f"   Checks:")
            for check_name, check_score in checks.items():
                status = "✅" if check_score >= 0.7 else "⚠️" if check_score >= 0.4 else "❌"
                print(f"     {status} {check_name}: {check_score:.2f}")

        # Guard against no valid candidates
        if not verified:
            logger.error("All candidates were filtered out during verification")
            raise ValueError("No valid candidates after verification")

        # Rank candidates by score
        verified.sort(key=lambda x: x['score'], reverse=True)
        for i, candidate in enumerate(verified, 1):
            candidate['rank'] = i

        print("\n" + "=" * 60)
        print(f"✨ Verification complete! Best score: {verified[0]['score']:.2f}")
        logger.info(f"Verified {len(verified)} candidates, best score: {verified[0]['score']:.2f}")

        return verified

    def _check_length(self, text: str) -> float:
        """
        Check if response has reasonable length.
        Too short = incomplete, too long = verbose.

        Returns score 0.0-1.0
        """
        length = len(text)

        if length < 20:
            return 0.2  # Too short
        elif length < 50:
            return 0.6  # Somewhat short
        elif length < 500:
            return 1.0  # Good length
        elif length < 1000:
            return 0.8  # Bit long
        else:
            return 0.6  # Too verbose

    def _check_completeness(self, text: str) -> float:
        """
        Check if response seems complete.
        Looks for sentence endings, not trailing off.

        Returns score 0.0-1.0
        """
        text = text.strip()

        if not text:
            return 0.0

        # Check if ends with proper punctuation
        if text[-1] in '.!?':
            return 1.0
        elif text[-1] in ',;:':
            return 0.4  # Incomplete sentence
        else:
            return 0.6  # No punctuation but might be ok

    def _check_coherence(self, text: str) -> float:
        """
        Check basic coherence indicators.
        Looks for sentence structure, capitalization.

        Returns score 0.0-1.0
        """
        if not text:
            return 0.0

        score = 0.0

        # Has at least one sentence-like structure
        if '.' in text or '!' in text or '?' in text:
            score += 0.3

        # Starts with capital letter
        if text and text[0].isupper():
            score += 0.3

        # Has multiple sentences (more complete)
        sentence_count = len(re.findall(r'[.!?]+', text))
        if sentence_count >= 2:
            score += 0.4
        elif sentence_count >= 1:
            score += 0.2

        return min(score, 1.0)

    def _check_format(self, text: str) -> float:
        """
        Check basic formatting quality.
        No excessive repetition, reasonable structure.

        Returns score 0.0-1.0
        """
        if not text:
            return 0.0

        score = 1.0

        # Check for excessive repetition (same word 5+ times in a row)
        words = text.lower().split()
        if len(words) > 0:
            for i in range(len(words) - 4):
                if words[i] == words[i+1] == words[i+2] == words[i+3] == words[i+4]:
                    score -= 0.5
                    break

        # Check for excessive punctuation (e.g., "!!!!!")
        if re.search(r'[!?.]{5,}', text):
            score -= 0.3

        # Check for excessive newlines
        if text.count('\n\n\n') > 0:
            score -= 0.2

        return max(score, 0.0)

    def _check_code_execution(self, text: str) -> Optional[float]:
        """
        Check if code blocks execute successfully.
        
        Returns:
            1.0 if success
            0.0 if failure
            None if no code blocks found
        """
        code_blocks = self.executor.extract_code_blocks(text)
        if not code_blocks:
            return None
            
        logger.info(f"Found {len(code_blocks)} code blocks to execute")
        
        all_success = True
        for i, code in enumerate(code_blocks):
            result = self.executor.execute_code(code)
            if not result['success']:
                logger.warning(f"Code block {i+1} failed: {result['error']}")
                all_success = False
            else:
                logger.info(f"Code block {i+1} executed successfully")
                
        return 1.0 if all_success else 0.0

    def get_best_candidate(self, verified_candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Get the best (highest scoring) candidate.

        Args:
            verified_candidates: List of verified candidates

        Returns:
            Best candidate dictionary
        """
        if not verified_candidates:
            raise ValueError("No candidates to select from")

        # Already sorted by score in verify()
        return verified_candidates[0]


def main():
    """Example usage."""
    # Example candidates
    candidates = [
        {
            "id": 1,
            "text": "Machine learning is a field of AI that enables computers to learn from data.",
            "temperature": 0.6
        },
        {
            "id": 2,
            "text": "ML",  # Too short
            "temperature": 0.7
        },
        {
            "id": 3,
            "text": "Machine learning is a subset of artificial intelligence that focuses on the development of algorithms and statistical models that enable computers to improve their performance on tasks through experience and data, without being explicitly programmed.",
            "temperature": 0.9
        }
    ]

    verifier = SimpleVerifier()
    verified = verifier.verify(candidates)

    print("\n" + "=" * 60)
    print("VERIFICATION RESULTS")
    print("=" * 60)

    for candidate in verified:
        print(f"\nRank {candidate['rank']}: Candidate {candidate['id']}")
        print(f"Score: {candidate['score']:.2f}")
        print(f"Text: {candidate['text'][:80]}...")

    best = verifier.get_best_candidate(verified)
    print(f"\n🏆 Best candidate: #{best['id']} (score: {best['score']:.2f})")


if __name__ == "__main__":
    main()
