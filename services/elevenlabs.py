import requests
from core.exceptions import TransientError
from core.circuit_breaker import CircuitBreaker
from config.settings import CIRCUIT_BREAKER_CONFIG

cb_elevenlabs = CircuitBreaker(**CIRCUIT_BREAKER_CONFIG)

def generate_audio(text):
    if not cb_elevenlabs.allow_request():
        raise TransientError("Circuit breaker open", "ElevenLabs")

    try:
        # HTTP (not HTTPS) to avoid SSL issues
        response = requests.post("http://httpstat.us/503", timeout=3)

        if response.status_code == 503:
            cb_elevenlabs.record_failure()
            raise TransientError("503 Service Unavailable", "ElevenLabs")

    except requests.exceptions.RequestException as e:
        # 🔥 THIS IS THE KEY FIX
        cb_elevenlabs.record_failure()
        raise TransientError(f"Network/SSL failure: {e}", "ElevenLabs")

    cb_elevenlabs.record_success()
    return "audio-bytes"
