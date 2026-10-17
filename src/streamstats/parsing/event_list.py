import logging
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import TextIO

from streamstats.constants import SUPPORTED_FORMATS
from streamstats.errors import (
    CliConfigurationError,
    InvalidEventError,
    StreamStatsError,
    UnsupportedFormatError,
)
from streamstats.models import Event
from streamstats.parsing.file_parsers import ParsedRow, parse_csv, parse_jsonl

logger = logging.getLogger(__name__)


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
    
    def _parse_file(self, file: TextIO, file_format: str) -> Iterator[ParsedRow]:
        """Запускает парсинг файлов в зависимости от типа файла: json/csv

        Args:
            file (TextIO): Уже открытый файл

        Returns:
            Итератор с данными из лога в формате словаря
        """
        if file_format == "csv":
            yield from parse_csv(file)
        elif file_format == "jsonl":
            yield from parse_jsonl(file)
        else:
            raise UnsupportedFormatError(f"Формат {file_format} не поддерживается")
        
    def __iter__(self) -> Iterator[Event | str]:
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
                with open(path, "r", encoding="utf-8-sig", newline="") as file:
                    yield from self._iter_file(file, path, self.file_format[num])
            except OSError as err:
                raise CliConfigurationError(f"Не удалось открыть файл {path}: {err.strerror}") from err

    def _iter_file(self, file: TextIO, path: Path, file_format: str) -> Iterator[Event | str]:
        """Превращает строки одного открытого файла в объекты Event

        Raises:
            InvalidEventError: Если в логе ошибка и не включён skip_invalid
            StreamStatsError: Если файл не в кодировке UTF-8

        Yields:
            Event или строка "WARNING" для пропущенной невалидной строки
        """
        try:
            for line_num, line in self._parse_file(file, file_format):
                try:
                    if isinstance(line, InvalidEventError):
                        raise line
                    yield Event.create_event(line)
                except InvalidEventError as err:
                    if not self.skip_invalid:
                        raise InvalidEventError(f"В логе по пути {path} "
                                                f"в строке {line_num} "
                                                f"ошибка: {err}") from err
                    logger.warning("Invalid event: %s, %s, %s", type(err).__name__, line_num, err)
                    yield "WARNING"
        except UnicodeDecodeError as err:
            raise StreamStatsError(f"Файл {path} не является текстовым файлом в кодировке UTF-8") from err
