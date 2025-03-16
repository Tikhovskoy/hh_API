import requests
from requests.exceptions import RequestException
from config import HH_API_BASE_URL, HH_DEFAULT_PER_PAGE
import logging
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)
# Настройка логирования (настройте в основном скрипте для консистентности)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

# Сессионный объект для переиспользования соединений
session = requests.Session()


def get_hh_vacancies(query: str, area: int = 1, per_page: int = HH_DEFAULT_PER_PAGE,
                     page: int = 0, date_from: Optional[str] = None) -> Dict[str, Any]:
    """
    Выполняет запрос к API HeadHunter для получения вакансий по заданному запросу.

    :param query: Строка запроса (например, "Программист Python").
    :param area: Код региона (по умолчанию 1).
    :param per_page: Количество вакансий на странице.
    :param page: Номер страницы запроса.
    :param date_from: Опциональная дата для фильтрации вакансий.
    :return: Словарь с данными от API или пустой словарь при ошибке.
    """
    params = {
        "text": query,
        "area": area,
        "per_page": per_page,
        "page": page
    }
    if date_from:
        params["date_from"] = date_from
    try:
        response = session.get(HH_API_BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        logger.error(f"Ошибка при запросе HH API (страница {page}): {e}")
        return {}


def get_all_hh_vacancies(query: str, area: int = 1, date_from: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Загружает все вакансии по заданному запросу с использованием пагинации.

    :param query: Строка запроса (например, "Программист Python").
    :param area: Код региона.
    :param date_from: Опциональная дата для фильтрации вакансий.
    :return: Список вакансий (каждая вакансия – словарь).
    """
    data = get_hh_vacancies(query, area=area, per_page=HH_DEFAULT_PER_PAGE, page=0, date_from=date_from)
    vacancies = data.get("items", [])
    total_pages = data.get("pages", 0)
    logger.info(f"HH API: '{query}' – найдено страниц: {total_pages}")
    for current_page in range(1, total_pages):
        data_page = get_hh_vacancies(query, area=area, per_page=HH_DEFAULT_PER_PAGE, page=current_page,
                                     date_from=date_from)
        logger.info(f"HH API: Загружаем страницу {current_page} из {total_pages}")
        vacancies.extend(data_page.get("items", []))
    return vacancies
