from dataclasses import dataclass, field
from datetime import datetime
from streamstats.models import Level
from streamstats.constants import ERROR_LEVELS

class StatsCounter:
    def __init__(self):
        """Инициализация класса
        """
        self.count_of_logs: int = 0
        self.count_of_levels: dict = {level: 0 for level in Level}
        self.source_event_count: dict = {}
        self.source_error_count: dict = {}
        self.first_timestamp: datetime = None
        self.last_timestamp: datetime = None
    
    def _get_top_5_sources(self) -> dict[str, int]:
        """Получение топ 5 источников ошибок
        
            Возвращает словарь из топ-5 источников ошибок

        Returns:
            source_error_count_printable: Словарь из топ 5 источников ошибок
        """
        source_error_count_printable = dict(sorted(self.source_error_count.items(), key=lambda a: a[1], reverse=True))
        
        if len(source_error_count_printable) >= 5:
            print(dict(list(source_error_count_printable.items())))
            return dict(list(source_error_count_printable.items())[:5])
        return source_error_count_printable
    
    def add_log(self, log: Event) -> None:
        """Добавить лог в статистику
        
            Принимает на вход лог в формате объекта Event и
            Учитывает его в статистике

        Args:
            log (Event): данные одного лога(строки из файла)
        """
        self.count_of_logs += 1
        self.count_of_levels[log.level] += 1
        
        if log.source in self.source_event_count:
            self.source_event_count[log.source] += 1
        else:
            self.source_event_count[log.source] = 1
        
        
        if log.level in ERROR_LEVELS:
            if log.source in self.source_error_count:
                self.source_error_count[log.source] += 1
            else:
                self.source_error_count[log.source] = 1
        
        if (self.first_timestamp is None
            or log.timestamp < self.first_timestamp):
            self.first_timestamp = log.timestamp
        elif (self.last_timestamp is None
            or log.timestamp > self.last_timestamp):
            self.last_timestamp = log.timestamp
    
    def to_dict(self) -> dict[str, str | dict[str, int] | int]:
        """Выдает статистику в формате словаря
        
            Преобразует форматы типа datetime и Levels в читаемый вид
            Получает топ-5 источников ошибок, обращаясь к методу _get_top_5_sources
            Генерирует словарь со всеми полями статистики в формате "Поле": "статистика"

        Returns:
            Словарь с результатами подсчета статистики
        """
        count_of_levels_printable = {}
        for key, value in self.count_of_levels.items():
            count_of_levels_printable[key.value] = value
            
        return {"count of logs": self.count_of_logs,
                "count of levels": count_of_levels_printable,
                "source event count": self.source_event_count,
                "top 5 sources by errors ": self._get_top_5_sources(),
                "first timestamp": self.first_timestamp.isoformat() if self.first_timestamp else None,
                "last timestamp": self.last_timestamp.isoformat() if self.last_timestamp else None,
                }