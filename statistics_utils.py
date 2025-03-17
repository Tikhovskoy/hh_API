from typing import List, Dict, Any, Optional, Callable
from terminaltables import AsciiTable
import logging

logger = logging.getLogger(__name__)

def calculate_statistics(
    vacancies: List[Dict[str, Any]],
    salary_func: Callable[[Dict[str, Any]], Optional[float]],
    total_vacancies: int
) -> Dict[str, int]:
    """
    Вычисляет статистику по списку вакансий:
    - Количество обработанных вакансий (где удалось вычислить зарплату)
    - Средняя зарплата по обработанным вакансиям

    :param vacancies: Список вакансий.
    :param salary_func: Функция для вычисления зарплаты из вакансии.
    :param total_vacancies: Общее количество найденных вакансий.
    :return: Словарь со статистикой.
    """
    total_salary = 0
    processed = 0
    for vacancy in vacancies:
        salary = salary_func(vacancy)
        if salary:
            total_salary += salary
            processed += 1
    average_salary = int(total_salary / processed) if processed else 0
    return {
        "vacancies_found": total_vacancies,
        "vacancies_processed": processed,
        "average_salary": average_salary
    }

def print_statistics_table(
    stats: Dict[str, Dict[str, int]],
    title: str,
    headers: Optional[List[str]] = None
) -> None:
    """
    Выводит статистику вакансий в виде ASCII-таблицы.

    :param stats: Словарь со статистикой по каждому языку.
    :param title: Заголовок таблицы.
    :param headers: Опциональный список заголовков (если не указан, используются стандартные).
    """
    if not headers:
        headers = ["Язык программирования", "Вакансий найдено", "Вакансий обработано", "Средняя зарплата"]
    table_data = [headers]
    for language, data in stats.items():
        table_data.append([
            language.lower(),
            str(data.get("vacancies_found", 0)),
            str(data.get("vacancies_processed", 0)),
            str(data.get("average_salary", 0))
        ])
    table = AsciiTable(table_data, title)
    logger.info("\n" + table.table)
