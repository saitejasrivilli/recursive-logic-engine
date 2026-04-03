"""Data quality filtering using a fast scorer model."""

import torch
import logging
from typing import List, Dict, Tuple
import numpy as np
from torch.utils.data import DataLoader


logger = logging.getLogger(__name__)


class DataQualityFilter:
    """Filter high-quality training examples using a fast scorer model."""
    
    def __init__(
        self,
        scorer_model,
        scorer_tokenizer,
        device: str = "cuda" if torch.cuda.is_available() else "cpu",
    ):
        """
        Initialize quality filter.
        
        Args:
            scorer_model: Fast scorer model (e.g., GPT2-small)
            scorer_tokenizer: Tokenizer for scorer
            device: Device to run scorer on
        """
        self.scorer_model = scorer_model.to(device).eval()
        self.scorer_tokenizer = scorer_tokenizer
        self.device = device
    
    def score_example(self, example: Dict[str, str]) -> float:
        """
        Score a single example.
        
        Uses a heuristic: reward is based on whether the model
        can predict aspects of the correct answer given the question.
        
        Args:
            example: Dict with 'input' and 'output' keys
            
        Returns:
            Score between 0 and 1
        """
        with torch.no_grad():
            # Tokenize input
            inputs = self.scorer_tokenizer(
                example['input'],
                truncation=True,
                max_length=256,
                return_tensors="pt",
            ).to(self.device)
            
            # Get model logits
            outputs = self.scorer_model(**inputs, output_hidden_states=True)
            
            # Simple heuristic: average magnitude of final layer hidden states
            # (proxy for "how much information did the model process")
            hidden = outputs.hidden_states[-1]
            score = float(torch.abs(hidden).mean().item())
            
            # Normalize to [0, 1]
            score = min(1.0, score / 10.0)
        
        return score
    
    def score_batch(self, examples: List[Dict[str, str]]) -> List[float]:
        """
        Score a batch of examples in parallel.
        
        Args:
            examples: List of examples
            
        Returns:
            List of scores
        """
        scores = []
        
        with torch.no_grad():
            for example in examples:
                score = self.score_example(example)
                scores.append(score)
        
        return scores
    
    def filter_top_k(
        self,
        data: List[Dict[str, str]],
        top_k: int,
        batch_size: int = 64,
    ) -> Tuple[List[Dict[str, str]], List[float]]:
        """
        Filter and return top-k highest quality examples.
        
        Args:
            data: Full dataset
            top_k: Number of top examples to keep
            batch_size: Batch size for scoring
            
        Returns:
            Tuple of (filtered_data, scores)
        """
        logger.info(f"Scoring {len(data)} examples for quality...")
        
        all_scores = []
        for i in range(0, len(data), batch_size):
            batch = data[i:i+batch_size]
            batch_scores = self.score_batch(batch)
            all_scores.extend(batch_scores)
        
        # Get indices of top-k
        scores_array = np.array(all_scores)
        top_indices = np.argsort(scores_array)[-top_k:][::-1]
        
        filtered_data = [data[i] for i in top_indices]
        filtered_scores = [all_scores[i] for i in top_indices]
        
        logger.info(
            f"Filtered to top {top_k} examples. "
            f"Mean score: {np.mean(filtered_scores):.4f}, "
            f"Std: {np.std(filtered_scores):.4f}"
        )
        
        return filtered_data, filtered_scores
    
    def filter_percentile(
        self,
        data: List[Dict[str, str]],
        percentile: float = 0.25,  # Keep top 25%
        batch_size: int = 64,
    ) -> Tuple[List[Dict[str, str]], List[float]]:
        """
        Filter by percentile (e.g., keep top 25%).
        
        Args:
            data: Full dataset
            percentile: Percentile to keep (0-1)
            batch_size: Batch size for scoring
            
        Returns:
            Tuple of (filtered_data, scores)
        """
        top_k = max(1, int(len(data) * percentile))
        return self.filter_top_k(data, top_k, batch_size)


def apply_quality_filter(
    data: List[Dict[str, str]],
    scorer_model,
    scorer_tokenizer,
    top_k: int = None,
    percentile: float = None,
    device: str = "cuda" if torch.cuda.is_available() else "cpu",
) -> Tuple[List[Dict[str, str]], DataQualityFilter]:
    """
    Apply quality filter to dataset.
    
    Args:
        data: Dataset to filter
        scorer_model: Fast scorer model
        scorer_tokenizer: Scorer tokenizer
        top_k: Keep top-k examples (mutually exclusive with percentile)
        percentile: Keep top percentile (0-1)
        device: Device for scorer
        
    Returns:
        Tuple of (filtered_data, quality_filter)
    """
    quality_filter = DataQualityFilter(
        scorer_model,
        scorer_tokenizer,
        device=device,
    )
    
    if top_k is not None:
        filtered_data, scores = quality_filter.filter_top_k(data, top_k)
    elif percentile is not None:
        filtered_data, scores = quality_filter.filter_percentile(data, percentile)
    else:
        raise ValueError("Either top_k or percentile must be specified")
    
    return filtered_data, quality_filter
