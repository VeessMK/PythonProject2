import re
from collections import Counter
from typing import Any, Dict, List


def process_bank_search(data: List[Dict[str, Any]], search: str) -> List[Dict[str, Any]]:
    """
    Фильтрует список банковских операций по заданной строке в описании.
    """
    if not data or not search:
        return []

    filtered_operations = []

    for operation in data:
        description = operation.get("description", "")

        if re.search(search, description, re.IGNORECASE):
            filtered_operations.append(operation)

    return filtered_operations


def process_bank_operations_regex(data: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество банковских операций по заданным категориям
    с использованием регулярных выражений.
    """
    if not data or not categories:
        return {}

    patterns = {category: re.compile(rf"\b{re.escape(category)}\b", re.IGNORECASE) for category in categories}

    category_counter = Counter({category: 0 for category in categories})

    for operation in data:
        description = operation.get("description", "")

        for category, pattern in patterns.items():
            if pattern.search(description):
                category_counter[category] += 1

    return dict(category_counter)
