from dataclasses import dataclass, field
from datetime import datetime
from streamstats.models import Level
from streamstats.constants import ERROR_LEVELS

class StatsCounter:
    def __init__(self):
        self.count_of_logs: int = 0
        self.count_of_levels: dict = {level: 0 for level in Level}
        self.source_event_count: dict = {}
        self.source_error_count: dict = {}
        self.first_timestamp: datetime = None
        self.last_timestamp: datetime = None
    
    def get_top_5_sources(self) -> list[str]:
        # TODO: сделать возврат топ-5 источников
        return {"Здесь будет топ 5": "Источников",
                "И еще что-то": "Наверное"}
    
    def add_log(self, log: Event) -> None:
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
    
    def get_stats(self) -> dict:
        return {"count_of_logs": self.count_of_logs,
                "count_of_levels": self.count_of_levels,
                "source_event_count": self.source_event_count,
                "source_error_count": self.get_top_5_sources(),
                "first_timestamp": self.first_timestamp.isoformat() if self.first_timestamp else None,
                "last_timestamp": self.last_timestamp.isoformat() if self.last_timestamp else None,
                }