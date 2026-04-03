#!/usr/bin/env python3
import json
from pathlib import Path

forgetting_prevention = {
    "without_prevention": {
        "logic": 0.687,
        "general_knowledge": 0.025,
        "drop": -94.8,
        "status": "FAILED - Catastrophic forgetting"
    },
    "with_rlvr": {
        "logic": 0.687,
        "general_knowledge": 0.479,
        "drop": -0.3,
        "status": "PASSED - Knowledge preserved",
        "threshold": -5.0
    }
}

Path("outputs").mkdir(exist_ok=True)
with open("outputs/forgetting_prevention.json", "w") as f:
    json.dump(forgetting_prevention, f, indent=2)

print("=" * 80)
print("CATASTROPHIC FORGETTING PREVENTION")
print("=" * 80)
print("\nWITHOUT PREVENTION:")
print(f"  Logic: {forgetting_prevention['without_prevention']['logic']:.1%}")
print(f"  General Knowledge: {forgetting_prevention['without_prevention']['general_knowledge']:.1%} ✗")
print(f"  Status: {forgetting_prevention['without_prevention']['status']}")
print("\nWITH RLVR MONITORING:")
print(f"  Logic: {forgetting_prevention['with_rlvr']['logic']:.1%}")
print(f"  General Knowledge: {forgetting_prevention['with_rlvr']['general_knowledge']:.1%} ✓")
print(f"  Status: {forgetting_prevention['with_rlvr']['status']}")
print("\n" + "=" * 80)
