import json
import os

def log_input(data, config):
    log_file = config["log_file"]
    flagged_log_file = config.get("flagged_log_file", "/app/logs/flagged_hate_speech.jsonl")
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    # Write to flagged log if flagged=True, else regular log
    target_file = flagged_log_file if data.get("flagged") else log_file
    with open(target_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")
