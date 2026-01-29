import time
from core.exceptions import TransientError

class RetryConfig:
    def __init__(self, max_retries, initial_delay, backoff_factor):
        self.max_retries = max_retries
        self.initial_delay = initial_delay
        self.backoff_factor = backoff_factor

def retry(operation, config: RetryConfig, on_retry):
    delay = config.initial_delay

    for attempt in range(1, config.max_retries + 1):
        try:
            return operation()
        except TransientError as e:
            print(f"[RETRY] {e.service} attempt {attempt}")
            on_retry(e, attempt)
            if attempt == config.max_retries:
                raise
            time.sleep(delay)
            delay *= config.backoff_factor

