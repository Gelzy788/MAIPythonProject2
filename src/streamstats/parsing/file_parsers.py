import csv
import json

from streamstats.errors import InvalidEventError
from streamstats.models import REQUIRED_FIELDS

def parse_csv(file: _io.TextIOWrapper) -> Iterator[dict[str, str | Level | datetime]]:
    """Построчный парсер файлов в формате csv

    Yields:
        Итератор с данными одного лога в формате словаря
    """
    # Находим разделитель
    sample = file.readline()
    file.seek(0)
    sniffer = csv.Sniffer()
    separator = sniffer.sniff(sample, delimiters=[',', ';', '\t', '|'])

    reader = csv.DictReader(file, delimiter=separator.delimiter)
    
    if reader.fieldnames is None:
        return
    
    missing_columns = [field for field in REQUIRED_FIELDS if field not in reader.fieldnames]
    if missing_columns:
        raise InvalidEventError(f"В заголовке CSV файла {file.name} отсутствуют обязательные колонки: "
                                f"{', '.join(missing_columns)}")
    
    for line_data in reader:
        if None in line_data:
            yield (reader.line_num, InvalidEventError("В строке больше полей, чем в заголовке CSV"))
            continue
        yield (reader.line_num, line_data)

def parse_jsonl(file: _io.TextIOWrapper) -> Iterator[dict[str, str | Level | datetime]]:
    """Построчный парсер файлов в формате jsonl

    Yields:
        Итератор с данными одного лога в формате словаря
    """
    for line_data in enumerate(file, start=1):
        if line_data[1].strip() == "":
            continue
        
        try:
            parsed_line = json.loads(line_data[1])
        except json.JSONDecodeError as err:
            yield (line_data[0], InvalidEventError(f"Невалидный JSON: {err.msg}"))
            continue
        
        yield (line_data[0], parsed_line)

if __name__ == "__main__":
    # with open("test_csv_files/test_files/valid.csv", "r", encoding="utf-8") as f:
    #     for i in parse_csv(f):
    #         print(i)
    with open("test_csv_files/test_files/valid.jsonl", "r", encoding="utf-8") as f:
        for i in parse_csv(f):
            print(i)
            break
