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

    hh_statistics = {
        lang: calculate_statistics(
            get_all_hh_vacancies(f"Программист {lang}", area=CONFIG["HH_DEFAULT_AREA"])[0],
            predict_rub_salary_hh,
            get_all_hh_vacancies(f"Программист {lang}", area=CONFIG["HH_DEFAULT_AREA"])[1],
        )
        for lang in languages
    }

    sj_statistics = {
        lang: calculate_statistics(
            get_all_superjob_vacancies(api_key, f"Программист {lang}", CONFIG["SUPERJOB_DEFAULT_CITY"], CONFIG["CATALOGUE_PROGRAMMING"])[0],
            predict_rub_salary_sj,
            get_all_superjob_vacancies(api_key, f"Программист {lang}", CONFIG["SUPERJOB_DEFAULT_CITY"], CONFIG["CATALOGUE_PROGRAMMING"])[1],
        )
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
