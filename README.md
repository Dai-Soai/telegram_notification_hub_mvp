# Telegram Notification Hub MVP

A minimal Telegram notification hub for RADAR Services utilities.

## Status

MVP in progress.

## Purpose

Reads workflow execution logs and sends formatted Telegram alerts.

## Target Flow

```text
execution_log.json
    ↓
message formatter
    ↓
telegram sender
    ↓
telegram chat
