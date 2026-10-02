import csv

#TODO: Сделать поддержку различных разделителей
def parse_csv(file: _io.TextIOWrapper) -> Itrerator[dict[str: str | Level | datetime]]:
    """Построчный парсер файлов в формате csv

    Yields:
        Итератор с данными одного лога в формате словаря
    """
    for line_data in enumerate(csv.DictReader(file)):
        yield line_data

def parse_jsonl(file: _io.TextIOWrapper):
    pass

if __name__ == "__main__":
    with open("test_csv_files/test_files/valid.csv", "r", encoding="utf-8") as f:
        for i in parse_csv(f):
            print(i)