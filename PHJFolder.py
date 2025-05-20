import os
import json
import phj  # your custom PHJ parser module

def convert_phj_to_json(phj_file_path):
    try:
        with open(phj_file_path, "r", encoding="utf-8") as f:
            content = f.read()
        data = phj.loads(content)
    except Exception as e:
        print(f"[ERROR] Failed to parse {phj_file_path}: {e}")
        return

    json_path = os.path.splitext(phj_file_path)[0] + ".json"
    try:
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"[OK] Converted: {phj_file_path} -> {json_path}")
    except Exception as e:
        print(f"[ERROR] Failed to write JSON file {json_path}: {e}")

def process_folder(folder_path):
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".phj"):
                full_path = os.path.join(root, file)
                convert_phj_to_json(full_path)

if __name__ == "__main__":
    import sys

    folder = sys.argv[1] if len(sys.argv) > 1 else "."
    print(f"Scanning folder: {folder}")
    process_folder(folder)
