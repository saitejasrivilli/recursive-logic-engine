#!/usr/bin/env python3
import sys
import os

# Add current directory to path
sys.path.insert(0, os.getcwd())

from src.training.trainer import Trainer
from src.utils.config import load_config

# Load config
config = load_config('config/train.yaml')

# Create trainer
trainer = Trainer(config)

# Train
print("Starting training...")
trainer.train()

print("Training complete!")
print(f"Model saved to: outputs/checkpoints/best_model.pt")
