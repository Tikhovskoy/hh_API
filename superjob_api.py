import requests
from requests.exceptions import RequestException
from config import (SUPERJOB_API_KEY, SUPERJOB_API_BASE_URL, TOWN_MOSCOW_ID,
                    CATALOGUE_PROGRAMMING, SUPERJOB_DEFAULT_COUNT)
import logging
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

# Сессионный объект для переиспользования соединений
session = requests.Session()


def get_superjob_vacancies(keyword: str, town: int = TOWN_MOSCOW_ID, catalogues: int = CATALOGUE_PROGRAMMING,
                           count: int = SUPERJOB_DEFAULT_COUNT, page: int = 0) -> Dict[str, Any]:
    """
    Выполняет запрос к API SuperJob для получения вакансий по заданному запросу.

    :param keyword: Строка запроса (например, "Программист Python").
    :param town: Код города.
    :param catalogues: Код каталога вакансий.
    :param count: Количество вакансий на странице.
    :param page: Номер страницы запроса.
    :return: Словарь с данными от API или пустой словарь при ошибке.
    """
    headers = {"X-Api-App-Id": SUPERJOB_API_KEY}
    params = {
        "town": town,
        "keyword": keyword,
        "catalogues": catalogues,
        "count": count,
        "page": page
    }
    try:
        response = session.get(SUPERJOB_API_BASE_URL, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        logger.error(f"Ошибка при запросе SuperJob API (страница {page}): {e}")
        return {}


def get_all_superjob_vacancies(keyword: str, town: int = TOWN_MOSCOW_ID,
                               catalogues: int = CATALOGUE_PROGRAMMING) -> List[Dict[str, Any]]:
    """
    Загружает все вакансии по заданному запросу с использованием пагинации.

    :param keyword: Строка запроса (например, "Программист Python").
    :param town: Код города.
    :param catalogues: Код каталога вакансий.
    :return: Список вакансий (каждая вакансия – словарь).
    """
    data = get_superjob_vacancies(keyword, town=town, catalogues=catalogues,
                                  count=SUPERJOB_DEFAULT_COUNT, page=0)
    vacancies = data.get("objects", [])
    total_vacancies = data.get("total", 0)
    # Вычисляем общее количество страниц
    pages = (total_vacancies // SUPERJOB_DEFAULT_COUNT) + (1 if total_vacancies % SUPERJOB_DEFAULT_COUNT else 0)
    logger.info(f"SuperJob API: '{keyword}' – найдено страниц: {pages}")
    for current_page in range(1, pages):
        data_page = get_superjob_vacancies(keyword, town=town, catalogues=catalogues,
                                           count=SUPERJOB_DEFAULT_COUNT, page=current_page)
        logger.info(f"SuperJob API: Загружаем страницу {current_page} из {pages}")
        vacancies.extend(data_page.get("objects", []))
    return vacancies
