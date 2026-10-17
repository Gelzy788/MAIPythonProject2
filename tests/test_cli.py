import json

import pytest


def test_full_run_with_report(run_cli, shared_datadir, tmp_path, get_top_sources):
    result = run_cli(
        "analyze", shared_datadir / "valid.csv", shared_datadir / "valid.jsonl",
        "--format", "csv", "jsonl",
        "--output", "report.json",
    )

    assert result.returncode == 0, result.stderr
    report = json.loads((tmp_path / "report.json").read_text(encoding="utf-8"))
    assert report["count of logs"] == 7
    assert report["count of levels"] == {"DEBUG": 1, "INFO": 2, "WARNING": 1, "ERROR": 2, "CRITICAL": 1}
    assert report["source event count"] == {"auth": 2, "db": 2, "api": 2, "cache": 1}
    assert get_top_sources(report) == {"db": 2, "api": 1}
    assert report["first timestamp"] == "2026-10-01T10:00:00+03:00"
    assert report["last timestamp"] == "2026-10-02T09:02:00+03:00"

def test_broken_line_stops(run_cli, shared_datadir, tmp_path):
    result = run_cli("analyze", shared_datadir / "broken_line.csv", "--format", "csv", "--output", "report.json")

    assert result.returncode == 2
    assert "broken_line.csv" in result.stderr
    assert "в строке 3" in result.stderr
    assert not (tmp_path / "report.json").exists()


def test_skip_invalid(run_cli, shared_datadir, tmp_path):
    result = run_cli(
        "analyze", shared_datadir / "broken_line.csv",
        "--format", "csv", "--skip-invalid", "--output", "report.json",
    )

    assert result.returncode == 0, result.stderr
    report = json.loads((tmp_path / "report.json").read_text(encoding="utf-8"))
    assert report["count of logs"] == 2


@pytest.mark.parametrize("args", [
    ("analyze", "{data}/valid.csv", "--format", "xml"),
    ("analyze", "{data}/valid.csv", "--format", "csv jsonl")
])
def test_configuration_errors(run_cli, shared_datadir, tmp_path, args):
    result = run_cli(*(arg.format(data=shared_datadir, tmp=tmp_path) for arg in args))

    assert result.returncode == 2
    assert result.stderr.strip() != ""

def test_report_is_printed(run_cli, shared_datadir):
    result = run_cli("analyze", shared_datadir / "valid.csv", "--format", "csv")

    assert result.returncode == 0, result.stderr
    assert "count of logs" in result.stdout
