# Статистика вакансий программистов

Проект собирает вакансии программистов с сайтов HeadHunter и SuperJob, рассчитывает среднюю зарплату и показывает результаты в виде удобных таблиц.

## Возможности

- Сбор вакансий с сайтов HeadHunter и SuperJob.
- Расчёт средней зарплаты по диапазонам, указанным в вакансиях.
- Поддержка пагинации (получение всех доступных вакансий).
- Чёткий и удобный вывод результатов в таблицах.

## Скрипты и их назначение

| Скрипт                      | Описание                                                    |
|-----------------------------|-------------------------------------------------------------|
| `combined_statistics.py`    | Сбор и вывод объединённой статистики по вакансиям с обоих сайтов. |
| `hh_api.py`                 | Запросы к API HeadHunter для получения данных о вакансиях. |
| `superjob_api.py`           | Запросы к API SuperJob для получения данных о вакансиях.   |
| `salary.py`                 | Функции расчёта ожидаемой зарплаты.                        |
| `statistics_utils.py`       | Вспомогательные функции для расчёта и отображения статистики. |
| `config.py`                 | Конфигурационный файл с параметрами API и настройками.     |

## Описание файлов проекта

- `.gitignore` — файл исключений для Git.
- `README.md` — описание проекта, инструкция по установке и использованию.
- `requirements.txt` — список зависимостей проекта.
- `config.py` — конфигурационные настройки (API-ключи, базовые URL и параметры запросов).
- `hh_api.py` — функции для работы с API HeadHunter.
- `superjob_api.py` — функции для работы с API SuperJob.
- `salary.py` — функции расчёта средней зарплаты.
- `statistics_utils.py` — вспомогательные функции для расчёта и отображения статистики.
- `hh_vacancies.py` — скрипт получения вакансий с HeadHunter.
- `superjob_vacancies.py` — скрипт получения вакансий с SuperJob.
- `combined_statistics.py` — скрипт сбора общей статистики по обоим сайтам.

## Стек технологий

- Python 3.8+
- python-dotenv==1.0.1
- requests==2.32.3
- terminaltables==3.1.10

## Установка

### 1. Клонирование проекта

```bash
git clone https://github.com/your_username/your_repo.git
cd your_repo
```

### 2. Настройка виртуального окружения

Создай и активируй виртуальное окружение:

- Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

- Linux/MacOS:
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Конфигурация API

Создай файл `.env` и добавь туда свой API-ключ от SuperJob:

```
SUPERJOB_API_KEY=твой_superjob_api_key
```

API-ключ можно получить [здесь](https://api.superjob.ru/register).

## Использование

Запусти основной скрипт для получения объединённой статистики:

```bash
python combined_statistics.py
```

Или отдельно для каждого сайта:

- **HeadHunter:**

```bash
python hh_vacancies.py
```

- **SuperJob:**

```bash
python superjob_vacancies.py
```

## Структура проекта

```
.
├── .gitignore
├── README.md
├── requirements.txt
├── config.py
├── hh_api.py
├── superjob_api.py
├── salary.py
├── statistics_utils.py
├── hh_vacancies.py
├── superjob_vacancies.py
└── combined_statistics.py
```

## Примеры запуска

Запуск сбора данных по конкретному языку программирования:

```bash
python hh_vacancies.py --language Python
```

```bash
python superjob_vacancies.py --language JavaScript
```

