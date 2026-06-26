from __future__ import annotations

from typing import Any, Protocol

import requests

from telegram_notification_hub.contract import (
    NotificationMessage,
    SendResult,
    TelegramConfig,
)


class HttpClient(Protocol):
    def post(
        self,
        url: str,
        json: dict[str, Any],
        timeout: int,
    ) -> Any: ...


class TelegramSender:
    """
    Send notification messages to Telegram.

    http_client is injectable for tests.
    """

    def __init__(
        self,
        config: TelegramConfig,
        http_client: HttpClient | None = None,
        timeout: int = 10,
    ) -> None:
        self.config = config
        self.http_client = http_client or requests
        self.timeout = timeout

    @property
    def api_url(self) -> str:
        return f"https://api.telegram.org/bot{self.config.token}/sendMessage"

    def send(self, message: NotificationMessage) -> SendResult:
        try:
            response = self.http_client.post(
                self.api_url,
                json={
                    "chat_id": self.config.chat_id,
                    "text": message.text,
                },
                timeout=self.timeout,
            )

            status_code = getattr(response, "status_code", None)
            response_text = getattr(response, "text", "")

            if status_code == 200:
                return SendResult(
                    status="success",
                    provider="telegram",
                    message="sent",
                    response_code=status_code,
                )

            return SendResult(
                status="failed",
                provider="telegram",
                message="telegram api error",
                response_code=status_code,
                error=response_text,
            )

        except Exception as exc:
            return SendResult(
                status="failed",
                provider="telegram",
                message="request failed",
                error=str(exc),
            )
