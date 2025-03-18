import requests
import config
import logging
from typing import Optional, Dict, Any, List, Tuple

logger = logging.getLogger(__name__)
session = requests.Session()

def get_hh_vacancies(query: str, area: Optional[int] = None, per_page: Optional[int] = None,
                     page: int = 0, date_from: Optional[str] = None) -> Dict[str, Any]:
    """
    Выполняет запрос к API HeadHunter для получения вакансий по заданному запросу.
    
    :param query: Строка запроса (например, "Программист Python").
    :param area: Код региона (по умолчанию значение из config).
    :param per_page: Количество вакансий на странице (по умолчанию из config).
    :param page: Номер страницы запроса.
    :param date_from: Опциональная дата для фильтрации вакансий.
    :return: Словарь с данными от API.
    :raises: requests.RequestException, если запрос не удался.
    """
    config_data = config.get_config()
    
    if area is None:
        area = config_data["HH_DEFAULT_AREA"]
    if per_page is None:
        per_page = config_data["HH_DEFAULT_PER_PAGE"]

    request_params = {
        "text": query,
        "area": area,
        "per_page": per_page,
        "page": page
    }
    
    if date_from:
        request_params["date_from"] = date_from
    
    response = session.get(config_data["HH_API_BASE_URL"], params=request_params, timeout=10)
    response.raise_for_status()
    return response.json()

def get_all_hh_vacancies(query: str, area: Optional[int] = None, date_from: Optional[str] = None) -> Tuple[List[Dict[str, Any]], int]:
    """
    Загружает все вакансии по заданному запросу с использованием пагинации.
    
    :param query: Строка запроса (например, "Программист Python").
    :param area: Код региона (по умолчанию значение из config).
    :param date_from: Опциональная дата для фильтрации вакансий.
    :return: Кортеж: (список вакансий, общее количество найденных вакансий).
    """
    config_data = config.get_config()
    per_page = config_data["HH_DEFAULT_PER_PAGE"]

    if area is None:
        area = config_data["HH_DEFAULT_AREA"]

    first_page_response = get_hh_vacancies(query, area=area, per_page=per_page, page=0, date_from=date_from)
    vacancies = first_page_response.get("items", [])
    vacancies_found = first_page_response.get("found", 0)
    total_pages = first_page_response.get("pages", 0)

    logger.info(f"HH API: '{query}' – найдено страниц: {total_pages}")

    for current_page in range(1, total_pages):
        page_response = get_hh_vacancies(query, area=area, per_page=per_page, page=current_page, date_from=date_from)
        logger.info(f"HH API: Загружаем страницу {current_page} из {total_pages}")
        vacancies.extend(page_response.get("items", []))

    return vacancies, vacancies_found

def main():
    """
    Основная функция для получения данных о вакансиях.
    """
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    
    logger.info("Получение вакансий с HH API")
    
    try:
        vacancies_data = get_hh_vacancies("Программист Python")
        logger.info("Полученные вакансии: %s", vacancies_data)
    except Exception as error:
        logger.error("Ошибка при получении вакансий: %s", error)

if __name__ == '__main__':
    main()
