from streamstats.errors import CliConfigurationError

from pprint import pprint
from json import dump
from pathlib import Path


class ResultCreator:
    """Выводит результаты в нужном формате: json или CLI
    """
    
    @staticmethod
    def result_create(
        result: dict, file_dir: str=None):
        if file_dir:
            ResultCreator._write_result_in_file(result, file_dir)
        
        ResultCreator._print_result(result)
    
    def _write_result_in_file(result: dict, file_dir: str):
        try:
            with open(file_dir, "x", encoding="utf-8") as file:
                dump(result, file, ensure_ascii=False, indent=4)
        except FileExistsError as err:
            raise CliConfigurationError(f"Файл {file_dir} уже существует")
            
    def _print_result(result: dict):
        pprint(result, sort_dicts=False)
