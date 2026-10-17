# 📊 streamstats

**Потоковый анализатор логов в форматах CSV и JSONL с JSON-отчётом**

---

## ✨ Возможности

- **Потоковое чтение** — CSV и JSONL читаются построчно, файл никогда не загружается в память целиком.
- **Несколько файлов за раз** — статистика объединяется, форматы можно смешивать.
- **Автоопределение разделителя** CSV.
- **Мягкий режим** — ошибочные строки можно пропускать, их число попадёт в отчёт.
- **JSON-отчёт** со статистикой по уровням, источникам и временным меткам.

---

## 🛠 Установка

```bash
git clone https://github.com/Gelzy788/MAIPythonProject1.git
cd MAIPythonProject1
```

<table>
<tr>
<th>🐧 Linux / 🍎 macOS</th>
<th>🪟 Windows</th>
</tr>
<tr>
<td>

```bash
python3 -m venv venv
source venv/bin/activate
pip install .
```

</td>
<td>

```bash
python -m venv venv
venv\Scripts\activate
pip install .
```

</td>
</tr>
</table>

---

### Синтаксис

```text
python -m streamstats analyze INPUT [INPUT ...] --format FORMAT [FORMAT ...]
                                [--output REPORT.json] [--skip-invalid]
```

| Аргумент | Обязательный | Описание |
|:---|:---:|:---|
| `INPUT` | ✅ | Один или несколько входных файлов. |
| `--format` | ✅ | `csv` или `jsonl` — по одному на каждый файл, в том же порядке. |
| `--output` | — | Путь к файлу отчёта (расширение `.json`). |
| `--skip-invalid` | — | Пропускать ошибочные строки вместо остановки. |

---

## 📝 Формат событий

Каждая строка лога — это одно событие со следующими полями:

| Поле | Требования |
|:---|:---|
| `timestamp` | ISO 8601, например `2026-10-01T10:00:00+03:00`. Часовой пояс необязателен. |
| `level` | `DEBUG`, `INFO`, `WARNING`, `ERROR` или `CRITICAL`. Регистр не важен. |
| `source` | Непустая строка. |
| `message` | Строка, может быть пустой. |

<details>
<summary><b>Пример CSV</b></summary>

```csv
timestamp,level,source,message
2026-10-01T10:00:00+03:00,INFO,api,Server started
2026-10-01T10:00:05+03:00,ERROR,db,Connection refused
```

</details>

<details>
<summary><b>Пример JSONL</b></summary>

```json
{"timestamp": "2026-10-01T10:00:00+03:00", "level": "INFO", "source": "api", "message": "Server started"}
{"timestamp": "2026-10-01T10:00:05+03:00", "level": "error", "source": "db", "message": "Connection refused"}
```

</details>

---

## 📈 Отчёт

Отчёт всегда выводится в консоль, а с флагом `--output` — дополнительно сохраняется в JSON-файл. При анализе нескольких файлов статистика объединяется.

Отчёт содержит:

| Показатель | Описание |
|:---|:---|
| Всего событий | Общее число корректных событий |
| По уровням | Число событий каждого уровня |
| По источникам | Число событий каждого источника |
| Топ-5 источников ошибок | Источники с наибольшим числом `ERROR` и `CRITICAL` |
| Временной диапазон | Первая и последняя временная метка |
| Пропущено строк | Число строк, отброшенных в режиме `--skip-invalid` |

---

## 🏗 Архитектура

### Поток данных

```text
__main__ ──► EventList ──► Парсер ──► Event.create_event ──► StatsCounter ──► ResultCreator
  (CLI)    (открывает    (отдаёт      (валидирует          (считает        (выводит
            файлы)       строки)       событие)             статистику)      отчёт)
```

На каждом шаге обрабатывается **одна строка**, поэтому потребление памяти не зависит от размера файла.

### Структура проекта

```text
src/streamstats/
├── __main__.py                 # CLI
├── models.py                   # событие и его валидация
├── errors.py                   # исключения
├── constants.py                # константы
├── parsing/
│   ├── file_parsers.py         # парсеры CSV и JSONL
│   └── event_list.py           # обход файлов и режимы ошибок
├── analysis/
│   └── stats_counter.py        # подсчёт статистики
└── result/
    └── result.py               # вывод отчёта
tests/                          # тесты и тестовые данные
```

### Иерархия исключений

```text
StreamStatsError
├── UnsupportedFormatError      # неподдерживаемый формат
├── InvalidEventError           # неверное событие
│   └── InvalidTimestampError   # неверная временная метка
└── CliConfigurationError       # ошибка конфигурации CLI
```