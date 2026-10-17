import pytest

from streamstats.errors import InvalidEventError, StreamStatsError
from streamstats.parsing.file_parsers import parse_csv, parse_jsonl


# Тесты CSV парсера
def test_csv_valid_file(read_rows):
    rows = read_rows(parse_csv, "valid.csv")

    assert rows[0][1] == {
        "timestamp": "2026-10-01T10:00:00+03:00",
        "level": "INFO",
        "source": "auth",
        "message": "User logged in",
    }

def test_csv_empty_file(read_rows):
    with pytest.raises(StreamStatsError):
        read_rows(parse_csv, "empty.csv")

def test_csv_header_only(read_rows):
    assert read_rows(parse_csv, "header_only.csv") == []

def test_csv_missing_column_in_header(read_rows):
    with pytest.raises(InvalidEventError):
        read_rows(parse_csv, "missing_column.csv")

def test_csv_unicode(read_rows):
    rows = read_rows(parse_csv, "unicode.csv")

    assert rows[0][1]["source"] == "сервис-авторизации"
    assert rows[1][1]["source"] == "你好"


# Тесты jsonl парсера
def test_jsonl_valid_file(read_rows):
    rows = read_rows(parse_jsonl, "valid.jsonl")

    assert rows[1][1]["message"] == "Timeout"

def test_jsonl_empty_file(read_rows):
    assert read_rows(parse_jsonl, "empty.jsonl") == []

def test_jsonl_broken_json(read_rows):
    rows = read_rows(parse_jsonl, "broken_json.jsonl")

    assert isinstance(rows[1][1], InvalidEventError)
    assert isinstance(rows[2][1], dict)

def test_jsonl_unicode(read_rows):
    rows = read_rows(parse_jsonl, "unicode.jsonl")

    assert rows[0][1]["message"] == "Пользователь вошёл"
    assert rows[1][1]["message"] == "连接失败"
