import json

import pytest

from streamstats.errors import CliConfigurationError
from streamstats.result.result import ResultCreator

REPORT = {"count of logs": 2, "source event count": {"сервис": 2}}


def test_report_is_written_as_json(tmp_path):
    report_path = tmp_path / "report.json"

    ResultCreator.result_create(REPORT, str(report_path))

    assert json.loads(report_path.read_text(encoding="utf-8")) == REPORT

def test_report_is_printed(capsys):
    ResultCreator.result_create(REPORT)

    assert "count of logs" in capsys.readouterr().out

def test_missing_directory(tmp_path):
    report_path = tmp_path / "no_such_dir" / "report.json"
    
    with pytest.raises(CliConfigurationError):
        ResultCreator.result_create(REPORT, str(report_path))


@pytest.mark.parametrize("file_name", ["report.jsonl", "report.txt", "report"])
def test_wrong_extension_is_rejected(tmp_path, file_name):
    with pytest.raises(CliConfigurationError):
        ResultCreator.validate_output(str(tmp_path / file_name))
