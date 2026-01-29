📞 AI Call Agent – Resilient Call Processing System
📌 Overview

This project implements a fault-tolerant AI Call Agent designed to simulate outbound call processing using an external AI voice service (ElevenLabs-style), with robust retry logic, circuit breaker protection, observability, and multi-channel alerting.

The system focuses on reliability, graceful degradation, and production-grade error handling rather than actual telephony.

Screenshot:
link: https://drive.google.com/file/d/1nHYlOCNRsHYoD9nYTwi01MSrWK7EsfKI/view?usp=sharing

🏗 Architecture Decisions
High-Level Flow
main.py
  └── call_engine.call_processor
        ├── services.elevenlabs (external dependency)
        ├── core.retry (retry logic)
        ├── core.circuit_breaker (fault isolation)
        ├── observability.logger (structured logging)
        └── alerts (email / telegram / webhook)

Folder Responsibilities
Folder	Responsibility
config/	Centralized configuration (thresholds, retries, cooldowns)
core/	Cross-cutting concerns (retry, circuit breaker, health check)
services/	External integrations (LLM, ElevenLabs, CRM)
call_engine/	Call orchestration & queue handling
observability/	Structured logging & Google Sheets integration
alerts/	Alerting via Email, Telegram, Webhook

📌 Design Principle:
Each layer has a single responsibility, enabling easier testing, replacement, and extension.

❌ Error Flow (Failure Handling)
Failure Scenario Example

Call attempt starts

External AI service fails

Retry mechanism triggers

Circuit breaker evaluates failures

If threshold exceeded → circuit opens

Alerts are triggered

Call is skipped safely

Error Propagation
Service Failure
   ↓
Retry Logic
   ↓
Circuit Breaker
   ↓
Alerting System
   ↓
Graceful Skip (No crash)


📌 Key Goal:
Failures never crash the system — they are contained, logged, and reported.

🔁 Retry Behavior

Implemented in core/retry.py

Characteristics

Configurable retry attempts

Exponential backoff (optional extension)

Service-specific retry context

Example Terminal Output
[RETRY] ElevenLabs attempt 1
[RETRY] ElevenLabs attempt 2
[RETRY] ElevenLabs attempt 3


📌 Retries happen before marking a call as failed.

⚡ Circuit Breaker Behavior

Implemented in core/circuit_breaker.py

States

CLOSED → Normal operation

OPEN → Calls blocked (external service unstable)

HALF-OPEN → Recovery testing

Trigger Rules

Opens after failure_threshold consecutive failures

Cooldown window before retrying

Automatically closes on successful recovery

Example Logs
[CIRCUIT] OPEN
[CIRCUIT] CLOSED


📌 Prevents cascading failures and protects system stability.

🚨 Alerting Logic

Alerts are triggered only after permanent failure (post retries).

Supported Channels
Channel	File
Email	alerts/email_alert.py
Telegram	alerts/telegram_alert.py
Webhook	alerts/webhook_alert.py
Example Output
[EMAIL] Call Failed -> +91-8888888882
[TELEGRAM] Call failed for +91-8888888882
[WEBHOOK] {'contact': '+91-8888888882', 'status': 'failed'}


📌 Alerts are non-blocking — failures in alert delivery do not impact core flow.

📊 Observability & Logs
Structured Logging

Logs are written to:

logs.jsonl

Example Log Entry
{
  "timestamp": "2026-01-29T12:35:21",
  "service": "elevenlabs",
  "status": "failed",
  "type": "transient"
}

Benefits

Easy debugging

Production-style observability

Post-mortem analysis

▶ Run
python main.py


