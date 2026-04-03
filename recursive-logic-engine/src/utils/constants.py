"""Global constants and enums."""

from enum import Enum
from typing import List

# Model sizes and their typical parameter counts
MODEL_SIZES = {
    "1.5B": 1.5e9,
    "3B": 3e9,
    "7B": 7e9,
    "13B": 13e9,
}

# Special tokens for reasoning
THINKING_START_TOKEN = "<think>"
THINKING_END_TOKEN = "</think>"
SPECIAL_TOKENS = [THINKING_START_TOKEN, THINKING_END_TOKEN]

# Dataset splits
TRAIN_SPLIT = 0.8
VAL_SPLIT = 0.1
TEST_SPLIT = 0.1

# Timeout for model inference
INFERENCE_TIMEOUT = 30  # seconds

# Quality filter thresholds
QUALITY_FILTER_PERCENTILE = 0.25  # Keep top 25%

# Catastrophic forgetting thresholds
FORGETTING_THRESHOLD = 0.05  # 5% drop triggers alert
MIN_GENERAL_KNOWLEDGE_ACCURACY = 0.40  # Minimum acceptable accuracy

# Training stability constants
MAX_REWARD_VALUE = 1.0
MIN_REWARD_VALUE = -1.0
MAX_KL_VALUE = 10.0

# Evaluation constants
EVAL_LOGIC_SAMPLES = 2000
EVAL_GENERAL_KNOWLEDGE_SAMPLES = 1000
EVAL_SELF_CORRECTION_SAMPLES = 500

# GRPO algorithm constants
DEFAULT_NUM_GROUPS = 4
DEFAULT_GROUP_SIZE = 8
DEFAULT_KL_COEFF = 0.05
DEFAULT_REWARD_COEFF = 1.0

# RLVR (Reward and Loss Velocity Regularization) constants
DEFAULT_LOSS_VELOCITY_COEFF = 0.01
DEFAULT_REWARD_VELOCITY_COEFF = 0.01
VELOCITY_WINDOW = 10  # steps for computing velocity

# Checkpointing
BEST_MODEL_NAME = "best_model"
LAST_MODEL_NAME = "last_model"
CHECKPOINT_SUFFIX = ".pt"

# Batch size recommendations
RECOMMENDED_BATCH_SIZES = {
    "1.5B": 32,
    "3B": 16,
    "7B": 8,
}

# Learning rate recommendations (scaled by batch size / 32)
BASE_LEARNING_RATE = 5e-6
LR_SCALES = {
    "1.5B": 1.0,
    "3B": 0.5,
    "7B": 0.25,
}


class LogicPuzzleType(Enum):
    """Types of logic puzzles in training dataset."""
    SYMBOLIC_REASONING = "symbolic"
    CODE_DEBUGGING = "code_debug"
    SCHEDULE_OPTIMIZATION = "schedule"
    ARITHMETIC = "arithmetic"
    LOGIC_GATES = "gates"
    CONSTRAINT_SATISFACTION = "constraint"


class DataSource(Enum):
    """Data sources for training."""
    LOCAL = "local"
    HUGGINGFACE = "huggingface"
    API = "api"


class EvalMetric(Enum):
    """Evaluation metrics."""
    ACCURACY = "accuracy"
    F1 = "f1"
    EXACT_MATCH = "em"
    REASONING_CORRECTNESS = "reasoning_correct"
    SELF_CORRECTION_RATE = "self_correction_rate"
