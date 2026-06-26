from __future__ import annotations

from telegram_notification_hub.contract import (
    NotificationMessage,
    WorkflowLogSummary,
)


def format_workflow_message(summary: WorkflowLogSummary) -> NotificationMessage:
    """
    Convert workflow log summary into a Telegram notification message.
    """

    if summary.status == "success":
        title = "✅ Workflow completed"
    else:
        title = "❌ Workflow failed"

    body_lines = [
        f"Workflow: {summary.workflow_id}",
        f"Status: {summary.status}",
        f"Steps executed: {summary.steps_executed}",
    ]

    if summary.error:
        body_lines.append(f"Error: {summary.error}")

    return NotificationMessage(
        title=title,
        body="\n".join(body_lines),
    )


def format_plain_message(title: str, body: str = "") -> NotificationMessage:
    """
    Create a generic notification message.
    """

    return NotificationMessage(
        title=title,
        body=body,
    )
