import requests
import logging
import math
from typing import Dict, Any, List, Tuple
import config

logger = logging.getLogger(__name__)
session = requests.Session()

def get_superjob_vacancies(api_key: str, keyword: str,
                            town: int = config.SUPERJOB_DEFAULT_CITY,
                            catalogues: int = config.CATALOGUE_PROGRAMMING,
                            count: int = config.SUPERJOB_DEFAULT_COUNT,
                            page: int = 0
                            ) -> Dict[str, Any]:
    """
    Выполняет запрос к API SuperJob для получения вакансий по заданному запросу.

    :param api_key: API-ключ SuperJob.
    :param keyword: Поисковый запрос (например, "Программист Python").
    :param town: Код города (по умолчанию Москва).
    :param catalogues: Код каталога профессий (по умолчанию "Программирование").
    :param count: Количество вакансий на странице (по умолчанию 100).
    :param page: Номер страницы (по умолчанию 0).
    :return: JSON-ответ от API.
    :raises requests.RequestException: Если запрос не удался.
    """
    headers = {"X-Api-App-Id": api_key}
    params = {
        "town": town,
        "keyword": keyword,
        "catalogues": catalogues,
        "count": count,
        "page": page
    }

    response = session.get(config.SUPERJOB_API_BASE_URL, headers=headers, params=params, timeout=10)
    response.raise_for_status()
    return response.json()

def get_all_superjob_vacancies(api_key: str, keyword: str,
                                town: int = config.SUPERJOB_DEFAULT_CITY,
                                catalogues: int = config.CATALOGUE_PROGRAMMING,
                                count: int = config.SUPERJOB_DEFAULT_COUNT
                                ) -> Tuple[List[Dict[str, Any]], int]:
    """
    Загружает все вакансии по заданному запросу с использованием пагинации.

    :param api_key: API-ключ SuperJob.
    :param keyword: Поисковый запрос (например, "Программист Python").
    :param town: Код города (по умолчанию Москва).
    :param catalogues: Код каталога профессий (по умолчанию "Программирование").
    :return: Кортеж (список вакансий, общее количество найденных вакансий).
    """
    vacancies = []
    page = 0
    response = get_superjob_vacancies(api_key, keyword, town=town, catalogues=catalogues, count=count, page=page)
    vacancies.extend(response.get("objects", []))
    vacancies_found = response.get("total", 0)

    logger.info(f"SuperJob API: '{keyword}' – найдено вакансий: {vacancies_found}")

    while response.get("more"):
        page += 1
        response = get_superjob_vacancies(api_key, keyword, town=town, catalogues=catalogues, count=count, page=page)
        logger.info(f"SuperJob API: Загружаем страницу {page}")
        vacancies.extend(response.get("objects", []))

    return vacancies, vacancies_found
