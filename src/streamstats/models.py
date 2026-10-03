from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from streamstats.errors import InvalidTimestampError

class Level(Enum):
    """Enum уровней логов.
    """
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

@dataclass(frozen=True)
class Event:
    """Класс с данными одного лога
    """
    timestamp: datetime
    level: Level
    source: str
    message: str
    
    @staticmethod
    def create_event(data: dict) -> Event:
        """Конструктор объектов Event

        Args:
            data (dict): Данные из строки с логами

        Raises:
            InvalidTimestampError: Если неправильный формат времени
            InvalidLevelError: Если неизвестный уровень лога

        Returns:
            Event: Объект класса Event
        """
        try:
            timestamp = datetime.fromisoformat(data["timestamp"])
        except ValueError:
            raise InvalidTimestampError()
        
        try: # NOTE: Надо ли писать кастомное сообщение? Или вообще сделать отдельную ошибку?
            level = Level(data["level"].upper())
        except ValueError:
            raise InvalidEventError()
        
        if data["source"] == "":
            raise InvalidEventError()
        
        return Event(timestamp,
                    level,
                    data["source"],
                    data["message"])
    

if __name__ == "__main__":
    # data = {
    #     "timestamp": "2026-10-02T12:30:45+03:00",
    #     "level": "DEBUG",
    #     "source": "hello",
    #     "message": "Hello World!"
    # }
    # event1 = Event.create_event(data)
    # print(event1)
    for i in Level:
        print(i)