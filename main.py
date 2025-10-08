import os

from src.bank import process_bank_search
from src.file_readers import csv_reader, xlsx_reader
from src.generators import filter_by_currency
from src.processing import filter_by_state, sort_by_date
from src.utils import transaction_loading


def main():
    """функция запуска программы"""
    print(
        """Привет! Добро пожаловать в программу работы с банковскими транзакциями.
Выберите необходимый пункт меню:
1. Получить информацию о транзакциях из JSON-файла
2. Получить информацию о транзакциях из CSV-файла
3. Получить информацию о транзакциях из XLSX-файла"""
    )

    choice = input()
    while True:
        if choice == "1":
            print("Для обработки выбран JSON-файл.\n")
            transactions = transaction_loading("data/operations.json")
            break
        elif choice == "2":
            print("Для обработки выбран CSV-файл.\n")
            transactions = csv_reader("data/transactions.csv")
            break
        elif choice == "3":
            print("Для обработки выбран XLSX-файл.\n")
            transactions = xlsx_reader(os.path.join("data/transactions_excel.xlsx"))
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите 1, 2 или 3.\n")

    print("Введите статус, по которому необходимо выполнить фильтрацию.")
    print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")

    while True:
        state = input().upper()

        if state in ["EXECUTED", "CANCELED", "PENDING"]:
            filtered_transactions = filter_by_state(transactions, state)
            print(f'Операции отфильтрованы по статусу "{state}"\n')
            break
        else:
            print(f'Статус операции "{state}" недоступен.\n')

    print("Отсортировать операции по дате? Да/Нет")
    user_input = input().lower()
    if user_input in ["да", "нет"]:
        if user_input == "да":
            print("Отсортировать по возрастанию или по убыванию?")
            if input().lower() == "по возрастанию":
                filtered_transactions = sort_by_date(filtered_transactions, reverse=False)
                print("по возрастанию")
            else:
                filtered_transactions = sort_by_date(filtered_transactions, reverse=True)
                print("по убыванию")
    print()

    print("Выводить только рублевые транзакции? Да/Нет")
    if input().lower() == "да":
        filtered_transactions = list(filter_by_currency(filtered_transactions, "RUB"))
    print()

    print("Отфильтровать список транзакций по определенному слову в описании? Да/Нет")
    if input().lower() == "да":
        print("Введите слово для поиска:")
        search_word = input()
        filtered_transactions = process_bank_search(filtered_transactions, search_word)
        print(f'Отфильтрованы транзакции содержащие "{search_word}" в описании')
    print()

    if filtered_transactions:
        print("Распечатываю итоговый список транзакций...")
        print(f"Всего операций в выборке: {len(filtered_transactions)}")
        print(filtered_transactions)
    else:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")


print(main())
