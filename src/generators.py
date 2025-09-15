def filter_by_currency(transactions, currency):
    """
    Фильтрует транзакции по коду валюты и возвращает итератор.
    """
    return (
        transaction
        for transaction in transactions
        if transaction.get("operationAmount", {}).get("currency", {}).get("code") == currency
    )


def transaction_descriptions(transactions):
    """
    Принимает список словарей с транзакциями и возвращает описание каждой операции по очереди.
    """
    return (transaction.get("description") for transaction in transactions)


def card_number_generator(start: int, end: int):
    """Генератор номеров банковских карт."""
    for number in range(start, end + 1):
        card_str = f"{number:016d}"
        yield f"{card_str[:4]} {card_str[4:8]} {card_str[8:12]} {card_str[12:16]}"
