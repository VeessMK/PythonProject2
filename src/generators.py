def filter_by_currency(transactions, currency):
    """
    Фильтрует транзакции по коду валюты и возвращает итератор.
    """
    return (transaction for transaction in transactions if transaction.get('operationAmount', {}).get('currency', {}).get('code') == currency)

