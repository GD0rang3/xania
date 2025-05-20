import phj
import sys
import os
import json

input_path = sys.argv[1] if len(sys.argv) > 1 else "example.phj"

with open(input_path, "r", encoding="utf-8") as f:
    content = f.read()

data = phj.loads(content)

output_path = os.path.splitext(input_path)[0] + ".json"

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Written to {output_path}")
