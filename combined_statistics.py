import os
import logging
from hh_api import get_all_hh_vacancies
from superjob_api import get_all_superjob_vacancies
from salary import predict_rub_salary_hh, predict_rub_salary_sj
import config
from statistics_utils import calculate_statistics, print_statistics_table
from typing import Optional, Dict

logger = logging.getLogger(__name__)

def get_language_statistics_hh(language: str, area: int = 1, date_from: Optional[str] = None) -> Dict[str, int]:
    query = f"Программист {language}"
    vacancies_list, vacancies_found = get_all_hh_vacancies(query, area=area, date_from=date_from)
    return calculate_statistics(vacancies_list, predict_rub_salary_hh, vacancies_found)

def get_language_statistics_sj(api_key: str, language: str, town: int, catalogues: int) -> Dict[str, int]:
    query = f"Программист {language}"
    vacancies_list, vacancies_found = get_all_superjob_vacancies(api_key, query, town=town, catalogues=catalogues)
    return calculate_statistics(vacancies_list, predict_rub_salary_sj, vacancies_found)

def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    
    config_data = config.get_config()
    api_key = config_data.get("SUPERJOB_API_KEY")
    if not api_key:
        raise ValueError("Ошибка: SUPERJOB_API_KEY не найден в конфиге")

    languages = ["Python", "C", "C#", "C++", "Java", "JS", "Ruby", "Go", "1С"]
    hh_statistics = {lang: get_language_statistics_hh(lang, area=1) for lang in languages}
    sj_statistics = {
        lang: get_language_statistics_sj(api_key, lang, config_data["TOWN_MOSCOW_ID"], config_data["CATALOGUE_PROGRAMMING"])
        for lang in languages
    }

    print_statistics_table(
        hh_statistics,
        title="HeadHunter Moscow",
        headers=["Язык программирования", "Найдено вакансий", "Обработано вакансий", "Средняя зарплата"]
    )
    logger.info("\n")
    print_statistics_table(
        sj_statistics,
        title="SuperJob Moscow",
        headers=["Язык программирования", "Вакансий найдено", "Вакансий обработано", "Средняя зарплата"]
    )

if __name__ == "__main__":
    main()
