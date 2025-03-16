from hh_api import get_all_hh_vacancies
from salary import predict_rub_salary_hh
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def main() -> None:
    """
    Получает вакансии с HeadHunter по запросу и выводит информацию о первых 10 вакансиях.
    """
    query: str = "Программист Python"
    vacancies: List[Dict[str, Any]] = get_all_hh_vacancies(query, area=1)
    logger.info(f"HH API: Найдено {len(vacancies)} вакансий по запросу '{query}'")
    # Вывод информации по первым 10 вакансиям
    for vacancy in vacancies[:10]:
        vacancy_name: str = vacancy.get("name", "Нет названия")
        salary = predict_rub_salary_hh(vacancy)
        logger.info(f"{vacancy_name} – {salary}")


if __name__ == "__main__":
    main()
