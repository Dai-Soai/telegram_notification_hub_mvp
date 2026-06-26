from typing import Any

from telegram_notification_hub.contract import NotificationMessage, TelegramConfig
from telegram_notification_hub.sender import TelegramSender


class FakeResponse:
    def __init__(self, status_code: int, text: str = "") -> None:
        self.status_code = status_code
        self.text = text


class FakeHttpClient:
    def __init__(self, response: FakeResponse) -> None:
        self.response = response
        self.last_url: str | None = None
        self.last_json: dict[str, Any] | None = None
        self.last_timeout: int | None = None

    def post(
        self,
        url: str,
        json: dict[str, Any],
        timeout: int,
    ) -> FakeResponse:
        self.last_url = url
        self.last_json = json
        self.last_timeout = timeout
        return self.response


class RaisingHttpClient:
    def post(
        self,
        url: str,
        json: dict[str, Any],
        timeout: int,
    ) -> None:
        raise RuntimeError("network error")


def test_telegram_sender_api_url():
    config = TelegramConfig(
        token="test-token",
        chat_id="123456",
    )

    sender = TelegramSender(config=config)

    assert sender.api_url == "https://api.telegram.org/bottest-token/sendMessage"


def test_telegram_sender_success():
    config = TelegramConfig(
        token="test-token",
        chat_id="123456",
    )
    fake_http = FakeHttpClient(FakeResponse(status_code=200, text="ok"))
    sender = TelegramSender(config=config, http_client=fake_http, timeout=5)

    message = NotificationMessage(
        title="✅ Workflow completed",
        body="Workflow: sample_workflow",
    )

    result = sender.send(message)

    assert result.ok is True
    assert result.status == "success"
    assert result.provider == "telegram"
    assert result.response_code == 200

    assert fake_http.last_url == "https://api.telegram.org/bottest-token/sendMessage"
    assert fake_http.last_json == {
        "chat_id": "123456",
        "text": "✅ Workflow completed\n\nWorkflow: sample_workflow",
    }
    assert fake_http.last_timeout == 5


def test_telegram_sender_api_failure():
    config = TelegramConfig(
        token="bad-token",
        chat_id="123456",
    )
    fake_http = FakeHttpClient(FakeResponse(status_code=401, text="Unauthorized"))
    sender = TelegramSender(config=config, http_client=fake_http)

    message = NotificationMessage(
        title="❌ Workflow failed",
        body="Workflow: sample_workflow",
    )

    result = sender.send(message)

    assert result.ok is False
    assert result.status == "failed"
    assert result.response_code == 401
    assert result.error == "Unauthorized"


def test_telegram_sender_network_failure():
    config = TelegramConfig(
        token="test-token",
        chat_id="123456",
    )
    sender = TelegramSender(config=config, http_client=RaisingHttpClient())

    message = NotificationMessage(
        title="RADAR Notification",
        body="System ready.",
    )

    result = sender.send(message)

    assert result.ok is False
    assert result.status == "failed"
    assert result.message == "request failed"
    assert result.error == "network error"
