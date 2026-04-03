"""Configuration management utilities."""

import os
import yaml
from pathlib import Path
from typing import Dict, Any
from dataclasses import dataclass


CONFIG_DIR = Path(__file__).parent.parent / "config"


@dataclass
class ModelConfig:
    name: str
    model_size: str
    pretrained: bool
    dtype: str
    device: str


@dataclass
class TrainingConfig:
    num_epochs: int
    batch_size: int
    gradient_accumulation_steps: int
    learning_rate: float
    warmup_steps: int
    max_steps: int
    eval_every: int
    save_every: int
    log_every: int


@dataclass
class GRPOConfig:
    num_groups: int
    group_size: int
    kl_coeff: float
    reward_coeff: float
    entropy_coeff: float
    policy_clip_range: float


@dataclass
class RLVRConfig:
    loss_velocity_coeff: float
    reward_velocity_coeff: float
    velocity_window: int


def load_yaml(path: str) -> Dict[str, Any]:
    """Load YAML config file."""
    with open(path, "r") as f:
        return yaml.safe_load(f)


def merge_configs(*configs: Dict[str, Any]) -> Dict[str, Any]:
    """Deep merge multiple config dicts (later configs override earlier)."""
    merged = {}
    for config in configs:
        for key, value in config.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = {**merged[key], **value}
            else:
                merged[key] = value
    return merged


def load_all_configs(override_path: str = None) -> Dict[str, Any]:
    """
    Load all default configs and optionally merge with override.
    
    Args:
        override_path: Optional path to override config YAML
        
    Returns:
        Merged configuration dict
    """
    configs = []
    
    # Load defaults
    for config_file in ["train.yaml", "data.yaml"]:
        config_path = CONFIG_DIR / config_file
        if config_path.exists():
            configs.append(load_yaml(str(config_path)))
    
    # Load override if provided
    if override_path and os.path.exists(override_path):
        configs.append(load_yaml(override_path))
    
    return merge_configs(*configs)


def get_config_value(config: Dict[str, Any], path: str, default: Any = None) -> Any:
    """
    Get nested config value using dot notation.
    
    Example:
        get_config_value(config, "training.learning_rate", 5e-6)
    """
    keys = path.split(".")
    value = config
    
    for key in keys:
        if isinstance(value, dict):
            value = value.get(key)
        else:
            return default
    
    return value if value is not None else default
