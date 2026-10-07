from streamstats.models import Level

# Множество во всеми уровнями логов, которые считаются ошибкой
ERROR_LEVELS = {Level.CRITICAL, Level.ERROR} # NOTE: Берем set, т.к. в нем быстрый in
# Топ сколько нужно вывести источников ошибок
HOW_MUCH_TOP_SOURCES = 5