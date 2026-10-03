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
    
    def get_top_5(self) -> list[str]:
        pass
    
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