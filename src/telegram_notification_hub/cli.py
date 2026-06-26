from __future__ import annotations

import argparse
import os
import sys

from telegram_notification_hub.contract import TelegramConfig
from telegram_notification_hub.formatter import (
    format_plain_message,
    format_workflow_message,
)
from telegram_notification_hub.log_reader import WorkflowLogReadError, load_workflow_log
from telegram_notification_hub.sender import TelegramSender


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="telegram-notifier",
        description="Send Telegram notifications for RADAR Services utilities.",
    )

    subparsers = parser.add_subparsers(dest="command")

    send_parser = subparsers.add_parser(
        "send",
        help="Send a plain Telegram notification.",
    )
    send_parser.add_argument(
        "--token",
        default=os.getenv("TELEGRAM_BOT_TOKEN"),
        help="Telegram bot token. Defaults to TELEGRAM_BOT_TOKEN.",
    )
    send_parser.add_argument(
        "--chat-id",
        default=os.getenv("TELEGRAM_CHAT_ID"),
        help="Telegram chat ID. Defaults to TELEGRAM_CHAT_ID.",
    )
    send_parser.add_argument(
        "--title",
        required=True,
        help="Notification title.",
    )
    send_parser.add_argument(
        "--body",
        default="",
        help="Notification body.",
    )
    send_log_parser = subparsers.add_parser(
        "send-log",
        help="Read workflow execution log and send Telegram notification.",
    )
    send_log_parser.add_argument(
        "log_file",
        help="Path to workflow execution log JSON.",
    )
    send_log_parser.add_argument(
        "--token",
        default=os.getenv("TELEGRAM_BOT_TOKEN"),
        help="Telegram bot token. Defaults to TELEGRAM_BOT_TOKEN.",
    )
    send_log_parser.add_argument(
        "--chat-id",
        default=os.getenv("TELEGRAM_CHAT_ID"),
        help="Telegram chat ID. Defaults to TELEGRAM_CHAT_ID.",
    )

    return parser


def run_send_command(args: argparse.Namespace) -> int:
    if not args.token:
        print("Missing Telegram bot token", file=sys.stderr)
        return 1

    if not args.chat_id:
        print("Missing Telegram chat ID", file=sys.stderr)
        return 1

    config = TelegramConfig(
        token=args.token,
        chat_id=args.chat_id,
    )
    message = format_plain_message(
        title=args.title,
        body=args.body,
    )

    sender = TelegramSender(config=config)
    result = sender.send(message)

    if result.ok:
        print("Telegram notification sent")
        return 0

    print(f"Telegram notification failed: {result.error}", file=sys.stderr)
    return 1


def run_send_log_command(args: argparse.Namespace) -> int:
    if not args.token:
        print("Missing Telegram bot token", file=sys.stderr)
        return 1

    if not args.chat_id:
        print("Missing Telegram chat ID", file=sys.stderr)
        return 1

    try:
        summary = load_workflow_log(args.log_file)
    except WorkflowLogReadError as exc:
        print(f"Failed to read workflow log: {exc}", file=sys.stderr)
        return 1

    config = TelegramConfig(
        token=args.token,
        chat_id=args.chat_id,
    )
    message = format_workflow_message(summary)

    sender = TelegramSender(config=config)
    result = sender.send(message)

    if result.ok:
        print("Telegram workflow notification sent")
        return 0

    print(f"Telegram workflow notification failed: {result.error}", file=sys.stderr)
    return 1


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "send":
        return run_send_command(args)

    if args.command == "send-log":
        return run_send_log_command(args)

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
