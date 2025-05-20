import phj
from pathlib import Path
import json
import sys

mod_folder = sys.argv[1]
mod_path = Path(mod_folder)

for file in mod_path.rglob("*.phj"):
    with open(file, "r") as f:
        content = f.read()

    data = phj.loads(content)
    json_file = file.with_suffix(".json")

    with open(json_file, "w") as f:
        if isinstance(data, dict):
            json.dump(data, f, indent=4)
        else:
            f.write(data)
