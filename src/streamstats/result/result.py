from pprint import pprint

class ResultCreator:
    """Выводит результаты в нужном формате: json или CLI
    """
    
    @staticmethod
    def result_create(
        result: dict, is_file_need: bool=False, file_name: str=None):
        if is_file_need:
            ResultCreator._write_result_in_file(result, file_name)
        
        ResultCreator._print_result(result)
    
    def _write_result_in_file(result: dict, file_name: str):
        pass
    
    def _print_result(result: dict):
        #TODO: Переделать print тк, чтобы он не менял очередность в топ-5
        pprint(result)
