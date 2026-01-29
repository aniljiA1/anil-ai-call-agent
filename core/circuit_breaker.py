import time
from enum import Enum

class CircuitState(Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"


class CircuitBreaker:
    def __init__(self, failure_threshold, recovery_timeout):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failures = 0
        self.state = CircuitState.CLOSED
        self.last_failure_time = None

    def allow_request(self):
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
                print("[CIRCUIT] HALF_OPEN")
                return True
            return False
        return True

    def record_success(self):
        if self.state != CircuitState.CLOSED:
            print("[CIRCUIT] CLOSED")
        self.failures = 0
        self.state = CircuitState.CLOSED

    def record_failure(self):
        self.failures += 1
        self.last_failure_time = time.time()

        if self.failures >= self.failure_threshold:
            if self.state != CircuitState.OPEN:
                print("[CIRCUIT] OPEN")
            self.state = CircuitState.OPEN
