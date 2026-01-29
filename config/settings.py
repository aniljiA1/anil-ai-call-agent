RETRY_CONFIG = {
    "max_retries": 3,
    "initial_delay": 5,
    "backoff_factor": 2
}

CIRCUIT_BREAKER_CONFIG = {
    "failure_threshold": 3,
    "recovery_timeout": 30
}

HEALTH_CHECK_INTERVAL = 10  # seconds
