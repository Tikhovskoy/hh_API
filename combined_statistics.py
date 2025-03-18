import os
import logging
from hh_api import get_all_hh_vacancies
from superjob_api import get_all_superjob_vacancies
from salary import predict_rub_salary_hh, predict_rub_salary_sj
from statistics_utils import calculate_statistics, print_statistics_table
from config import CONFIG

logger = logging.getLogger(__name__)

def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    
    api_key = CONFIG["SUPERJOB_API_KEY"]
    if not api_key:
        raise ValueError("Ошибка: SUPERJOB_API_KEY не найден в конфиге")

    languages = CONFIG["DEFAULT_LANGUAGES"]

    hh_statistics = {}
    sj_statistics = {}

    for lang in languages:
        hh_vacancies, hh_vacancies_found = get_all_hh_vacancies(f"Программист {lang}", area=CONFIG["HH_DEFAULT_AREA"])
        sj_vacancies, sj_vacancies_found = get_all_superjob_vacancies(api_key, f"Программист {lang}", CONFIG["SUPERJOB_DEFAULT_CITY"], CONFIG["CATALOGUE_PROGRAMMING"])

        hh_statistics[lang] = calculate_statistics(hh_vacancies, predict_rub_salary_hh, hh_vacancies_found)
        sj_statistics[lang] = calculate_statistics(sj_vacancies, predict_rub_salary_sj, sj_vacancies_found)

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