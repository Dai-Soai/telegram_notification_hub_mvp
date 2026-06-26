# Workflow Runner Integration Example

## Purpose

This document describes how Utility #9 — Telegram Notification Hub MVP integrates with Utility #8 — Workflow Runner MVP through execution log JSON.

## Integration Flow

```text
Utility #8 — Workflow Runner
        ↓
writes execution_log.json
        ↓
Utility #9 — Telegram Notification Hub
        ↓
reads workflow execution log
        ↓
formats notification message
        ↓
sends Telegram alert
```

## Contract Boundary

Utility #8 owns:

- workflow YAML loading
- workflow validation
- sequential step execution
- output writing
- execution log JSON

Utility #9 owns:

- execution log reading
- workflow summary extraction
- notification formatting
- Telegram delivery

---

## Locked Decision

No direct package dependency is introduced between Utility #8 and Utility #9.

Utility #9 consumes execution log JSON as an external contract.
