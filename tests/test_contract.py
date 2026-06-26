from telegram_notification_hub.contract import (
    NotificationMessage,
    SendResult,
    TelegramConfig,
    WorkflowLogSummary,
)


def test_telegram_config_contract():
    config = TelegramConfig(
        token="test-token",
        chat_id="123456",
    )

    assert config.token == "test-token"
    assert config.chat_id == "123456"


def test_workflow_log_summary_contract_success():
    summary = WorkflowLogSummary(
        workflow_id="sample_workflow",
        status="success",
        steps_executed=3,
    )

    assert summary.workflow_id == "sample_workflow"
    assert summary.status == "success"
    assert summary.steps_executed == 3
    assert summary.error is None


def test_workflow_log_summary_contract_failed():
    summary = WorkflowLogSummary(
        workflow_id="sample_workflow",
        status="failed",
        steps_executed=1,
        error="Input file not found",
    )

    assert summary.status == "failed"
    assert summary.error == "Input file not found"


def test_notification_message_text_with_body():
    message = NotificationMessage(
        title="✅ Workflow completed",
        body="Workflow: sample_workflow\nStatus: success",
    )

    assert (
        message.text
        == "✅ Workflow completed\n\nWorkflow: sample_workflow\nStatus: success"
    )


def test_notification_message_text_without_body():
    message = NotificationMessage(
        title="✅ Workflow completed",
        body="",
    )

    assert message.text == "✅ Workflow completed"


def test_send_result_success():
    result = SendResult(
        status="success",
        provider="telegram",
        message="sent",
        response_code=200,
    )

    assert result.ok is True
    assert result.status == "success"
    assert result.response_code == 200


def test_send_result_failed():
    result = SendResult(
        status="failed",
        provider="telegram",
        message="failed",
        response_code=401,
        error="Unauthorized",
    )

    assert result.ok is False
    assert result.status == "failed"
    assert result.error == "Unauthorized"
