import csv
import os

import pandas as pd

ABSPATH_TO_CSV = os.path.join(os.path.dirname(__file__), "..", "data", "transactions.csv")
ABSPATH_TO_XLSX = os.path.join(os.path.dirname(__file__), "..", "data", "transactions_excel.xlsx")


def csv_reader(path: str = ABSPATH_TO_CSV) -> list:
    """
    Читает csv файл
    :param path: Путь к файлу
    :return: Список словарей
    """
    result = []
    try:
        with open(path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=";")
            for row in reader:
                result.append(row)
        return result
    except FileNotFoundError:
        print(f"Ошибка: Файл {path} не найден")
        return []
    except Exception as e:
        print(f"Ошибка при чтении CSV: {e}")
        return []


def xlsx_reader(path: str = ABSPATH_TO_XLSX) -> list:
    """
    Читает excel файл
    :param path: Путь к файлу
    :return: Список словарей
    """
    try:
        df = pd.read_excel(path)
        result = df.to_dict("records")
        return result
    except FileNotFoundError:
        print(f"Ошибка: Файл {path} не найден")
        return []
    except Exception as e:
        print(f"Ошибка при чтении Excel: {e}")
        return []
