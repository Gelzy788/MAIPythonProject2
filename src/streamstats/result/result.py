from pprint import pprint

class ResultCreator:
    """Выводит результаты в нужном формате: json или CLI
    """
    
    @staticmethod
    def result_create(
        result: dict, file_name: str=None):
        if file_name:
            ResultCreator._write_result_in_file(result, file_name)
        
        ResultCreator._print_result(result)
    
    def _write_result_in_file(result: dict, file_name: str):
        print("СОЗДАТЬ ФАЙЛ")
    
    def _print_result(result: dict):
        #TODO: Переделать print тк, чтобы он не менял очередность в топ-5
        pprint(result)
