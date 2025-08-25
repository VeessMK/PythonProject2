from typing import Any, Dict, List


def filter_by_state(list_dict: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """
    Фильтрует список словарей по значению ключа 'state'
    :param list_dict: Список словарей
    :param state: Значение для фильтрации
    :return: Отфильтрованный список словарей
    """
    return [x for x in list_dict if x["state"] == state]
