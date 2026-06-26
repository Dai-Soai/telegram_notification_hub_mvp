from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

NotificationStatus = Literal["success", "failed"]
WorkflowStatus = Literal["success", "failed"]


@dataclass(frozen=True)
class TelegramConfig:
    """
    Telegram bot configuration.

    token:
        Telegram bot token.

    chat_id:
        Target Telegram chat ID.
    """

    token: str
    chat_id: str


@dataclass(frozen=True)
class WorkflowLogSummary:
    """
    Minimal summary extracted from a workflow execution log.
    """

    workflow_id: str
    status: WorkflowStatus
    steps_executed: int
    error: str | None = None


@dataclass(frozen=True)
class NotificationMessage:
    """
    Message ready to be sent to Telegram.
    """

    title: str
    body: str

    @property
    def text(self) -> str:
        if not self.body.strip():
            return self.title
        return f"{self.title}\n\n{self.body}"


@dataclass(frozen=True)
class SendResult:
    """
    Result returned after attempting to send a notification.
    """

    status: NotificationStatus
    provider: str
    message: str
    response_code: int | None = None
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.status == "success"
