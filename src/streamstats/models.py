from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from errors import InvalidTimestampError, InvalidLevelError

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
    timestamp: datetime
    level: Level
    source: str
    message: str
    
    @staticmethod
    def create_event(data: dict) -> Event:
        try:
            timestamp = datetime.fromisoformat(data["timestamp"])
        except ValueError:
            raise InvalidTimestampError()
        
        try:
            level = Level(data["level"])
        except ValueError:
            raise InvalidLevelError()
        
        # TODO: Добавить валидацию
        return Event(timestamp,
                    level,
                    data["source"],
                    data["message"])
    

if __name__ == "__main__":
    data = {
        "timestamp": "2026-10-02T12:30:45+03:00",
        "level": "DEBUG",
        "source": "hello",
        "message": "Hello World!"
    }
    event1 = Event.create_event(data)
    print(event1)