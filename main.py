import os

from src.bank import process_bank_search
from src.file_readers import csv_reader, xlsx_reader
from src.generators import filter_by_currency
from src.processing import filter_by_state, sort_by_date
from src.utils import transaction_loading


def main():
    """Функция запуска программы"""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    while True:
        choice = input().strip()
        if choice == "1":
            print("Для обработки выбран JSON-файл.\n")
            try:
                transactions = transaction_loading("data/operations.json")
                break
            except Exception as e:
                print(f"Ошибка при чтении JSON-файла: {e}")
                return
        elif choice == "2":
            print("Для обработки выбран CSV-файл.\n")
            try:
                transactions = csv_reader("data/transactions.csv")
                break
            except Exception as e:
                print(f"Ошибка при чтении CSV-файла: {e}")
                return
        elif choice == "3":
            print("Для обработки выбран XLSX-файл.\n")
            try:
                transactions = xlsx_reader(os.path.join("data/transactions_excel.xlsx"))
                break
            except Exception as e:
                print(f"Ошибка при чтении XLSX-файла: {e}")
                return
        else:
            print("Неверный выбор. Пожалуйста, выберите 1, 2 или 3.")

    print("Введите статус, по которому необходимо выполнить фильтрацию.")
    print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")

    while True:
        state = input().strip().upper()
        if state in ["EXECUTED", "CANCELED", "PENDING"]:
            filtered_transactions = filter_by_state(transactions, state)
            print(f'Операции отфильтрованы по статусу "{state}"\n')
            break
        else:
            print(f'Статус операции "{state}" недоступен.')
            print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")

    print("Отсортировать операции по дате? Да/Нет")
    while True:
        sort_choice = input().strip().lower()
        if sort_choice in ["да", "нет"]:
            if sort_choice == "да":
                print("Отсортировать по возрастанию или по убыванию?")
                while True:
                    order_choice = input().strip().lower()
                    if order_choice == "по возрастанию":
                        filtered_transactions = sort_by_date(filtered_transactions, reverse=False)
                        print("Операции отсортированы по возрастанию даты")
                        break
                    elif order_choice == "по убыванию":
                        filtered_transactions = sort_by_date(filtered_transactions, reverse=True)
                        print("Операции отсортированы по убыванию даты")
                        break
                    else:
                        print("Пожалуйста, введите 'по возрастанию' или 'по убыванию'")
            break
        else:
            print("Пожалуйста, ответьте 'Да' или 'Нет'")
    print()

    print("Выводить только рублевые транзакции? Да/Нет")
    while True:
        currency_choice = input().strip().lower()
        if currency_choice in ["да", "нет"]:
            if currency_choice == "да":
                filtered_transactions = list(filter_by_currency(filtered_transactions, "RUB"))
                print("Оставлены только рублевые транзакции")
            break
        else:
            print("Пожалуйста, ответьте 'Да' или 'Нет'")
    print()

    print("Отфильтровать список транзакций по определенному слову в описании? Да/Нет")
    while True:
        search_choice = input().strip().lower()
        if search_choice in ["да", "нет"]:
            if search_choice == "да":
                print("Введите слово для поиска:")
                search_word = input().strip()
                if search_word:
                    filtered_transactions = process_bank_search(filtered_transactions, search_word)
                    print(f'Найдено {len(filtered_transactions)} транзакций, содержащих "{search_word}" в описании')
                else:
                    print("Не введено слово для поиска")
            break
        else:
            print("Пожалуйста, ответьте 'Да' или 'Нет'")
    print()

    if filtered_transactions:
        print("Распечатываю итоговый список транзакций...")
        print(f"Всего банковских операций в выборке: {len(filtered_transactions)}")
        print()

        for transaction in filtered_transactions:
            print(transaction)
            print()
    else:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")


print(main())
