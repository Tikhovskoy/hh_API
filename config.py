import os
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env.
load_dotenv()

# Ключи и URL для API
SUPERJOB_API_KEY: str = os.getenv("SUPERJOB_API_KEY")
HH_API_BASE_URL: str = "https://api.hh.ru/vacancies"
SUPERJOB_API_BASE_URL: str = "https://api.superjob.ru/2.0/vacancies/"

# Общие настройки
TOWN_MOSCOW_ID: int = 4            # Москва
CATALOGUE_PROGRAMMING: int = 48     # Разработка, программирование

# Параметры по умолчанию для запросов
HH_DEFAULT_PER_PAGE: int = 100      # вакансий на странице для HH
SUPERJOB_DEFAULT_COUNT: int = 100   # вакансий на странице для SuperJob
