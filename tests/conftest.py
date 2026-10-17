import os
import subprocess
import sys
from pathlib import Path

import pytest

SRC_DIR = Path(__file__).resolve().parents[1] / "src"


@pytest.fixture
def event_data() -> dict:
    """Словарь валидного события. Тесты меняют в нём одно поле."""
    return {
        "timestamp": "2026-10-01T10:00:00+03:00",
        "level": "INFO",
        "source": "auth",
        "message": "User logged in",
    }


@pytest.fixture
def get_top_sources():
    """Достаёт из отчёта топ источников ошибок, не завися от точного имени ключа."""
    def _get(report: dict) -> dict:
        keys = [key for key in report if key.strip().lower().startswith("top")]
        assert len(keys) == 1, f"В отчёте должен быть ровно один ключ с топом источников, ключи: {list(report)}"
        return report[keys[0]]
    return _get


@pytest.fixture
def read_rows(shared_datadir):
    """Открывает файл из tests/data так же, как EventList, и возвращает всё, что отдал парсер"""
    def _read(parser, file_name: str) -> list:
        with open(shared_datadir / file_name, "r", encoding="utf-8", newline="") as file:
            return list(parser(file))
    return _read


@pytest.fixture
def run_cli(tmp_path):
    """Запусккает программу из CLI через subprocess"""
    def _run(*args: str) -> subprocess.CompletedProcess:
        env = os.environ.copy()
        env["PYTHONPATH"] = os.pathsep.join(filter(None, [str(SRC_DIR), env.get("PYTHONPATH")]))
        return subprocess.run(
            [sys.executable, "-m", "streamstats", *map(str, args)],
            cwd=tmp_path,
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
    return _run
