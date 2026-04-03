"""GRPO (Group Relative Policy Optimization) algorithm."""

import torch
import torch.nn.functional as F
from typing import Dict, Tuple, List
import logging


logger = logging.getLogger(__name__)


class GRPOOptimizer:
    """Group Relative Policy Optimization optimizer."""
    
    def __init__(
        self,
        model,
        optimizer,
        num_groups: int = 4,
        group_size: int = 8,
        kl_coeff: float = 0.05,
        reward_coeff: float = 1.0,
        entropy_coeff: float = 0.0,
        policy_clip_range: float = 0.2,
        device: str = "cuda" if torch.cuda.is_available() else "cpu",
    ):
        """
        Initialize GRPO optimizer.
        
        Args:
            model: Language model to optimize
            optimizer: PyTorch optimizer
            num_groups: Number of groups for GRPO
            group_size: Size of each group
            kl_coeff: KL divergence penalty coefficient
            reward_coeff: Reward coefficient
            entropy_coeff: Entropy bonus coefficient
            policy_clip_range: PPO clipping range
            device: Device for computation
        """
        self.model = model
        self.optimizer = optimizer
        self.num_groups = num_groups
        self.group_size = group_size
        self.kl_coeff = kl_coeff
        self.reward_coeff = reward_coeff
        self.entropy_coeff = entropy_coeff
        self.policy_clip_range = policy_clip_range
        self.device = device
    
    def compute_group_relative_advantage(
        self,
        rewards: torch.Tensor,  # [batch_size]
    ) -> torch.Tensor:
        """
        Compute group relative advantages.
        
        For each group, compute advantage relative to group mean.
        This reduces variance in policy gradients.
        
        Args:
            rewards: Rewards for all examples
            
        Returns:
            Group-relative advantages [batch_size]
        """
        batch_size = rewards.shape[0]
        advantages = torch.zeros_like(rewards)
        
        for i in range(self.num_groups):
            start_idx = i * self.group_size
            end_idx = min((i + 1) * self.group_size, batch_size)
            
            group_rewards = rewards[start_idx:end_idx]
            group_mean = group_rewards.mean()
            group_std = group_rewards.std() + 1e-8
            
            # Normalize advantages within group
            advantages[start_idx:end_idx] = (group_rewards - group_mean) / group_std
        
        return advantages
    
    def compute_policy_loss(
        self,
        log_probs: torch.Tensor,  # [batch_size, seq_len]
        old_log_probs: torch.Tensor,  # [batch_size, seq_len]
        advantages: torch.Tensor,  # [batch_size]
        attention_mask: torch.Tensor = None,
    ) -> torch.Tensor:
        """
        Compute PPO-style policy loss with clipping.
        
        Args:
            log_probs: Log probabilities from current policy
            old_log_probs: Log probabilities from old policy
            advantages: Computed advantages
            attention_mask: Attention mask (for sequences)
            
        Returns:
            Policy loss scalar
        """
        # Probability ratio
        ratio = torch.exp(log_probs - old_log_probs)
        
        # Clipped objective
        surr1 = ratio * advantages.unsqueeze(-1)
        surr2 = torch.clamp(
            ratio,
            1 - self.policy_clip_range,
            1 + self.policy_clip_range,
        ) * advantages.unsqueeze(-1)
        
        loss = -torch.min(surr1, surr2)
        
        # Apply attention mask
        if attention_mask is not None:
            loss = loss * attention_mask.unsqueeze(-1)
            loss = loss.sum() / attention_mask.sum().clamp(min=1)
        else:
            loss = loss.mean()
        
        return loss
    
    def compute_kl_penalty(
        self,
        log_probs: torch.Tensor,
        old_log_probs: torch.Tensor,
        attention_mask: torch.Tensor = None,
    ) -> torch.Tensor:
        """
        Compute KL divergence penalty to prevent diverging from reference policy.
        
        Args:
            log_probs: Log probs from current policy
            old_log_probs: Log probs from reference policy
            attention_mask: Attention mask
            
        Returns:
            KL divergence penalty
        """
        kl_div = old_log_probs - log_probs  # Reverse KL
        
        if attention_mask is not None:
            kl_div = kl_div * attention_mask.unsqueeze(-1)
            kl_div = kl_div.sum() / attention_mask.sum().clamp(min=1)
        else:
            kl_div = kl_div.mean()
        
        return kl_div
    
    def compute_entropy_bonus(
        self,
        log_probs: torch.Tensor,
        attention_mask: torch.Tensor = None,
    ) -> torch.Tensor:
        """
        Compute entropy bonus to encourage exploration.
        
        Args:
            log_probs: Log probabilities
            attention_mask: Attention mask
            
        Returns:
            Entropy bonus
        """
        probs = torch.exp(log_probs)
        entropy = -(probs * log_probs).sum(dim=-1)
        
        if attention_mask is not None:
            entropy = entropy * attention_mask.squeeze(-1)
            entropy = entropy.sum() / attention_mask.sum().clamp(min=1)
        else:
            entropy = entropy.mean()
        
        return entropy
    
    def compute_total_loss(
        self,
        log_probs: torch.Tensor,
        old_log_probs: torch.Tensor,
        advantages: torch.Tensor,
        attention_mask: torch.Tensor = None,
    ) -> Tuple[torch.Tensor, Dict[str, float]]:
        """
        Compute total GRPO loss.
        
        Total Loss = policy_loss + kl_penalty - entropy_bonus
        
        Args:
            log_probs: Log probs from current policy
            old_log_probs: Log probs from reference policy
            advantages: Advantages
            attention_mask: Attention mask
            
        Returns:
            Tuple of (total_loss, loss_components_dict)
        """
        policy_loss = self.compute_policy_loss(
            log_probs, old_log_probs, advantages, attention_mask
        )
        
        kl_penalty = self.compute_kl_penalty(log_probs, old_log_probs, attention_mask)
        kl_loss = self.kl_coeff * kl_penalty
        
        entropy_bonus = self.compute_entropy_bonus(log_probs, attention_mask)
        entropy_loss = -self.entropy_coeff * entropy_bonus
        
        total_loss = policy_loss + kl_loss + entropy_loss
        
        return total_loss, {
            "policy_loss": policy_loss.item(),
            "kl_loss": kl_loss.item(),
            "entropy_loss": entropy_loss.item(),
            "total_loss": total_loss.item(),
        }
    
    def step(
        self,
        rewards: torch.Tensor,
        log_probs: torch.Tensor,
        old_log_probs: torch.Tensor,
        attention_mask: torch.Tensor = None,
    ) -> Dict[str, float]:
        """
        Perform one GRPO optimization step.
        
        Args:
            rewards: Rewards for examples
            log_probs: Log probs from current policy
            old_log_probs: Log probs from reference policy
            attention_mask: Attention mask
            
        Returns:
            Loss components dict
        """
        # Compute advantages
        advantages = self.compute_group_relative_advantage(rewards)
        
        # Compute loss
        loss, loss_components = self.compute_total_loss(
            log_probs, old_log_probs, advantages, attention_mask
        )
        
        # Backward pass
        self.optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
        self.optimizer.step()
        
        return loss_components


