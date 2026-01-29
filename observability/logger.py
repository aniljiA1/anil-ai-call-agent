import json
from datetime import datetime

def log_event(service, error_type, message, retries, circuit_state):
    log = {
        "timestamp": datetime.utcnow().isoformat(),
        "service": service,
        "error_type": error_type,
        "message": message,
        "retries": retries,
        "circuit_state": circuit_state
    }

    with open("logs.jsonl", "a") as f:
        f.write(json.dumps(log) + "\n")
