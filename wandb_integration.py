"""Weights & Biases experiment tracking integration."""

import wandb
from typing import Dict, Optional, List, Any
import os


class WandBTracker:
    """Wrapper for W&B experiment tracking."""
    
    def __init__(
        self,
        project: str,
        entity: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
        notes: Optional[str] = None,
        mode: str = "online",  # "online", "offline", "disabled"
    ):
        """
        Initialize W&B tracker.
        
        Args:
            project: W&B project name
            entity: W&B team/entity (optional)
            config: Hyperparameters dict to log
            tags: List of tags for the run
            notes: Run description
            mode: W&B mode (online/offline/disabled)
        """
        self.project = project
        self.entity = entity or os.getenv("WANDB_ENTITY")
        self.mode = mode if mode != "null" else "disabled"
        
        # Initialize W&B run
        wandb.init(
            project=project,
            entity=self.entity,
            config=config,
            tags=tags or [],
            notes=notes or "",
            mode=self.mode,
        )
    
    def log_metrics(self, metrics: Dict[str, float], step: int = None):
        """Log metrics to W&B."""
        if self.mode == "disabled":
            return
        
        log_dict = metrics.copy()
        if step is not None:
            wandb.log(log_dict, step=step)
        else:
            wandb.log(log_dict)
    
    def log_training_curve(
        self,
        step: int,
        reward: float,
        kl_div: float,
        loss: float,
        accuracy: float,
        learning_rate: float,
    ):
        """Log main training metrics."""
        self.log_metrics({
            "train/reward": reward,
            "train/kl_divergence": kl_div,
            "train/loss": loss,
            "train/accuracy": accuracy,
            "train/learning_rate": learning_rate,
        }, step=step)
    
    def log_validation(self, step: int, metrics: Dict[str, float]):
        """Log validation metrics."""
        val_metrics = {f"val/{k}": v for k, v in metrics.items()}
        self.log_metrics(val_metrics, step=step)
    
    def log_catastrophic_forgetting(
        self,
        step: int,
        logic_accuracy: float,
        general_knowledge_accuracy: float,
        delta: float,
    ):
        """Log catastrophic forgetting metrics."""
        self.log_metrics({
            "eval/logic_accuracy": logic_accuracy,
            "eval/general_knowledge_accuracy": general_knowledge_accuracy,
            "eval/forgetting_delta": delta,
        }, step=step)
    
    def log_self_correction_trace(self, trace: Dict[str, Any]):
        """Log a self-correction trace."""
        if self.mode == "disabled":
            return
        
        # Create a formatted trace string
        trace_str = f"""
        INPUT: {trace['input']}
        INITIAL_THINK: {trace['initial_think']}
        CORRECTION: {trace.get('correction', 'N/A')}
        FINAL_THINK: {trace.get('final_think', 'N/A')}
        OUTPUT: {trace['output']}
        CORRECT: {trace.get('is_correct', 'Unknown')}
        """
        
        wandb.log({"self_correction_traces": wandb.Html(f"<pre>{trace_str}</pre>")})
    
    def log_model_comparison(
        self,
        comparisons: List[Dict[str, Any]],
    ):
        """Log model comparison table."""
        if self.mode == "disabled":
            return
        
        table_data = [
            [c["model"], c["logic_acc"], c["general_acc"], c["speed"]]
            for c in comparisons
        ]
        
        table = wandb.Table(
            data=table_data,
            columns=["Model", "Logic Accuracy", "General Knowledge", "Speed (ms)"]
        )
        wandb.log({"model_comparison": table})
    
    def log_hyperparams(self, config: Dict[str, Any]):
        """Log hyperparameters."""
        wandb.config.update(config)
    
    def save_checkpoint(self, path: str, name: str = "model"):
        """Save model checkpoint to W&B."""
        if self.mode == "disabled":
            return
        
        artifact = wandb.Artifact(name, type="model")
        artifact.add_file(path)
        wandb.log_artifact(artifact)
    
    def finish(self):
        """Finish W&B run."""
        if self.mode != "disabled":
            wandb.finish()


def create_wandb_tracker(config: Dict[str, Any]) -> WandBTracker:
    """Factory function to create W&B tracker from config."""
    wandb_config = config.get("wandb", {})
    
    return WandBTracker(
        project=wandb_config.get("project", "recursive-logic-engine"),
        entity=wandb_config.get("entity"),
        tags=wandb_config.get("tags", []),
        notes=wandb_config.get("notes", ""),
        mode=wandb_config.get("mode", "online"),
    )
