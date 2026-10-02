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
        super().__init__("Хз пока")
        # TODO: Написать сообщение ошибки

class InvalidTimestampError(StreamStatsError):
    """Ошибка неверной временной метки
    """
    def __init__(self):
        super().__init__("В файле неверная временная метка")

class InvalidLevelError(StreamStatsError):
    """Ошибка неизвестного уровня лога
    """
    
    def __init__(self):
        super().__init__("В файле неизвестный уровень лога")

class CliConfigurationError(StreamStatsError):
    """Ошибка конфигурации CLI
    """
    def __init__(self):
        super().__init__("Неверная конфигурация CLI")