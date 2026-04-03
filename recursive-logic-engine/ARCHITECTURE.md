<!-- ARCHITECTURE.md -->
# Recursive Logic Engine - Architecture & Design Patterns

## System Design Philosophy

This project follows **enterprise ML systems design** patterns used at companies like Anthropic, OpenAI, Deepmind, and Google Brain:

1. **Modular Components**: Each responsibility is isolated (data, training, eval, utils)
2. **Configuration-Driven**: Hyperparameters in YAML, not hardcoded
3. **Structured Logging**: JSON logs for easy parsing and monitoring
4. **Checkpoint Management**: Track best models, save intermediate checkpoints
5. **Metric Tracking**: W&B integration for experiment management
6. **Clean Interfaces**: Well-defined APIs between components

## Component Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    TRAINING LOOP                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Trainer (src/training/trainer.py)                              │
│  ├── Loads model & reference model                              │
│  ├── Iterates over batches                                      │
│  ├── Calls GRPO step                                            │
│  ├── Computes RLVR penalty                                      │
│  ├── Monitors stability                                         │
│  ├── Logs to W&B & files                                        │
│  └── Saves checkpoints                                          │
│                                                                  │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐  │
│  │   Data Loader    │  │  GRPO Optimizer  │  │ Reward Fn    │  │
│  │                  │  │                  │  │              │  │
│  │ • Logic puzzles  │  │ • Group relative │  │ • Exact      │  │
│  │ • Gen. knowledge │  │   advantages     │  │   match      │  │
│  │ • Preprocessing  │  │ • Policy clipping│  │ • F1 score   │  │
│  │ • Quality filter │  │ • KL penalty     │  │ • Similarity │  │
│  └──────────────────┘  └──────────────────┘  └──────────────┘  │
│                                                                  │
│  ┌──────────────────┐  ┌──────────────────┐                     │
│  │ RLVR Loss        │  │  Stability Monit.│                     │
│  │                  │  │                  │                     │
│  │ • Loss velocity  │  │ • Spike detection│                     │
│  │ • Reward velocity│  │ • Warnings       │                     │
│  │ • Penalty        │  │ • Safeguards     │                     │
│  └──────────────────┘  └──────────────────┘                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│              EVALUATION & ANALYSIS                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Self-Correction Analyzer (src/eval/self_correction.py)         │
│  ├── Extract <think> blocks                                     │
│  ├── Detect correction patterns                                 │
│  ├── Generate traces                                            │
│  └── Analyze effectiveness                                      │
│                                                                  │
│  Catastrophic Forgetting Evaluator                              │
│  ├── Run on MMLU-style tasks                                    │
│  ├── Compare vs baseline                                        │
│  ├── Alert if >5% drop                                          │
│  └── Log to W&B                                                 │
│                                                                  │
│  Logic Puzzle Evaluator                                         │
│  ├── Benchmark on logic tasks                                   │
│  ├── Accuracy metrics                                           │
│  ├── Reasoning quality                                          │
│  └── Self-correction rate                                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│           CONFIGURATION & UTILITIES                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Config Management (src/utils/config.py)                        │
│  ├── Load YAML configs                                          │
│  ├── Merge configs (defaults + overrides)                       │
│  ├── Get nested values via dot notation                         │
│  └── Type-safe access                                           │
│                                                                  │
│  Logging (src/utils/logging.py)                                 │
│  ├── Structured JSON logs                                       │
│  ├── Console + file output                                      │
│  ├── Metric logging helpers                                     │
│  └── Hyperparameter logging                                     │
│                                                                  │
│  W&B Integration (src/utils/wandb_integration.py)               │
│  ├── Experiment tracking                                        │
│  ├── Metric logging                                             │
│  ├── Model checkpointing                                        │
│  ├── Comparison tables                                          │
│  └── Trace visualization                                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

```
Raw Data (40k puzzles)
         ↓
    Quality Filter (Scorer Model: GPT2-small)
         ↓
   Filtered Data (10k high-signal examples)
         ↓
   Train/Val/Test Split (80/10/10)
         ↓
   Tokenization & Preprocessing
         ↓
   DataLoader (batch_size=32)
         ↓
   ┌─────────────────────────────────────┐
   │     Training Loop (per batch)        │
   ├─────────────────────────────────────┤
   │                                     │
   │ 1. Forward pass (model + ref)       │
   │ 2. Decode predictions               │
   │ 3. Compute rewards                  │
   │ 4. GRPO advantage computation       │
   │ 5. Policy loss + KL penalty         │
   │ 6. RLVR velocity penalty            │
   │ 7. Backward pass                    │
   │ 8. Optimizer step                   │
   │ 9. Log metrics                      │
   │ 10. Stability check                 │
   │                                     │
   └─────────────────────────────────────┘
         ↓
   Validation (every N steps)
         ↓
   Save best model
```

## Key Algorithms

### GRPO (Group Relative Policy Optimization)

