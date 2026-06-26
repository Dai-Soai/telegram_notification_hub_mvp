from pathlib import Path

from telegram_notification_hub.formatter import format_workflow_message
from telegram_notification_hub.log_reader import load_workflow_log


def test_workflow_runner_execution_log_sample_exists():
    log_file = Path("examples/workflow_execution.sample.json")

    assert log_file.exists()


def test_workflow_runner_execution_log_can_be_loaded():
    log_file = Path("examples/workflow_execution.sample.json")

    summary = load_workflow_log(log_file)

    assert summary.workflow_id == "sample_summary_workflow"
    assert summary.status == "success"
    assert summary.steps_executed == 3
    assert summary.error is None


def test_workflow_runner_execution_log_formats_message():
    log_file = Path("examples/workflow_execution.sample.json")

    summary = load_workflow_log(log_file)
    message = format_workflow_message(summary)

    assert message.title == "✅ Workflow completed"
    assert "Workflow: sample_summary_workflow" in message.body
    assert "Status: success" in message.body
    assert "Steps executed: 3" in message.body


def test_workflow_runner_integration_doc_exists():
    doc_file = Path("examples/workflow_runner_integration_example.md")

    assert doc_file.exists()

    content = doc_file.read_text(encoding="utf-8")

    assert "Utility #8" in content
    assert "Utility #9" in content
    assert "No direct package dependency" in content
    assert "execution log JSON" in content
