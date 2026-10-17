from streamstats.models import Level

# Множество во всеми уровнями логов, которые считаются ошибкой
ERROR_LEVELS = {Level.CRITICAL, Level.ERROR}
# Топ сколько нужно вывести источников ошибок
HOW_MUCH_TOP_SOURCES = 5
SUPPORTED_FORMATS = {"csv", "jsonl"}
