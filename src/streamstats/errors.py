class StreamStatsError(Exception):
    """Родительская ошбика для всей программы
    """
    pass

class UnsupportedFormatError(StreamStatsError):
    """Ошибка неподдерживаемого формата файла логов
    """
    def __init__(self):
        super().__init__("На вход подан файл с неподдерживаемым форматом")

class InvalidEventError(StreamStatsError):
    """Ошибка неверного события
    """
    def __init__(self):
        super().__init__("Лог записан в неправильном формате")
        # TODO: Написать сообщение ошибки

class InvalidTimestampError(InvalidEventError):
    """Ошибка неверной временной метки
    """
    def __init__(self):
        super().__init__("В файле неверная временная метка")

class CliConfigurationError(StreamStatsError):
    """Ошибка конфигурации CLI
    """
    def __init__(self, messege: str=""):
        super().__init__("Неверная конфигурация CLI:", messege)