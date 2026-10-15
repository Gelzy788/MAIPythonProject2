from streamstats.errors import CliConfigurationError

from pprint import pprint
from json import dump
from pathlib import Path


class ResultCreator:
    """Выводит результаты в нужном формате: json или CLI
    """
    
    @staticmethod
    def validate_output(file_dir: str=None) -> None:
        if not file_dir:
            return
        
        output_path = Path(file_dir)
        
        if output_path.suffix != ".json":
            raise CliConfigurationError(f"Файл отчёта {file_dir} должен иметь расширение .json")
        
        if output_path.exists():
            raise CliConfigurationError(f"Файл {file_dir} уже существует")
        
        if not output_path.parent.is_dir():
            raise CliConfigurationError(f"Каталог {output_path.parent} для файла отчёта не существует")
    
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
        except OSError as err:
            raise CliConfigurationError(f"Не удалось записать отчёт в {file_dir}: {err.strerror}")
            
    def _print_result(result: dict):
        pprint(result, sort_dicts=False)
