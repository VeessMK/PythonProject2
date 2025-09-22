import json
import os
from typing import Dict, List

import requests
from dotenv import load_dotenv


def transaction_loading(file_path: str) -> List[Dict]:
    """
    Читает файл в формате .JSON
    :param file_path: Принимает на вход путь до JSON-файла
    :return: Возвращает список словарей с данными о финансовых транзакциях
    """
    try:
        if not os.path.exists(file_path):
            return []

        if os.path.getsize(file_path) == 0:
            return []

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            return data
        else:
            return []

    except (json.JSONDecodeError, IOError, OSError):
        return []


def transaction_exchange(transaction: Dict) -> float:
    """
    Отдаёт сумму транзакции,
    :param transaction: Принимает на вход транзакцию
    :return: Возвращает сумму транзакции в рублях
    """
    try:
        operation_amount = transaction.get("operationAmount", {})
        transaction_currency = operation_amount.get("currency", {}).get("code")
        transaction_amount = float(operation_amount.get("amount", 0))

        if transaction_currency not in ("USD", "EUR"):
            return transaction_amount

        load_dotenv()
        api_key = os.getenv("API_KEY")

        if not api_key:
            raise ValueError("API_KEY не найден")

        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={transaction_currency}&amount={transaction_amount}"

        headers = {"apikey": api_key}

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        result = response.json()
        return float(result["result"])

    except (KeyError, ValueError, requests.RequestException) as e:
        print(f"Ошибка при конвертации: {e}")
        return float(transaction.get("operationAmount", {}).get("amount", 0))
