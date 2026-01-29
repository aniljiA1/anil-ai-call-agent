from core.retry import retry, RetryConfig
from core.exceptions import TransientError
from services.elevenlabs import generate_audio, cb_elevenlabs
from observability.logger import log_event
from alerts.email_alert import send_email
from alerts.telegram_alert import send_telegram
from alerts.webhook_alert import send_webhook
from config.settings import RETRY_CONFIG

def process_call(contact):
    try:
        retry(
            lambda: generate_audio("Hello"),
            RetryConfig(**RETRY_CONFIG),
            lambda e, r: log_event(
                e.service,
                "Transient",
                str(e),
                r,
                cb_elevenlabs.state.value
            )
        )
        print(f"Call succeeded for {contact}")

    except TransientError:
        send_email("Call Failed", contact)
        send_telegram(f"Call failed for {contact}")
        send_webhook({"contact": contact, "status": "failed"})
        print(f"Skipping {contact}")
