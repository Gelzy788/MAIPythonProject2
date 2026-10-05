import csv
import json

# TODO: Сделать валидацию битых файлов/строк
#TODO: Сделать поддержку различных разделителей
def parse_csv(file: _io.TextIOWrapper) -> Iterator[dict[str, str | Level | datetime]]:
    """Построчный парсер файлов в формате csv

    Yields:
        Итератор с данными одного лога в формате словаря
    """
    for line_data in enumerate(csv.DictReader(file)):
        yield line_data

def parse_jsonl(file: _io.TextIOWrapper) -> Iterator[dict[str, str | Level | datetime]]:
    """Построчный парсер файлов в формате jsonl

    Yields:
        Итератор с данными одного лога в формате словаря
    """
    for line_data in file:
        yield json.loads(line_data)

if __name__ == "__main__":
    # with open("test_csv_files/test_files/valid.csv", "r", encoding="utf-8") as f:
    #     for i in parse_csv(f):
    #         print(i)
    with open("test_csv_files/test_files/valid.jsonl", "r", encoding="utf-8") as f:
        for i in parse_csv(f):
            print(i)
            break