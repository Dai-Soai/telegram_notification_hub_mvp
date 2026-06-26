from telegram_notification_hub.contract import WorkflowLogSummary
from telegram_notification_hub.formatter import (
    format_plain_message,
    format_workflow_message,
)


def test_format_workflow_success_message():
    summary = WorkflowLogSummary(
        workflow_id="sample_summary_workflow",
        status="success",
        steps_executed=3,
    )

    message = format_workflow_message(summary)

    assert message.title == "✅ Workflow completed"
    assert "Workflow: sample_summary_workflow" in message.body
    assert "Status: success" in message.body
    assert "Steps executed: 3" in message.body
    assert "Error:" not in message.body


def test_format_workflow_failed_message():
    summary = WorkflowLogSummary(
        workflow_id="sample_summary_workflow",
        status="failed",
        steps_executed=1,
        error="Input file not found",
    )

    message = format_workflow_message(summary)

    assert message.title == "❌ Workflow failed"
    assert "Workflow: sample_summary_workflow" in message.body
    assert "Status: failed" in message.body
    assert "Steps executed: 1" in message.body
    assert "Error: Input file not found" in message.body


def test_format_plain_message_with_body():
    message = format_plain_message(
        title="RADAR Notification",
        body="System is ready.",
    )

    assert message.title == "RADAR Notification"
    assert message.body == "System is ready."
    assert message.text == "RADAR Notification\n\nSystem is ready."


def test_format_plain_message_without_body():
    message = format_plain_message(
        title="RADAR Notification",
    )

    assert message.title == "RADAR Notification"
    assert message.body == ""
    assert message.text == "RADAR Notification"
