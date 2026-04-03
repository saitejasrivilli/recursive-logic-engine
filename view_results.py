import json
import glob

for file in sorted(glob.glob("outputs/*.json")):
    print(f"\n{'='*80}")
    print(f"FILE: {file}")
    print('='*80)
    with open(file) as f:
        data = json.load(f)
        print(json.dumps(data, indent=2))

