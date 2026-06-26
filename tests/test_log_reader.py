import json
from pathlib import Path

import pytest

from telegram_notification_hub.log_reader import (
    WorkflowLogReadError,
    load_json_file,
    load_workflow_log,
    workflow_summary_from_dict,
)


def test_load_json_file(tmp_path: Path):
    log_file = tmp_path / "execution.json"
    log_file.write_text(
        json.dumps(
            {
                "workflow_id": "sample_workflow",
                "status": "success",
                "steps_executed": 3,
                "error": None,
            }
        ),
        encoding="utf-8",
    )

    payload = load_json_file(log_file)

    assert payload["workflow_id"] == "sample_workflow"
    assert payload["status"] == "success"


def test_workflow_summary_from_dict_success():
    summary = workflow_summary_from_dict(
        {
            "workflow_id": "sample_workflow",
            "status": "success",
            "steps_executed": 3,
            "error": None,
        }
    )

    assert summary.workflow_id == "sample_workflow"
    assert summary.status == "success"
    assert summary.steps_executed == 3
    assert summary.error is None


def test_workflow_summary_from_dict_failed():
    summary = workflow_summary_from_dict(
        {
            "workflow_id": "sample_workflow",
            "status": "failed",
            "steps_executed": 1,
            "error": "Input file not found",
        }
    )

    assert summary.workflow_id == "sample_workflow"
    assert summary.status == "failed"
    assert summary.steps_executed == 1
    assert summary.error == "Input file not found"


def test_workflow_summary_rejects_invalid_status():
    with pytest.raises(WorkflowLogReadError, match="Invalid workflow status"):
        workflow_summary_from_dict(
            {
                "workflow_id": "sample_workflow",
                "status": "unknown",
                "steps_executed": 0,
            }
        )


def test_load_workflow_log(tmp_path: Path):
    log_file = tmp_path / "execution.json"
    log_file.write_text(
        json.dumps(
            {
                "workflow_id": "sample_workflow",
                "status": "success",
                "steps_executed": 3,
                "error": None,
            }
        ),
        encoding="utf-8",
    )

    summary = load_workflow_log(log_file)

    assert summary.workflow_id == "sample_workflow"
    assert summary.status == "success"
    assert summary.steps_executed == 3


def test_load_missing_workflow_log():
    with pytest.raises(WorkflowLogReadError, match="Workflow log file not found"):
        load_workflow_log("missing-execution.json")


def test_load_invalid_json(tmp_path: Path):
    log_file = tmp_path / "invalid.json"
    log_file.write_text("{invalid-json", encoding="utf-8")

    with pytest.raises(WorkflowLogReadError, match="Invalid workflow log JSON"):
        load_workflow_log(log_file)


def test_load_json_root_must_be_object(tmp_path: Path):
    log_file = tmp_path / "invalid-root.json"
    log_file.write_text("[1, 2, 3]", encoding="utf-8")

    with pytest.raises(
        WorkflowLogReadError, match="Workflow log root must be a JSON object"
    ):
        load_workflow_log(log_file)
