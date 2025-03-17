from hh_api import get_hh_vacancies, get_all_hh_vacancies
from superjob_api import get_superjob_vacancies, get_all_superjob_vacancies
from salary import predict_rub_salary_hh, predict_rub_salary_sj
from config import HH_DEFAULT_PER_PAGE, TOWN_MOSCOW_ID, CATALOGUE_PROGRAMMING, SUPERJOB_DEFAULT_COUNT
from statistics_utils import calculate_statistics, print_statistics_table
from typing import Optional, Dict
import logging

logger = logging.getLogger(__name__)

def get_language_statistics_hh(language: str, area: int = 1, date_from: Optional[str] = None) -> Dict[str, int]:
    query = f"Программист {language}"
    hh_initial_response = get_hh_vacancies(query, area=area, per_page=HH_DEFAULT_PER_PAGE, page=0, date_from=date_from)
    vacancies_found = hh_initial_response.get("found", 0)
    vacancies_list = get_all_hh_vacancies(query, area=area, date_from=date_from)
    return calculate_statistics(vacancies_list, predict_rub_salary_hh, vacancies_found)

def get_language_statistics_sj(language: str, town: int = TOWN_MOSCOW_ID, catalogues: int = CATALOGUE_PROGRAMMING) -> Dict[str, int]:
    query = f"Программист {language}"
    sj_initial_response = get_superjob_vacancies(query, town=town, catalogues=catalogues, count=SUPERJOB_DEFAULT_COUNT, page=0)
    vacancies_found = sj_initial_response.get("total", 0)
    vacancies_list = get_all_superjob_vacancies(query, town=town, catalogues=catalogues)
    return calculate_statistics(vacancies_list, predict_rub_salary_sj, vacancies_found)

def main() -> None:
    languages = ["Python", "C", "C#", "C++", "Java", "JS", "Ruby", "Go", "1С"]

    # Статистика для HeadHunter
    hh_statistics = {lang: get_language_statistics_hh(lang, area=1) for lang in languages}

    # Статистика для SuperJob
    sj_statistics = {lang: get_language_statistics_sj(lang) for lang in languages}

    print_statistics_table(hh_statistics, title="HeadHunter Moscow",
                           headers=["Язык программирования", "Найдено вакансий",
                                    "Обработано вакансий", "Средняя зарплата"])
    logger.info("\n")
    print_statistics_table(sj_statistics, title="SuperJob Moscow",
                           headers=["Язык программирования", "Ваксий найдено",
                                    "Ваксий обработано", "Средняя зарплата"])

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    import logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    main()
