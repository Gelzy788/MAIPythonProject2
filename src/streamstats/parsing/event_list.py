from dataclasses import dataclass
from pathlib import Path
from streamstats.models import Event
from streamstats.errors import InvalidEventError
from streamstats.parsing.file_parsers import parse_csv, parse_jsonl

@dataclass()
class EventList:
    """Парсинг и получение логов в формате event

    Raises:
        InvalidEventError: если в стркое с логом ошибка
    """
    paths: list[Path]
    file_format: str
    skip_invalid: bool
    
    def _parse_file(self, file: _io.TextIOWrapper) -> Itrerator[dict[str: str | Level | datetime]]:
        """Запускает парсинг файлов в зависимости от типа файла: json/csv

        Args:
            file (_io.TextIOWrapper): Уже открытый файл

        Returns:
            Итератор с данными из лога в формате словаря
        """
        if self.file_format == "csv":
            return parse_csv(file)
        if self.file_format == "jsonl":
            return parse_jsonl(file)
        
    def __iter__(self) -> Iterator[Event]:
        """Итерирвоание объекта класса
        
            При каждом запросе парсит файл, упаковывет данные в объект Event
            и возвращает

        Raises:
            InvalidEventError: Если в логе что-то написано неправильно

        Yields:
            Iterator[Event]: один итератор с логом в формате объекта Event
        """
        for path in self.paths:
            with open(path, "r" , encoding="utf-8") as file:
                for line_num, line in self._parse_file(file):
                    try:
                        event = Event.create_event(line)
                        yield event
                    except InvalidEventError as err:
                        if not self.skip_invalid:
                            raise InvalidEventError(f"В логе по пути {path}",
                                                    f"в строке {line_num}",
                                                    f"ошибка: {err}")
                        # TODO Сделать логирование WARNING
                        print("WARNING")
                        continue

if __name__ == "__main__":
    for i in EventList(["test_csv_files/test_files/valid.csv"], "csv", False):
        print(i)