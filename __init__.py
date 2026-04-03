"""Recursive Logic Engine - Self-Correcting Reasoning Specialist"""

__version__ = "0.1.0"
__author__ = "ML Research Team"

from src.utils.config import load_all_configs
from src.utils.logging import setup_logging
from src.training.trainer import Trainer
from src.training.grpo import GRPOOptimizer
from src.data.loader import create_dataloaders, LogicPuzzleDataset
from src.eval.self_correction import SelfCorrectionAnalyzer, SelfCorrectionTrace

__all__ = [
    "load_all_configs",
    "setup_logging",
    "Trainer",
    "GRPOOptimizer",
    "create_dataloaders",
    "LogicPuzzleDataset",
    "SelfCorrectionAnalyzer",
    "SelfCorrectionTrace",
]
