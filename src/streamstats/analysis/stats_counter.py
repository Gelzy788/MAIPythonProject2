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
        source_error_count_printable = dict(sorted(self.source_error_count.items(), key=lambda a: a[1]))
        
        return self.source_error_count
    
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
        count_of_levels_printable = {}
        for key, value in self.count_of_levels.items():
            count_of_levels_printable[key.value] = value
            
        return {"count_of_logs": self.count_of_logs,
                "count_of_levels": count_of_levels_printable,
                "source_event_count": self.source_event_count,
                "source_error_count": self.get_top_5_sources(),
                "first_timestamp": self.first_timestamp.isoformat() if self.first_timestamp else None,
                "last_timestamp": self.last_timestamp.isoformat() if self.last_timestamp else None,
                }