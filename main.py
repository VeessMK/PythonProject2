from src.masks import get_mask_account, get_mask_card_number

from src.processing import filter_by_state, sort_by_date

from src.widget import get_date, mask_account_card

from src.generators import filter_by_currency, transaction_descriptions

print(get_mask_card_number("7000792289606361"))

print(get_mask_account("73654108430135874305"))

print(mask_account_card("Visa Platinum 8990922113665229"))

print(mask_account_card("Счет 73654108430135874305"))

print(get_date("2024-03-11T02:26:18.671407"))

list_dict = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
]

print(filter_by_state(list_dict))

print(filter_by_state(list_dict, state="CANCELED"))

print(sort_by_date(list_dict))

print(sort_by_date(list_dict, reverse=False))

transactions = [
    {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {
            "amount": "9824.07",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702"
    },
    {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {
            "amount": "79114.93",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188"
    },
    {
        "id": 873106923,
        "state": "EXECUTED",
        "date": "2019-03-23T01:09:46.296404",
        "operationAmount": {
            "amount": "43318.34",
            "currency": {
                "name": "рубли",
                "code": "RUB"
            }
        },
        "description": "Перевод со счета на счет",
        "from": "Счет 44812258784861134719",
        "to": "Счет 74489636417521191160"
    }
]

usd_transactions = filter_by_currency(transactions, "USD")
for _ in range(1):
    print(next(usd_transactions))

descriptions = transaction_descriptions(transactions)
for _ in range(1):
    print(next(descriptions))