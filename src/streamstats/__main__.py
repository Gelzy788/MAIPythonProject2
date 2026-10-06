from streamstats.analysis.stats_counter import *
from streamstats.parsing.event_list import *
from streamstats.parsing.file_parsers import *
from streamstats.models import *
from streamstats.result.result import *

if __name__ == "__main__":
    stat = StatsCounter()
    for i in EventList(["test_csv_files/test_files/valid.jsonl"], "jsonl", False):
        stat.add_log(i)

    ResultCreator.result_create(result=stat.to_dict())
    # print(stat.count_of_levels[Level.CRITICAL])
    # print(stat.count_of_logs)
    # print(stat.source_error_count)
    # print(stat.source_event_count)
    # print(stat.first_timestamp)
    # print(stat.last_timestamp)