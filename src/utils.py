import json
import logging
import os
from typing import Dict, List

import requests
from dotenv import load_dotenv

log_file = os.path.join(os.path.dirname(__file__), "..", "logs", "utils.log")
log_file = os.path.abspath(log_file)

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def transaction_loading(file_path: str) -> List[Dict]:
    """
    Читает файл в формате .JSON
    :param file_path: Принимает на вход путь до JSON-файла
    :return: Возвращает список словарей с данными о финансовых транзакциях
    """
    logger.info(f"Начало загрузки транзакций из файла: {file_path}")

    try:
        if not os.path.exists(file_path):
            logger.warning(f"Файл не найден: {file_path}")
            return []

        file_size = os.path.getsize(file_path)
        logger.debug(f"Размер файла: {file_size} байт")

        if file_size == 0:
            logger.warning(f"Файл пустой: {file_path}")
            return []

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        logger.debug("Успешно загружено данных из JSON")

        if isinstance(data, list):
            logger.info(f"Загружено {len(data)} транзакций из файла {file_path}")
            return data
        else:
            logger.warning(f"Данные в файле {file_path} не являются списком. Тип данных: {type(data)}")
            return []

    except FileNotFoundError:
        logger.error(f"Файл не найден: {file_path}")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка декодирования JSON в файле {file_path}: {e}")
        return []
    except (IOError, OSError) as e:
        logger.error(f"Ошибка ввода/вывода при работе с файлом {file_path}: {e}")
        return []
    except Exception as e:
        logger.error(f"Неожиданная ошибка при загрузке транзакций из {file_path}: {e}")
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

        logger.debug(f"Обработка транзакции: {transaction_amount} {transaction_currency}")

        if transaction_currency not in ("USD", "EUR"):
            logger.debug(f"Конвертация не требуется, валюта: {transaction_currency}")
            return transaction_amount

        load_dotenv()
        api_key = os.getenv("API_KEY")

        if not api_key:
            logger.error("API_KEY не найден в переменных окружения")
            raise ValueError("API_KEY не найден")

        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={transaction_currency}&amount={transaction_amount}"

        headers = {"apikey": api_key}

        logger.info(f"Запрос конвертации: {transaction_amount} {transaction_currency} -> RUB")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        result = response.json()
        converted_amount = float(result["result"])

        logger.info(f"Успешная конвертация: {transaction_amount} {transaction_currency} = {converted_amount} RUB")
        return converted_amount

    except requests.RequestException as e:
        logger.error(f"Ошибка API при конвертации: {e}")
        fallback_amount = float(transaction.get("operationAmount", {}).get("amount", 0))
        logger.warning(f"Возвращаем исходную сумму: {fallback_amount}")
        return fallback_amount

    except (KeyError, ValueError) as e:
        logger.error(f"Ошибка обработки транзакции: {e}")
        fallback_amount = float(transaction.get("operationAmount", {}).get("amount", 0))
        logger.warning(f"Возвращаем исходную сумму: {fallback_amount}")
        return fallback_amount
