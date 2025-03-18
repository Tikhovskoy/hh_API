import requests
import logging
from typing import Optional, Dict, Any, List, Tuple
from config import CONFIG

logger = logging.getLogger(__name__)
session = requests.Session()

def get_superjob_vacancies(api_key: str, keyword: str, town: Optional[int] = None,
                            catalogues: Optional[int] = None, count: Optional[int] = None, page: int = 0) -> Dict[str, Any]:
    """
    Выполняет запрос к API SuperJob для получения вакансий по заданному запросу.
    """
    if town is None:
        town = CONFIG["SUPERJOB_DEFAULT_CITY"]
    if catalogues is None:
        catalogues = CONFIG["CATALOGUE_PROGRAMMING"]
    if count is None:
        count = CONFIG["SUPERJOB_DEFAULT_COUNT"]

    headers = {"X-Api-App-Id": api_key}
    params = {
        "town": town,
        "keyword": keyword,
        "catalogues": catalogues,
        "count": count,
        "page": page
    }

    response = session.get(CONFIG["SUPERJOB_API_BASE_URL"], headers=headers, params=params, timeout=10)
    response.raise_for_status()
    return response.json()

def get_all_superjob_vacancies(api_key: str, keyword: str, town: Optional[int] = None, catalogues: Optional[int] = None) -> Tuple[List[Dict[str, Any]], int]:
    """
    Загружает все вакансии по заданному запросу с использованием пагинации.
    """
    if town is None:
        town = CONFIG["SUPERJOB_DEFAULT_CITY"]
    if catalogues is None:
        catalogues = CONFIG["CATALOGUE_PROGRAMMING"]

    first_response = get_superjob_vacancies(api_key, keyword, town=town, catalogues=catalogues, count=CONFIG["SUPERJOB_DEFAULT_COUNT"], page=0)
    vacancies = first_response.get("objects", [])
    vacancies_found = first_response.get("total", 0)
    pages = (vacancies_found // CONFIG["SUPERJOB_DEFAULT_COUNT"]) + (1 if vacancies_found % CONFIG["SUPERJOB_DEFAULT_COUNT"] else 0)

    logger.info(f"SuperJob API: '{keyword}' – найдено страниц: {pages}")

    for current_page in range(1, pages):
        page_response = get_superjob_vacancies(api_key, keyword, town=town, catalogues=catalogues, count=CONFIG["SUPERJOB_DEFAULT_COUNT"], page=current_page)
        logger.info(f"SuperJob API: Загружаем страницу {current_page} из {pages}")
        vacancies.extend(page_response.get("objects", []))

    return vacancies, vacancies_found

def main():
    """
    Основная функция для получения вакансий с SuperJob API.
    """
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    api_key = CONFIG["SUPERJOB_API_KEY"]
    if not api_key:
        raise ValueError("Ошибка: SUPERJOB_API_KEY не найден в конфиге")

    logger.info("Получение вакансий с SuperJob API")
    try:
        vacancies = get_superjob_vacancies(api_key, "Программист Python")
        logger.info("Полученные вакансии: %s", vacancies)
    except Exception as error:
        logger.error("Ошибка при получении вакансий: %s", error)

if __name__ == '__main__':
    main()
