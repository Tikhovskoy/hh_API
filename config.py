import os
from dotenv import load_dotenv

def get_config():
    """
    Загружает переменные окружения из .env и возвращает их в виде словаря.
    """
    load_dotenv()

    config = {
        "SUPERJOB_API_KEY": os.getenv("SUPERJOB_API_KEY"),
        "SUPERJOB_API_BASE_URL": "https://api.superjob.ru/2.0/vacancies/",
        "HH_API_BASE_URL": "https://api.hh.ru/vacancies",
        "TOWN_MOSCOW_ID": 4,
        "CATALOGUE_PROGRAMMING": 48,
        "HH_DEFAULT_PER_PAGE": 100,
        "SUPERJOB_DEFAULT_COUNT": 100,
        "HH_DEFAULT_AREA": 1,
    }

    if not config["SUPERJOB_API_KEY"]:
        raise ValueError("Ошибка: SUPERJOB_API_KEY не задан в переменных окружения")

    return config
