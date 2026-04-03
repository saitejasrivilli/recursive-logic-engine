"""Structured logging utilities."""

import logging
import sys
from pathlib import Path
from typing import Optional
import json
from datetime import datetime


class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging."""
    
    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "message": record.getMessage(),
        }
        
        # Add any extra fields
        if hasattr(record, "extra_data"):
            log_data.update(record.extra_data)
        
        return json.dumps(log_data)


def setup_logging(
    log_file: Optional[str] = None,
    level: str = "INFO",
    name: str = "recursive_logic"
) -> logging.Logger:
    """
    Set up structured logging with console and optional file output.
    
    Args:
        log_file: Optional path to log file
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        name: Logger name
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level))
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, level))
    console_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(getattr(logging, level))
        file_formatter = JSONFormatter()
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger


def log_metrics(logger: logging.Logger, metrics: dict, step: int = None):
    """Log metrics in structured format."""
    log_msg = f"Step {step}: " if step else ""
    log_msg += " | ".join([f"{k}={v:.4f}" if isinstance(v, float) else f"{k}={v}" 
                           for k, v in metrics.items()])
    logger.info(log_msg)


def log_hyperparams(logger: logging.Logger, config: dict):
    """Log hyperparameters at training start."""
    logger.info("=" * 80)
    logger.info("TRAINING CONFIGURATION")
    logger.info("=" * 80)
    
    def log_dict(d, prefix=""):
        for key, value in d.items():
            if isinstance(value, dict):
                log_dict(value, prefix=f"{prefix}{key}.")
            else:
                logger.info(f"{prefix}{key}: {value}")
    
    log_dict(config)
    logger.info("=" * 80)