```python
# Reduce variance via group-relative advantages
for group in groups:
    group_rewards = rewards[group]
    mean = group_rewards.mean()
    std = group_rewards.std()
    advantages[group] = (group_rewards - mean) / std

# PPO-style update with clipping
ratio = exp(log_probs - old_log_probs)
policy_loss = -min(
    ratio * advantages,
    clip(ratio, 1-ε, 1+ε) * advantages
)

# Total loss with KL penalty
total_loss = policy_loss + β * KL(π || π_ref)
```

### RLVR (Reward and Loss Velocity Regularization)

```python
# Track metric changes over time
loss_velocity = mean(|loss_t - loss_{t-1}| for t in window)
reward_velocity = mean(|reward_t - reward_{t-1}| for t in window)

# Penalize high velocity (training instability)
velocity_penalty = α * loss_velocity + γ * reward_velocity

# Add to total loss
total_loss += velocity_penalty
```

### Quality Filter

```python
# Score each example using fast scorer model
scores = []
for example in data:
    hidden = scorer(example.input).hidden_states[-1]
    score = mean(abs(hidden))  # Magnitude as signal quality proxy
    scores.append(score)

# Keep top-k or top-percentile
keep_indices = argsort(scores)[-top_k:]
filtered_data = data[keep_indices]
```

## Configuration Hierarchy

```
config/
├── train.yaml (primary)
├── data.yaml
└── [override.yaml] (optional)
        ↓
    (merge with: later overrides earlier)
        ↓
    Final config dict
```

**Config merging is deep**: nested dicts are merged, not replaced.

Example:
```yaml
# train.yaml
training:
  lr: 5e-6
  batch_size: 32

# override.yaml
training:
  batch_size: 64  # overrides
  # lr: 5e-6 preserved
```

Result: `lr=5e-6, batch_size=64`

## Checkpoint System

```
outputs/
├── checkpoints/
│   ├── best_model.pt          ← Best validation accuracy
│   ├── checkpoint_step_1000.pt
│   ├── checkpoint_step_2000.pt
│   └── checkpoint_step_3000.pt ← Latest
└── training.log
```

Each checkpoint contains:
```python
{
    "model_state_dict": ...,
    "optimizer_state_dict": ...,
    "global_step": ...,
    "best_val_accuracy": ...,
    "config": {...}
}
```

## Production Considerations

### Scaling to Larger Models

```python
# From 1.5B to 3B+
model = GPT2LMHeadModel.from_pretrained("gpt-neox-3b")
# Enable gradient checkpointing
model.gradient_checkpointing_enable()
# Use mixed precision training
with autocast():
    loss.backward()
# Use distributed training
model = DDP(model, device_ids=[0,1,2,3])
```

### Distributed Training

```python
# Setup (uses FSDP for model parallelism)
from torch.distributed.fsdp import FullyShardedDataParallel as FSDP

model = FSDP(model, auto_wrap_policy=...)
```

### Inference Optimization

```python
# Quantization
model = torch.quantization.quantize_dynamic(model, qconfig_spec=...)

# KV-cache for faster generation
# Beam search instead of greedy
# Batch inference
```

### Continuous Evaluation

```
├── Hourly eval on test set
├── Daily comparison vs baseline
├── Weekly catastrophic forgetting check
└── Monthly model versioning
```

## Testing Strategy

```
tests/
├── test_data.py           # Data loading/preprocessing
├── test_model.py          # Model initialization
├── test_training.py       # GRPO/RLVR components
└── test_eval.py           # Evaluation metrics

Run: pytest tests/ -v
```

## Monitoring & Observability

### Metrics Tracked

| Metric | Category | Alert Threshold |
|--------|----------|-----------------|
| `train/reward` | Quality | < -1.0 |
| `train/kl_divergence` | Stability | > 10.0 |
| `train/loss_velocity` | Stability | > 1.0 |
| `val/accuracy` | Performance | < baseline-5% |
| `general_knowledge_acc` | Forgetting | < 40% |

### Logging Format

```json
{
  "timestamp": "2025-04-02T10:30:45",
  "level": "INFO",
  "module": "trainer",
  "message": "Step 1000: reward=0.78, kl_div=0.05",
  "step": 1000,
  "reward": 0.78,
  "kl_divergence": 0.05
}
```

## Extension Points

### Adding New Reward Functions

```python
class CustomRewardComputer(RewardComputer):
    def compute_custom_reward(self, pred, target):
        # Custom logic
        return score
```

### Adding New Datasets

```python
class CustomDataset(Dataset):
    def __getitem__(self, idx):
        # Custom format
        return {"input_ids": ..., "attention_mask": ...}
```

### Adding New Evaluation Metrics

```python
class CustomEvaluator:
    def evaluate(self, model, loader):
        # Custom evaluation
        return {"custom_metric": value}
```

## References & Best Practices

1. **Config Management**: Inspired by MLflow, Hydra
2. **Training Loop**: Based on HuggingFace Trainer patterns
3. **GRPO**: Implementation of "Group Relative Policy Optimization"
4. **RLVR**: Preventing reward hacking via velocity regularization
5. **Logging**: Structured logging best practices (ELK stack compatible)

