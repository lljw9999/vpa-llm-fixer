#!/usr/bin/env python3
"""
Evaluator - Tiny test sets and scoring.
"""

from typing import List, Dict, Any, Optional
import re


# Tiny test sets
TINY_QA_SET = [
    {
        "question": "What is the capital of France?",
        "answer": "Paris",
        "acceptable": ["paris", "the capital of france is paris"]
    },
    {
        "question": "What is 2 + 2?",
        "answer": "4",
        "acceptable": ["4", "four", "2+2=4", "2 + 2 = 4", "the answer is 4"]
    },
    {
        "question": "What color is the sky on a clear day?",
        "answer": "blue",
        "acceptable": ["blue", "the sky is blue", "it's blue"]
    }
]

TINY_CODE_SET = [
    {
        "question": "Write a Python function to add two numbers.",
        "keywords": ["def", "return", "+", "add"],
        "type": "code"
    }
]


class SimpleEvaluator:
    """Simple evaluator with tiny test sets."""

    def __init__(self):
        """Initialize evaluator."""
        self.qa_set = TINY_QA_SET
        self.code_set = TINY_CODE_SET

    def evaluate_response(
        self,
        question: str,
        response: str,
        gold_answer: Optional[str] = None,
        acceptable: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Evaluate a single response.

        Args:
            question: The question asked
            response: The model's response
            gold_answer: The correct answer (if known)
            acceptable: List of acceptable answer variations

        Returns:
            Dictionary with evaluation results
        """
        response_lower = response.lower().strip()

        result = {
            "question": question,
            "response": response,
            "gold_answer": gold_answer,
            "correct": False,
            "partial": False,
            "score": 0.0
        }

        if gold_answer is None:
            # No gold answer, can't evaluate correctness
            result["score"] = 0.5  # Neutral
            return result

        gold_lower = gold_answer.lower().strip()

        # Exact match
        if response_lower == gold_lower:
            result["correct"] = True
            result["score"] = 1.0
            return result

        # Check acceptable variations
        if acceptable:
            for accept in acceptable:
                if accept.lower() in response_lower:
                    result["correct"] = True
                    result["score"] = 1.0
                    return result

        # Partial match (gold answer is substring of response)
        if gold_lower in response_lower:
            result["partial"] = True
            result["score"] = 0.7
            return result

        # No match
        result["score"] = 0.0
        return result

    def evaluate_on_tiny_set(
        self,
        generate_fn,
        test_set: str = "qa",
        k: int = 3
    ) -> Dict[str, Any]:
        """
        Evaluate on a tiny test set.

        Args:
            generate_fn: Function that takes question and returns candidates
            test_set: "qa" or "code"
            k: Number of candidates to generate per question

        Returns:
            Dictionary with evaluation metrics
        """
        if test_set == "qa":
            dataset = self.qa_set
        elif test_set == "code":
            dataset = self.code_set
        else:
            raise ValueError(f"Unknown test set: {test_set}")

        print(f"\n📊 Evaluating on {test_set.upper()} test set ({len(dataset)} questions)")
        print("=" * 60)

        results = []
        total_correct = 0
        total_partial = 0
        total_questions = len(dataset)

        for i, item in enumerate(dataset, 1):
            question = item["question"]
            print(f"\n[{i}/{total_questions}] Question: {question}")

            # Generate candidates
            candidates = generate_fn(question, k=k)

            if not candidates:
                print("  ❌ No candidates generated")
                continue

            # Get best candidate (first one, assumed highest score from verifier)
            best = candidates[0]
            response = best.get('text', '')

            # Evaluate
            if test_set == "qa":
                eval_result = self.evaluate_response(
                    question,
                    response,
                    gold_answer=item.get("answer"),
                    acceptable=item.get("acceptable")
                )

                if eval_result["correct"]:
                    print(f"  ✅ CORRECT (score: {eval_result['score']:.2f})")
                    total_correct += 1
                elif eval_result["partial"]:
                    print(f"  ⚠️  PARTIAL (score: {eval_result['score']:.2f})")
                    total_partial += 1
                else:
                    print(f"  ❌ WRONG (score: {eval_result['score']:.2f})")

                print(f"     Expected: {item['answer']}")
                print(f"     Got: {response[:100]}...")

            elif test_set == "code":
                # Simple keyword check for code
                keywords = item.get("keywords", [])
                found_keywords = [kw for kw in keywords if kw in response.lower()]
                score = len(found_keywords) / len(keywords) if keywords else 0.0

                eval_result = {
                    "question": question,
                    "response": response,
                    "keywords_found": found_keywords,
                    "keywords_total": len(keywords),
                    "score": score
                }

                if score >= 0.75:
                    print(f"  ✅ GOOD (score: {score:.2f})")
                    total_correct += 1
                elif score >= 0.5:
                    print(f"  ⚠️  PARTIAL (score: {score:.2f})")
                    total_partial += 1
                else:
                    print(f"  ❌ POOR (score: {score:.2f})")

                print(f"     Keywords: {found_keywords}/{keywords}")
                print(f"     Response: {response[:100]}...")

            results.append(eval_result)

        # Calculate metrics
        accuracy = total_correct / total_questions if total_questions > 0 else 0.0
        partial_rate = total_partial / total_questions if total_questions > 0 else 0.0

        print("\n" + "=" * 60)
        print("📈 EVALUATION RESULTS")
        print("=" * 60)
        print(f"Total Questions: {total_questions}")
        print(f"Correct: {total_correct} ({accuracy * 100:.1f}%)")
        print(f"Partial: {total_partial} ({partial_rate * 100:.1f}%)")
        print(f"Wrong: {total_questions - total_correct - total_partial}")
        print(f"\n🎯 Accuracy: {accuracy:.2%}")

        return {
            "test_set": test_set,
            "total": total_questions,
            "correct": total_correct,
            "partial": total_partial,
            "accuracy": accuracy,
            "results": results
        }

    def compare_candidates(
        self,
        candidates: List[Dict[str, Any]],
        question: str,
        gold_answer: Optional[str] = None
    ) -> None:
        """
        Compare all candidates for a question.

        Args:
            candidates: List of candidate dictionaries
            question: The question
            gold_answer: The correct answer (if known)
        """
        print(f"\n🔬 Comparing {len(candidates)} candidates")
        print(f"Question: {question}")
        if gold_answer:
            print(f"Gold Answer: {gold_answer}")
        print("=" * 60)

        for candidate in candidates:
            text = candidate.get('text', '')
            score = candidate.get('score', 0.0)
            rank = candidate.get('rank', '?')

            print(f"\nCandidate {candidate.get('id')} (Rank {rank}):")
            print(f"  Verifier Score: {score:.2f}")
            print(f"  Response: {text[:150]}...")

            if gold_answer:
                eval_result = self.evaluate_response(question, text, gold_answer)
                status = "✅" if eval_result["correct"] else "⚠️" if eval_result["partial"] else "❌"
                print(f"  Correctness: {status} (score: {eval_result['score']:.2f})")


def main():
    """Example usage."""
    evaluator = SimpleEvaluator()

    # Example: Evaluate a single response
    print("=" * 60)
    print("Example: Single Response Evaluation")
    print("=" * 60)

    result = evaluator.evaluate_response(
        question="What is the capital of France?",
        response="The capital of France is Paris.",
        gold_answer="Paris",
        acceptable=["paris", "the capital of france is paris"]
    )

    print(f"Question: {result['question']}")
    print(f"Response: {result['response']}")
    print(f"Gold: {result['gold_answer']}")
    print(f"Correct: {result['correct']}")
    print(f"Score: {result['score']:.2f}")

    # Example: Compare candidates
    print("\n" + "=" * 60)
    print("Example: Candidate Comparison")
    print("=" * 60)

    candidates = [
        {"id": 1, "text": "Paris", "score": 0.95, "rank": 1},
        {"id": 2, "text": "The capital is Paris.", "score": 0.88, "rank": 2},
        {"id": 3, "text": "London", "score": 0.75, "rank": 3}
    ]

    evaluator.compare_candidates(
        candidates,
        question="What is the capital of France?",
        gold_answer="Paris"
    )


if __name__ == "__main__":
    main()
