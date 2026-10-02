from models import Level

# Множество во всеми уровнями логов, которые считаются ошибкой
ERROR_LEVELS = set(Level.CRITICAL, Level.ERROR) # NOTE: Берем set, т.к. в нем быстрый in