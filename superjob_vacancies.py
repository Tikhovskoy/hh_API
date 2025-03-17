from superjob_api import get_superjob_vacancies, get_all_superjob_vacancies
from salary import predict_rub_salary_sj
from statistics_utils import calculate_statistics, print_statistics_table
from config import TOWN_MOSCOW_ID, CATALOGUE_PROGRAMMING, SUPERJOB_DEFAULT_COUNT
import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


def get_language_statistics_sj(language: str,
                               town: int = TOWN_MOSCOW_ID,
                               catalogues: int = CATALOGUE_PROGRAMMING) -> Dict[str, int]:
    """
    Получает статистику вакансий для заданного языка с SuperJob.

    :param language: Название языка программирования.
    :param town: Код города.
    :param catalogues: Код каталога вакансий.
    :return: Словарь со статистикой (найдено вакансий, обработано, средняя зарплата).
    """
    query: str = f"Программист {language}"
    data: Dict[str, Any] = get_superjob_vacancies(query, town=town, catalogues=catalogues, count=SUPERJOB_DEFAULT_COUNT, page=0)
    vacancies_found: int = data.get("total", 0)
    vacancies: List[Dict[str, Any]] = get_all_superjob_vacancies(query, town=town, catalogues=catalogues)
    return calculate_statistics(vacancies, predict_rub_salary_sj, vacancies_found)


def main() -> None:
    """
    Основная функция получения и вывода статистики вакансий с SuperJob для заданных языков программирования.
    """
    languages: List[str] = ["Python", "Java", "JavaScript", "C++", "C#", "PHP", "Ruby", "Go", "1С"]
    stats: Dict[str, Dict[str, int]] = {}
    for language in languages:
        stats[language] = get_language_statistics_sj(language)
    print_statistics_table(stats, title="SuperJob Moscow")


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    main()
