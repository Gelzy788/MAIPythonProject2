class StreamStatsError(Exception):
    """Родительская ошбика для всей программы
    """

class UnsupportedFormatError(StreamStatsError):
    """Ошибка неподдерживаемого формата файла логов
    """
    def __init__(self, message: str = "На вход подан файл с неподдерживаемым форматом"):
        super().__init__(message)

class InvalidEventError(StreamStatsError):
    """Ошибка неверного события
    """
    def __init__(self, message: str = "Лог записан в неправильном формате"):
        super().__init__(message)

class InvalidTimestampError(InvalidEventError):
    """Ошибка неверной временной метки
    """
    def __init__(self, message: str = "В файле неверная временная метка"):
        super().__init__(message)

class CliConfigurationError(StreamStatsError):
    """Ошибка конфигурации CLI
    """
    def __init__(self, message: str = ""):
        super().__init__(f"Неверная конфигурация CLI: {message}")
