"""Reward computation for training."""

import torch
import re
import logging
from typing import List, Dict, Tuple
from difflib import SequenceMatcher


logger = logging.getLogger(__name__)


class RewardComputer:
    """Compute rewards based on correctness of model outputs."""
    
    def __init__(self, reward_type: str = "exact_match"):
        """
        Initialize reward computer.
        
        Args:
            reward_type: Type of reward ("exact_match", "f1", "similarity")
        """
        self.reward_type = reward_type
    
    def compute_exact_match(self, prediction: str, target: str) -> float:
        """
        Compute exact match reward.
        
        Args:
            prediction: Model's prediction
            target: Ground truth
            
        Returns:
            1.0 if exact match, 0.0 otherwise
        """
        # Normalize: strip whitespace, lowercase, remove punctuation
        pred_norm = self._normalize(prediction)
        target_norm = self._normalize(target)
        
        if pred_norm == target_norm:
            return 1.0
        else:
            return 0.0
    
    def compute_f1_reward(self, prediction: str, target: str) -> float:
        """
        Compute F1-based reward.
        
        Args:
            prediction: Model's prediction
            target: Ground truth
            
        Returns:
            F1 score between 0 and 1
        """
        pred_tokens = self._tokenize(prediction)
        target_tokens = self._tokenize(target)
        
        if len(target_tokens) == 0:
            return 1.0 if len(pred_tokens) == 0 else 0.0
        
        # Compute precision and recall
        common = sum(1 for t in pred_tokens if t in target_tokens)
        
        if common == 0:
            return 0.0
        
        precision = common / len(pred_tokens) if pred_tokens else 0
        recall = common / len(target_tokens)
        
        if precision + recall == 0:
            return 0.0
        
        f1 = 2 * (precision * recall) / (precision + recall)
        return f1
    
    def compute_similarity_reward(self, prediction: str, target: str) -> float:
        """
        Compute similarity-based reward using SequenceMatcher.
        
        Args:
            prediction: Model's prediction
            target: Ground truth
            
        Returns:
            Similarity score between 0 and 1
        """
        pred_norm = self._normalize(prediction)
        target_norm = self._normalize(target)
        
        matcher = SequenceMatcher(None, pred_norm, target_norm)
        ratio = matcher.ratio()
        
        return ratio
    
    def compute_reasoning_correctness(
        self,
        prediction: str,
        target: str,
        include_intermediate: bool = False,
    ) -> float:
        """
        Compute reasoning correctness reward.
        
        This checks if the final answer is correct, and optionally
        gives partial credit for correct intermediate steps.
        
        Args:
            prediction: Model's full response (may include thinking)
            target: Ground truth answer
            include_intermediate: Whether to check intermediate steps
            
        Returns:
            Reward between 0 and 1
        """
        # Extract final answer
        final_answer = self._extract_final_answer(prediction)
        
        # Base reward for correct final answer
        exact_match = self.compute_exact_match(final_answer, target)
        
        if exact_match == 1.0:
            return 1.0
        
        # Partial reward for close answers
        similarity = self.compute_similarity_reward(final_answer, target)
        
        if include_intermediate:
            # Check if thinking block exists (proxy for reasoning effort)\n            has_thinking = "<think>" in prediction and "</think>" in prediction\n            thinking_reward = 0.1 if has_thinking else 0.0\n            return min(1.0, similarity + thinking_reward)\n        \n        return similarity\n    \n    def compute_batch_rewards(self, predictions: List[str], targets: List[str]) -> torch.Tensor:\n        \"\"\"\n        Compute rewards for a batch.\n        \n        Args:\n            predictions: List of model predictions\n            targets: List of ground truths\n            \n        Returns:\n            Tensor of rewards [batch_size]\n        \"\"\"\n        rewards = []\n        \n        for pred, target in zip(predictions, targets):\n            if self.reward_type == "exact_match":\n                reward = self.compute_exact_match(pred, target)\n            elif self.reward_type == "f1":\n                reward = self.compute_f1_reward(pred, target)\n            elif self.reward_type == "similarity":\n                reward = self.compute_similarity_reward(pred, target)\n            else:\n                raise ValueError(f"Unknown reward type: {self.reward_type}")\n            \n            rewards.append(reward)\n        \n        return torch.tensor(rewards, dtype=torch.float32)\n    \n    @staticmethod\n    def _normalize(text: str) -> str:\n        \"\"\"Normalize text for comparison.\"\"\"\n        # Remove extra whitespace\n        text = " ".join(text.split())\n        # Lowercase\n        text = text.lower()\n        # Remove punctuation\n        text = re.sub(r"[^\\w\\s]\", \"\", text)\n        return text\n    \n    @staticmethod\n    def _tokenize(text: str) -> List[str]:\n        \"\"\"Tokenize text.\"\"\"\n        text = RewardComputer._normalize(text)\n        return text.split()\n    \n    @staticmethod\n    def _extract_final_answer(text: str) -> str:\n        \"\"\"Extract final answer from response (after </think> if present).\"\"\"\n        if \"</think>\" in text:\n            # Get text after thinking block\n            after_think = text.split(\"</think>\")[-1]\n            return after_think.strip()\n        else:\n            return text.strip()\n\n\ndef compute_rewards_for_batch(\n    predictions: List[str],\n    targets: List[str],\n    reward_type: str = \"exact_match\",\n) -> torch.Tensor:\n    \"\"\"\n    Compute rewards for a batch of predictions.\n    \n    Args:\n        predictions: List of model predictions\n        targets: List of ground truths\n        reward_type: Type of reward computation\n        \n    Returns:\n        Tensor of rewards [batch_size]\n    \"\"\"\n    computer = RewardComputer(reward_type=reward_type)\n    return computer.compute_batch_rewards(predictions, targets)\n\n\ndef reward_fn(\n    batch_predictions: List[str],\n    batch_targets: List[str],\n) -> torch.Tensor:\n    \"\"\"\n    Default reward function.\n    \n    Args:\n        batch_predictions: Batch of predictions\n        batch_targets: Batch of targets\n        \n    Returns:\n        Rewards tensor\n    \"\"\"\n    return compute_rewards_for_batch(batch_predictions, batch_targets, \"exact_match\")\n