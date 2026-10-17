# streamstats

**Потоковый анализатор логов в форматах CSV и JSONL с JSON-отчётом.**

## Возможности

- Чтение CSV и JSONL построчно, без загрузки файла в память целиком.
- Объединение статистики нескольких файлов, в том числе разных форматов, за один запуск.
- Автоопределение разделителя CSV.
- Валидация каждого события с указанием файла и строки при ошибке.
- Режим пропуска ошибочных строк с подсчётом пропусков в отчёте.
- JSON-отчёт со статистикой по уровням, источникам и временным меткам.

## Использование
```text
python -m streamstats analyze INPUT [INPUT ...] --format FORMAT [FORMAT ...] [--output REPORT.json] [--skip-invalid]
```
| Аргумент | Обязательный | Описание |
|---|---|---|
| `INPUT` | да | Один или несколько входных файлов. |
| `--format` | да | `csv` или `jsonl`, по одному на файл, в том же порядке. |
| `--output` | нет | Путь к файлу отчёта с расширением `.json`. |
| `--skip-invalid` | нет | Пропускать ошибочные строки. |

## Формат событий
| Поле | Требования |
|---|---|
| `timestamp` | ISO 8601, например `2026-10-01T10:00:00+03:00`. Часовой пояс необязателен. |
| `level` | `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`. Регистр не важен. |
| `source` | Непустая строка. |
| `message` | Строка, может быть пустой. |

## Отчёт

Отчёт выводится в консоль, а при `--output` дополнительно сохраняется в JSON-файл. Статистика нескольких файлов объединяется.

В отчёте:

- общее число событий;
- число событий по уровням;
- число событий по источникам;
- топ-5 источников ошибок `ERROR` и `CRITICAL`;
- первая и последняя временная метка;
- число пропущенных строк.

## Структура проекта

```text
src/streamstats/
  __main__.py               CLI
  models.py                 событие и его валидация
  errors.py                 исключения
  constants.py              константы
  parsing/file_parsers.py   парсеры CSV и JSONL
  parsing/event_list.py     обход файлов и режимы ошибок
  analysis/stats_counter.py подсчёт статистики
  result/result.py          вывод отчёта
tests/                      тесты и тестовые данные
```
`__main__` → `EventList` открывает файлы → парсер построчно отдаёт данные → `Event.create_event` проверяет их → `StatsCounter` считает статистику → `ResultCreator` выводит отчёт. На каждом шаге обрабатывается одна строка, поэтому память не зависит от размера файла.

### Ошибки

```text
StreamStatsError
├── UnsupportedFormatError    неподдерживаемый формат
├── InvalidEventError         неверное событие
│   └── InvalidTimestampError неверная временная метка
└── CliConfigurationError     ошибка конфигурации CLI
```

## 🛠 Установка

### Клонирование
```bash
git clone https://github.com/Gelzy788/MAIPythonProject1.git
cd MAIPythonProject1
```

### 🐧 Linux / 🍎 macOS
```bash
python3 -m venv venv
source venv/bin/activate
pip install .
```

### 🪟 Windows
```bash
python -m venv venv
venv\Scripts\activate
pip install .
```