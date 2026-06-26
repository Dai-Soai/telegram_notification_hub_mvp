from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from telegram_notification_hub.contract import WorkflowLogSummary


class WorkflowLogReadError(Exception):
    """Raised when workflow execution log cannot be read."""


def load_json_file(path: str | Path) -> dict[str, Any]:
    log_path = Path(path)

    if not log_path.exists():
        raise WorkflowLogReadError(f"Workflow log file not found: {log_path}")

    if not log_path.is_file():
        raise WorkflowLogReadError(f"Workflow log path is not a file: {log_path}")

    try:
        payload = json.loads(log_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise WorkflowLogReadError(f"Invalid workflow log JSON: {log_path}") from exc

    if not isinstance(payload, dict):
        raise WorkflowLogReadError("Workflow log root must be a JSON object")

    return payload


def workflow_summary_from_dict(payload: dict[str, Any]) -> WorkflowLogSummary:
    workflow_id = str(payload.get("workflow_id", ""))
    status = str(payload.get("status", ""))
    steps_executed = int(payload.get("steps_executed", 0))
    error = payload.get("error")

    if status not in {"success", "failed"}:
        raise WorkflowLogReadError(f"Invalid workflow status: {status}")

    return WorkflowLogSummary(
        workflow_id=workflow_id,
        status=status,  # type: ignore[arg-type]
        steps_executed=steps_executed,
        error=str(error) if error else None,
    )


def load_workflow_log(path: str | Path) -> WorkflowLogSummary:
    payload = load_json_file(path)
    return workflow_summary_from_dict(payload)
