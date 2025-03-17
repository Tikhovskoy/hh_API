import requests
from config import (SUPERJOB_API_KEY, SUPERJOB_API_BASE_URL, TOWN_MOSCOW_ID,
                    CATALOGUE_PROGRAMMING, SUPERJOB_DEFAULT_COUNT)
import logging
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)

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
    :return: Словарь с данными от API.
    :raises: requests.RequestException, если запрос не удался.
    """
    headers = {"X-Api-App-Id": SUPERJOB_API_KEY}
    params = {
        "town": town,
        "keyword": keyword,
        "catalogues": catalogues,
        "count": count,
        "page": page
    }
    response = session.get(SUPERJOB_API_BASE_URL, headers=headers, params=params, timeout=10)
    response.raise_for_status()
    return response.json()

def get_all_superjob_vacancies(keyword: str, town: int = TOWN_MOSCOW_ID,
                               catalogues: int = CATALOGUE_PROGRAMMING) -> List[Dict[str, Any]]:
    first_response = get_superjob_vacancies(keyword, town=town, catalogues=catalogues,
                                            count=SUPERJOB_DEFAULT_COUNT, page=0)
    vacancies = first_response.get("objects", [])
    total_vacancies = first_response.get("total", 0)
    pages = (total_vacancies // SUPERJOB_DEFAULT_COUNT) + (1 if total_vacancies % SUPERJOB_DEFAULT_COUNT else 0)
    logger.info(f"SuperJob API: '{keyword}' – найдено страниц: {pages}")
    for current_page in range(1, pages):
        page_response = get_superjob_vacancies(keyword, town=town, catalogues=catalogues,
                                               count=SUPERJOB_DEFAULT_COUNT, page=current_page)
        logger.info(f"SuperJob API: Загружаем страницу {current_page} из {pages}")
        vacancies.extend(page_response.get("objects", []))
    return vacancies

def main():
    logger.info("Получение вакансий с SuperJob API")
    try:
        vacancies = get_superjob_vacancies("Программист Python")
        logger.info("Полученные вакансии: %s", vacancies)
    except Exception as error:
        logger.error("Ошибка при получении вакансий: %s", error)

if __name__ == '__main__':
    main()
