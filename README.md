# Telegram Notification Hub MVP

## Overview

Telegram Notification Hub MVP is a reusable notification utility for RADAR Services.

It consumes workflow execution logs and delivers formatted notifications through Telegram Bot API.

---

## Features

- Plain Telegram notification
- Workflow execution notification
- JSON execution log reader
- CLI interface
- Environment variable support
- Reusable notification formatter
- Pytest tested

---

## Project Structure

telegram_notification_hub_mvp/
├── examples/
├── src/
│   └── telegram_notification_hub/
├── tests/
├── README.md
├── pyproject.toml
└── .gitignore

---

## Installation

python -m venv .venv

source .venv/bin/activate

pip install -e .

---

## Environment

TELEGRAM_BOT_TOKEN=...

TELEGRAM_CHAT_ID=...

---

## CLI

telegram-notifier send ...

telegram-notifier send-log ...

---

## Example

telegram-notifier send \
    --title "RADAR Test" \
    --body "Hello"

telegram-notifier send-log \
    examples/workflow_execution.sample.json

---

## Integration

Utility #8
↓

execution_log.json

↓

Utility #9

↓

Telegram Notification

---

## Tests

pytest

Expected

38 passed

---

## License

MIT
