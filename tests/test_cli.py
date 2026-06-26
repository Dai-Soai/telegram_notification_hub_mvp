from telegram_notification_hub.cli import main


class FakeSendResult:
    def __init__(self, ok: bool, error: str | None = None) -> None:
        self.ok = ok
        self.error = error


class FakeSenderSuccess:
    def __init__(self, config) -> None:
        self.config = config

    def send(self, message):
        return FakeSendResult(ok=True)


class FakeSenderFailure:
    def __init__(self, config) -> None:
        self.config = config

    def send(self, message):
        return FakeSendResult(ok=False, error="Unauthorized")


def test_cli_help(monkeypatch, capsys):
    monkeypatch.setattr(
        "sys.argv",
        ["telegram-notifier"],
    )

    exit_code = main()
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Send Telegram notifications" in captured.out


def test_cli_send_success(monkeypatch, capsys):
    monkeypatch.setattr(
        "telegram_notification_hub.cli.TelegramSender",
        FakeSenderSuccess,
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "telegram-notifier",
            "send",
            "--token",
            "test-token",
            "--chat-id",
            "123456",
            "--title",
            "RADAR Notification",
            "--body",
            "System ready.",
        ],
    )

    exit_code = main()
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Telegram notification sent" in captured.out


def test_cli_send_failure(monkeypatch, capsys):
    monkeypatch.setattr(
        "telegram_notification_hub.cli.TelegramSender",
        FakeSenderFailure,
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "telegram-notifier",
            "send",
            "--token",
            "bad-token",
            "--chat-id",
            "123456",
            "--title",
            "RADAR Notification",
        ],
    )

    exit_code = main()
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Telegram notification failed: Unauthorized" in captured.err


def test_cli_send_missing_token(monkeypatch, capsys):
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.setattr(
        "sys.argv",
        [
            "telegram-notifier",
            "send",
            "--chat-id",
            "123456",
            "--title",
            "RADAR Notification",
        ],
    )

    exit_code = main()
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Missing Telegram bot token" in captured.err


def test_cli_send_missing_chat_id(monkeypatch, capsys):
    monkeypatch.delenv("TELEGRAM_CHAT_ID", raising=False)
    monkeypatch.setattr(
        "sys.argv",
        [
            "telegram-notifier",
            "send",
            "--token",
            "test-token",
            "--title",
            "RADAR Notification",
        ],
    )

    exit_code = main()
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Missing Telegram chat ID" in captured.err


def test_cli_send_uses_env(monkeypatch, capsys):
    monkeypatch.setattr(
        "telegram_notification_hub.cli.TelegramSender",
        FakeSenderSuccess,
    )
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "env-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "env-chat-id")
    monkeypatch.setattr(
        "sys.argv",
        [
            "telegram-notifier",
            "send",
            "--title",
            "RADAR Notification",
        ],
    )

    exit_code = main()
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Telegram notification sent" in captured.out
