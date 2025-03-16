from typing import Optional, Dict

def predict_salary(salary_from: Optional[float], salary_to: Optional[float]) -> Optional[float]:
    """
    Рассчитывает ожидаемую зарплату по заданным значениям.

    Если заданы оба значения – возвращается их среднее.
    Если задан только salary_from – возвращается salary_from * 1.2.
    Если задан только salary_to – возвращается salary_to * 0.8.
    Если ни одно значение не задано – возвращается None.

    :param salary_from: Минимальное значение зарплаты.
    :param salary_to: Максимальное значение зарплаты.
    :return: Предсказанная зарплата или None.
    """
    if salary_from is not None and salary_to is not None:
        return (salary_from + salary_to) / 2.0
    elif salary_from is not None:
        return salary_from * 1.2
    elif salary_to is not None:
        return salary_to * 0.8
    else:
        return None


def predict_rub_salary_hh(vacancy: Dict) -> Optional[float]:
    """
    Вычисляет зарплату вакансии для HeadHunter.

    Если валюта равна 'RUR', рассчитывается зарплата по значениям 'from' и 'to'.
    Иначе возвращается None.

    :param vacancy: Словарь с данными вакансии.
    :return: Зарплата в рублях или None.
    """
    salary = vacancy.get("salary")
    if not salary or salary.get("currency") != "RUR":
        return None
    return predict_salary(salary.get("from"), salary.get("to"))


def predict_rub_salary_sj(vacancy: Dict) -> Optional[float]:
    """
    Вычисляет зарплату вакансии для SuperJob.

    Если валюта равна 'rub', рассчитывается зарплата по значениям 'payment_from' и 'payment_to'.
    Иначе возвращается None.

    :param vacancy: Словарь с данными вакансии.
    :return: Зарплата в рублях или None.
    """
    payment_from = vacancy.get("payment_from")
    payment_to = vacancy.get("payment_to")
    currency = vacancy.get("currency")
    if currency != "rub":
        return None
    return predict_salary(payment_from, payment_to)
