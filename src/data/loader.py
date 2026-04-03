"""Data loading and preprocessing utilities."""

import torch
from torch.utils.data import Dataset, DataLoader
from typing import Dict, List, Tuple, Optional
import json
from pathlib import Path
import logging
from transformers import AutoTokenizer


logger = logging.getLogger(__name__)


class LogicPuzzleDataset(Dataset):
    """Dataset for logic puzzles with <think> tag support."""
    
    def __init__(
        self,
        examples: List[Dict[str, str]],
        tokenizer,
        max_length: int = 512,
        include_thinking: bool = True,
    ):
        """
        Initialize dataset.
        
        Args:
            examples: List of dicts with 'input', 'output', and optional 'thinking'
            tokenizer: HuggingFace tokenizer
            max_length: Max sequence length
            include_thinking: Whether to include <think> blocks
        """
        self.examples = examples
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.include_thinking = include_thinking
    
    def __len__(self):
        return len(self.examples)
    
    def __getitem__(self, idx):
        example = self.examples[idx]
        
        # Construct prompt with thinking blocks
        if self.include_thinking and "thinking" in example:
            prompt = f"{example['input']}\n<think>{example['thinking']}</think>\n"
        else:
            prompt = example['input'] + "\n"
        
        target = example['output']
        
        # Tokenize
        prompt_tokens = self.tokenizer(
            prompt,
            truncation=True,
            max_length=self.max_length // 2,
            return_tensors=None,
        )
        
        target_tokens = self.tokenizer(
            target,
            truncation=True,
            max_length=self.max_length // 2,
            return_tensors=None,
        )
        
        # Combine
        input_ids = prompt_tokens["input_ids"] + target_tokens["input_ids"]
        attention_mask = prompt_tokens["attention_mask"] + target_tokens["attention_mask"]
        
        # Pad to max_length
        pad_length = self.max_length - len(input_ids)
        if pad_length > 0:
            input_ids += [self.tokenizer.pad_token_id] * pad_length
            attention_mask += [0] * pad_length
        else:
            input_ids = input_ids[:self.max_length]
            attention_mask = attention_mask[:self.max_length]
        
        return {
            "input_ids": torch.tensor(input_ids, dtype=torch.long),
            "attention_mask": torch.tensor(attention_mask, dtype=torch.long),
            "example_id": idx,
            "ground_truth": example.get("output", ""),
        }


class GeneralKnowledgeDataset(Dataset):
    """Dataset for general knowledge (MMLU-style) tasks."""
    
    def __init__(
        self,
        examples: List[Dict[str, str]],
        tokenizer,
        max_length: int = 512,
    ):
        """
        Initialize dataset.
        
        Args:
            examples: List of dicts with 'question', 'answer', 'choices'
            tokenizer: HuggingFace tokenizer
            max_length: Max sequence length
        """
        self.examples = examples
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def __len__(self):
        return len(self.examples)
    
    def __getitem__(self, idx):
        example = self.examples[idx]
        
        # Format question with choices
        question = example['question']
        choices = example.get('choices', [])
        
        if choices:
            choices_text = "\n".join([f"{i+1}. {c}" for i, c in enumerate(choices)])
            prompt = f"{question}\n{choices_text}\n"
        else:
            prompt = question + "\n"
        
        target = example['answer']
        
        # Tokenize (same as logic dataset)
        prompt_tokens = self.tokenizer(
            prompt,
            truncation=True,
            max_length=self.max_length // 2,
            return_tensors=None,
        )
        
        target_tokens = self.tokenizer(
            target,
            truncation=True,
            max_length=self.max_length // 2,
            return_tensors=None,
        )
        
        input_ids = prompt_tokens["input_ids"] + target_tokens["input_ids"]
        attention_mask = prompt_tokens["attention_mask"] + target_tokens["attention_mask"]
        
        pad_length = self.max_length - len(input_ids)
        if pad_length > 0:
            input_ids += [self.tokenizer.pad_token_id] * pad_length
            attention_mask += [0] * pad_length
        else:
            input_ids = input_ids[:self.max_length]
            attention_mask = attention_mask[:self.max_length]
        
        return {
            "input_ids": torch.tensor(input_ids, dtype=torch.long),
            "attention_mask": torch.tensor(attention_mask, dtype=torch.long),
            "example_id": idx,
            "ground_truth": example.get("answer", ""),
        }


def load_jsonl(path: str) -> List[Dict]:
    """Load JSONL file."""
    data = []
    with open(path, 'r') as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))
    return data


def save_jsonl(data: List[Dict], path: str):
    """Save list of dicts to JSONL file."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        for item in data:
            f.write(json.dumps(item) + '\n')


def create_dataloaders(
    train_data: List[Dict],
    val_data: List[Dict],
    test_data: List[Dict],
    tokenizer,
    batch_size: int = 32,
    num_workers: int = 4,
    dataset_type: str = "logic",  # "logic" or "general_knowledge"
) -> Tuple[DataLoader, DataLoader, DataLoader]:
    """
    Create train/val/test dataloaders.
    
    Args:
        train_data: Training examples
        val_data: Validation examples
        test_data: Test examples
        tokenizer: HuggingFace tokenizer
        batch_size: Batch size
        num_workers: Number of workers for data loading
        dataset_type: Type of dataset ("logic" or "general_knowledge")
        
    Returns:
        Tuple of (train_loader, val_loader, test_loader)
    """
    if dataset_type == "logic":
        train_dataset = LogicPuzzleDataset(train_data, tokenizer)
        val_dataset = LogicPuzzleDataset(val_data, tokenizer)
        test_dataset = LogicPuzzleDataset(test_data, tokenizer)
    else:  # general_knowledge
        train_dataset = GeneralKnowledgeDataset(train_data, tokenizer)
        val_dataset = GeneralKnowledgeDataset(val_data, tokenizer)
        test_dataset = GeneralKnowledgeDataset(test_data, tokenizer)
    
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
    )
    
    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
    )
    
    test_loader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
    )
    
    return train_loader, val_loader, test_loader


def split_dataset(
    data: List[Dict],
    train_ratio: float = 0.8,
    val_ratio: float = 0.1,
    seed: int = 42,
) -> Tuple[List[Dict], List[Dict], List[Dict]]:
    """
    Split dataset into train/val/test.
    
    Args:
        data: Full dataset
        train_ratio: Training ratio
        val_ratio: Validation ratio (test = 1 - train - val)
        seed: Random seed
        
    Returns:
        Tuple of (train, val, test) datasets
    """
    import random
    random.seed(seed)
    torch.manual_seed(seed)
    
    shuffled = data.copy()
    random.shuffle(shuffled)
    
    train_size = int(len(shuffled) * train_ratio)
    val_size = int(len(shuffled) * val_ratio)
    
    train = shuffled[:train_size]
    val = shuffled[train_size:train_size + val_size]
    test = shuffled[train_size + val_size:]
    
    logger.info(f"Split: train={len(train)}, val={len(val)}, test={len(test)}")
    
    return train, val, test