def grpo_step(
    model,
    batch: Dict[str, torch.Tensor],
    rewards: torch.Tensor,
    reference_model,
    optimizer,
    grpo_config: Dict,
    device: str = "cuda" if torch.cuda.is_available() else "cpu",
) -> Dict[str, float]:
    """
    Single GRPO training step.
    
    Args:
        model: Model to optimize
        batch: Training batch with input_ids, attention_mask
        rewards: Computed rewards for batch
        reference_model: Reference policy (frozen)
        optimizer: PyTorch optimizer
        grpo_config: GRPO hyperparameters
        device: Device
        
    Returns:
        Loss components dict
    """
    # Get log probs from current model
    with torch.no_grad():
        model_output = model(
            input_ids=batch["input_ids"].to(device),
            attention_mask=batch["attention_mask"].to(device),
        )
        current_logits = model_output.logits
        
        # Get log probs from reference model (frozen)
        ref_output = reference_model(
            input_ids=batch["input_ids"].to(device),
            attention_mask=batch["attention_mask"].to(device),
        )
        ref_logits = ref_output.logits
    
    # Compute log probs (simplified: take argmax for now)
    current_log_probs = F.log_softmax(current_logits, dim=-1)
    ref_log_probs = F.log_softmax(ref_logits, dim=-1)
    
    # Create GRPO optimizer
    grpo_opt = GRPOOptimizer(
        model=model,
        optimizer=optimizer,
        num_groups=grpo_config.get("num_groups", 4),
        group_size=grpo_config.get("group_size", 8),
        kl_coeff=grpo_config.get("kl_coeff", 0.05),
        reward_coeff=grpo_config.get("reward_coeff", 1.0),
        device=device,
    )
    
    # Perform GRPO step
    loss_components = grpo_opt.step(
        rewards=rewards.to(device),
        log_probs=current_log_probs.mean(dim=-1),  # Average over vocab
        old_log_probs=ref_log_probs.mean(dim=-1),
        attention_mask=batch["attention_mask"].to(device),
    )
    
    return loss_components
