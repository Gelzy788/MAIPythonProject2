import argparse
import sys
from datetime import datetime
import logging
import os

from streamstats.analysis.stats_counter import *
from streamstats.parsing.event_list import *
from streamstats.parsing.file_parsers import *
from streamstats.models import *
from streamstats.result.result import *
from streamstats.errors import StreamStatsError
from streamstats.constants import SUPPORTED_FORMATS


def parse_args() -> argparse.Namespace:
    """Парсер CLI

        Читает аргументы, введенные в CLI пользователем и возвращае их
        
    Returns:
        args (argparse.Namespace): Аргументы, введенные пользователем в CLI
    """
    parser = argparse.ArgumentParser(
        prog="streamstats"
    )
    
    subparser = parser.add_subparsers(
        dest="command", required=True, title="команды", metavar="КОМАНДА"
    )
    
    sub_analyze = subparser.add_parser("analyze")
    
    sub_analyze.add_argument("input", nargs="+")
    sub_analyze.add_argument("--format", nargs="+", required=True, choices=sorted(SUPPORTED_FORMATS))
    sub_analyze.add_argument("--output", required=False)
    sub_analyze.add_argument("--skip-invalid", action='store_true')
    
    return parser.parse_args()

def start_program(args: argparse.Namespace):
    """Начинает выполнение программы
    
        Оркестриурет выполнение программы:
        Сначала запускает парсинг файла и сбор статистики
        Потом запускает вывод результатов в запрошенном формате

    Args:
        args (argparse.Namespace): Аргументы, введенные пользователем в CLI
    """
    ResultCreator.validate_output(args.output)
    
    stat = StatsCounter()
    for i in EventList(args.input, args.format, args.skip_invalid):
        stat.add_log(i)
    
    ResultCreator.result_create(stat.to_dict(), args.output)

def main():
    # Создание папки и файла с логами
    os.makedirs("logs", exist_ok=True)
    time_now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    logging.basicConfig(level=logging.INFO,
                        filename=f"logs/{time_now}_streamstats.log",
                        filemode="w",
                        format="%(asctime)s %(levelname)s %(message)s")
    
    try:
        start_program(parse_args())
    except StreamStatsError as err:
        print(str(err), file=sys.stderr)
        sys.exit(2)
    except Exception as err:
        print(str(err), file=sys.stderr)

if __name__ == "__main__":
    main()
    # python -m streamstats analyze /home/Gelzy/Documents/MAIPythonProject2/test_csv_files/test_files/valid.jsonl /home/Gelzy/Documents/MAIPythonProject2/test_csv_files/test_files/valid.csv --format jsonl csv --output ./usr/r.jsonl
