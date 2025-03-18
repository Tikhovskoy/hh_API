from hh_api import get_all_hh_vacancies
from salary import predict_rub_salary_hh
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    config_data = config.get_config()
    query: str = "Программист Python"
    vacancies, vacancies_found = get_all_hh_vacancies(query, area=config_data["HH_DEFAULT_AREA"])
    
    logger.info(f"HH API: Найдено {vacancies_found} вакансий по запросу '{query}'")
    
    for vacancy in vacancies[:config_data["DEFAULT_TOP_VACANCIES"]]:
        vacancy_name: str = vacancy.get("name", "Нет названия")
        salary = predict_rub_salary_hh(vacancy)
        logger.info(f"{vacancy_name} – {salary}")

if __name__ == "__main__":
    main()
