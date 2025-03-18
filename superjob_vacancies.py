import logging
import os
from superjob_api import get_all_superjob_vacancies
from salary import predict_rub_salary_sj
from statistics_utils import calculate_statistics, print_statistics_table
import config
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

def get_language_statistics_sj(api_key: str, language: str, town: int, catalogues: int) -> Dict[str, int]:
    """
    Получает статистику вакансий для заданного языка с SuperJob.
    """
    query: str = f"Программист {language}"
    vacancies, vacancies_found = get_all_superjob_vacancies(api_key, query, town=town, catalogues=catalogues)
    return calculate_statistics(vacancies, predict_rub_salary_sj, vacancies_found)

def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    config_data = config.get_config()
    api_key = config_data["SUPERJOB_API_KEY"]
    if not api_key:
        raise ValueError("Ошибка: SUPERJOB_API_KEY не найден в конфиге")

    languages = config_data["DEFAULT_LANGUAGES"]
    stats = {
        lang: get_language_statistics_sj(
            api_key, lang, config_data["SUPERJOB_DEFAULT_CITY"], config_data["CATALOGUE_PROGRAMMING"]
        )
        for lang in languages
    }
    
    print_statistics_table(stats, title="SuperJob Moscow")

if __name__ == "__main__":
    main()
