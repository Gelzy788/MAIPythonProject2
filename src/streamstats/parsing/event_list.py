from dataclasses import dataclass
from pathlib import Path
from streamstats.models import Event
from streamstats.errors import (InvalidEventError, UnsupportedFormatError,
                                CliConfigurationError, StreamStatsError)
from streamstats.constants import SUPPORTED_FORMATS
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
    
    def __post_init__(self) -> None:
        if isinstance(self.file_format, str):
            raise CliConfigurationError("Форматы файлов должны передаваться списком")
        
        if len(self.file_format) != len(self.paths):
            raise CliConfigurationError(f"Количество форматов ({len(self.file_format)}) "
                                        f"не совпадает с количеством файлов ({len(self.paths)})")
        
        for file_format in self.file_format:
            if file_format not in SUPPORTED_FORMATS:
                raise UnsupportedFormatError(f"Формат {file_format} не поддерживается. "
                                             f"Доступные форматы: {', '.join(sorted(SUPPORTED_FORMATS))}")
        
        for path in self.paths:
            if not Path(path).exists():
                raise CliConfigurationError(f"Файл {path} не найден")
            if not Path(path).is_file():
                raise CliConfigurationError(f"{path} не является файлом")
    
    def _parse_file(self, file: _io.TextIOWrapper, file_format: str) -> Itrerator[dict[str: str | Level | datetime]]:
        """Запускает парсинг файлов в зависимости от типа файла: json/csv

        Args:
            file (_io.TextIOWrapper): Уже открытый файл

        Returns:
            Итератор с данными из лога в формате словаря
        """
        if file_format == "csv":
            yield from parse_csv(file)
        elif file_format == "jsonl":
            yield from parse_jsonl(file)
        else:
            raise UnsupportedFormatError(f"Формат {file_format} не поддерживается")
        
    def __iter__(self) -> Iterator[Event]:
        """Итерирвоание объекта класса
        
            При каждом запросе парсит файл, упаковывет данные в объект Event
            и возвращает

        Raises:
            InvalidEventError: Если в логе что-то написано неправильно

        Yields:
            Iterator[Event]: один итератор с логом в формате объекта Event
        """
        for num, path in enumerate(self.paths):
            try:
                file = open(path, "r", encoding="utf-8-sig", newline="")
            except OSError as err:
                raise CliConfigurationError(f"Не удалось открыть файл {path}: {err.strerror}") from err
            
            with file:
                try:
                    for line_num, line in self._parse_file(file, self.file_format[num]):
                        try:
                            if isinstance(line, InvalidEventError):
                                raise line
                            event = Event.create_event(line)
                            yield event
                        except InvalidEventError as err:
                            if not self.skip_invalid:
                                raise InvalidEventError(f"В логе по пути {path} "
                                                        f"в строке {line_num} "
                                                        f"ошибка: {err}") from err
                            # TODO Сделать логирование WARNING
                            print("WARNING")
                            continue
                except UnicodeDecodeError as err:
                    raise StreamStatsError(f"Файл {path} не является текстовым файлом в кодировке UTF-8") from err

if __name__ == "__main__":
    for i in EventList(["test_csv_files/test_files/valid.csv"], "csv", False):
        print(i)
