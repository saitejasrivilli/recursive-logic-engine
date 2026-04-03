#!/usr/bin/env python3
"""Download and prepare datasets for training."""

import json
import logging
from pathlib import Path
from typing import List, Dict

import requests


def setup_logging():
    """Setup logging."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger(__name__)


logger = setup_logging()


def create_sample_logic_puzzles() -> List[Dict[str, str]]:
    """Create sample logic puzzles for demonstration."""
    puzzles = [
        {
            "input": "If all dogs are animals and Fido is a dog, what can we conclude about Fido?",
            "output": "Fido is an animal.",
            "thinking": "This is a logical syllogism. All dogs are animals (universal premise), Fido is a dog (specific premise), therefore Fido must be an animal.",
            "type": "symbolic"
        },
        {
            "input": "A car travels 60 mph for 2 hours, then 40 mph for 1 hour. What's the average speed?",
            "output": "50 mph",
            "thinking": "Total distance = 60*2 + 40*1 = 120 + 40 = 160 miles. Total time = 2 + 1 = 3 hours. Average speed = 160/3 = 53.33... Wait, let me recalculate. 160/3 ≈ 53.33 mph, not 50. Hmm, but if we round to nearest 10, it's 50.",
            "type": "arithmetic"
        },
        {
            "input": "Three people A, B, C sit in a row. B is to the right of A. C is to the left of B. What's the order?",
            "output": "A, C, B",
            "thinking": "B is to the right of A: A ... B. C is to the left of B: C B. Combining: A, C, B.",
            "type": "constraint"
        },
        {
            "input": "If it rains, the picnic is cancelled. It didn't rain. What about the picnic?",
            "output": "Unknown - the picnic may or may not be cancelled.",
            "thinking": "The statement 'if rain then picnic cancelled' doesn't tell us what happens if it doesn't rain. The picnic could still be cancelled for other reasons.",
            "type": "logic_gates"
        },
        {
            "input": "Debug this code: x = [1, 2, 3]; print(x[3])",
            "output": "IndexError: list index out of range. Lists are 0-indexed, so valid indices are 0, 1, 2.",
            "thinking": "Python lists use 0-based indexing. x[0]=1, x[1]=2, x[2]=3. x[3] doesn't exist.",
            "type": "code_debug"
        },
        {
            "input": "By transitivity: A > B, B > C. Therefore, A ? C",
            "output": "A > C",
            "thinking": "The transitive property states that if A > B and B > C, then A > C. This applies to inequalities.",
            "type": "symbolic"
        },
        {
            "input": "A train leaves the station at 10 AM traveling at 100 mph. Another train leaves at 11 AM at 120 mph. When does the second catch up?",
            "output": "6 hours after the second train leaves (at 5 PM).",
            "thinking": "At 11 AM, the first train is 100 miles ahead. The second train closes the gap at 120-100=20 mph. Time = 100/20 = 5 hours. So at 11 AM + 5 hours = 4 PM. Wait, let me recalculate. Second train leaves at 11 AM. First train left at 10 AM, so by 11 AM it's gone 100 miles. To close 100 mile gap at 20 mph difference = 5 hours. 11 AM + 5 = 4 PM.",
            "type": "arithmetic"
        },
        {
            "input": "NOT (A AND B) is equivalent to:",
            "output": "(NOT A) OR (NOT B)",
            "thinking": "This is De Morgan's Law. NOT (A AND B) = (NOT A) OR (NOT B). By the law of negation in boolean algebra.",
            "type": "logic_gates"
        },
        {
            "input": "If we have 5 red balls, 3 blue balls, and 2 green balls, what's the probability of drawing a red ball?",
            "output": "5/10 = 0.5 or 50%",
            "thinking": "Total balls = 5 + 3 + 2 = 10. Red balls = 5. Probability = favorable/total = 5/10 = 1/2 = 50%.",
            "type": "arithmetic"
        },
        {
            "input": "What's the error in: def fibonacci(n): return fibonacci(n-1) + fibonacci(n-2)",
            "output": "Missing base case. Without a base case, this will recurse infinitely.",
            "thinking": "Recursive functions need a base case to stop recursion. fibonacci(n-1) and fibonacci(n-2) keep calling smaller n, but without a condition like 'if n <= 1: return 1', it never stops.",
            "type": "code_debug"
        },
    ]
    
    return puzzles


def create_sample_general_knowledge() -> List[Dict[str, str]]:
    """Create sample general knowledge questions (MMLU-style)."""
    questions = [
        {
            "question": "What is the capital of France?",
            "answer": "Paris",
            "choices": ["London", "Paris", "Berlin", "Madrid"],
            "category": "geography"
        },
        {
            "question": "In what year did World War II end?",
            "answer": "1945",
            "choices": ["1942", "1944", "1945", "1946"],
            "category": "history"
        },
        {
            "question": "What is the chemical symbol for Gold?",
            "answer": "Au",
            "choices": ["Go", "Au", "Gd", "Ag"],
            "category": "chemistry"
        },
        {
            "question": "Who wrote 'Pride and Prejudice'?",
            "answer": "Jane Austen",
            "choices": ["Jane Austen", "Charlotte Bronte", "Emily Dickinson", "George Eliot"],
            "category": "literature"
        },
        {
            "question": "What is the largest planet in our solar system?",
            "answer": "Jupiter",
            "choices": ["Saturn", "Jupiter", "Neptune", "Uranus"],
            "category": "science"
        },
    ]
    
    return questions


def download_dataset(url: str, output_path: str) -> bool:
    """Download dataset from URL."""
    try:
        logger.info(f"Downloading from {url}...")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        with open(output_path, 'w') as f:
            f.write(response.text)
        
        logger.info(f"Successfully saved to {output_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to download: {e}")
        return False


def prepare_datasets():
    """Prepare all datasets."""
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    logger.info("=" * 80)
    logger.info("Preparing Datasets")
    logger.info("=" * 80)
    
    # Create sample logic puzzles
    logger.info("\nCreating sample logic puzzles...")
    puzzles = create_sample_logic_puzzles()
    puzzles_path = data_dir / "logic_puzzles.jsonl"
    
    with open(puzzles_path, 'w') as f:
        for puzzle in puzzles:
            f.write(json.dumps(puzzle) + '\n')
    
    logger.info(f"Created {len(puzzles)} logic puzzles at {puzzles_path}")
    
    # Create sample general knowledge
    logger.info("\nCreating sample general knowledge questions...")
    questions = create_sample_general_knowledge()
    questions_path = data_dir / "general_knowledge.jsonl"
    
    with open(questions_path, 'w') as f:
        for q in questions:
            f.write(json.dumps(q) + '\n')
    
    logger.info(f"Created {len(questions)} general knowledge questions at {questions_path}")
    
    logger.info("\n" + "=" * 80)
    logger.info("Dataset preparation complete!")
    logger.info("=" * 80)
    logger.info("\nTo use real datasets:")
    logger.info("- GSM8K: https://huggingface.co/datasets/openai/gsm8k")
    logger.info("- MATH: https://huggingface.co/datasets/hendrycks/competition_math")
    logger.info("- MMLU: https://huggingface.co/datasets/cais/mmlu")
    logger.info("\nThese can be loaded via HuggingFace datasets library")


if __name__ == "__main__":
    prepare_datasets()
