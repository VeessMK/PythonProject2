from src.masks import get_mask_account, get_mask_card_number


def get_date(full_date: str) -> str:
    """
    Принимает формат "2024-03-11T02:26:18.671407"
    и возвращает строку с датой в формате
    "ДД.ММ.ГГГГ"
    """

    return f"{full_date[8:10]}.{full_date[5:7]}.{full_date[:4]}"


def mask_account_card(account_card: str) -> str:
    """
    Принимать — строку, содержащую тип и номер карты или счета.
    Возвращать строку с замаскированным номером.
    В формате:
    Для карт: XXXX XX** **** XXXX
    Для счетов: **XXXX
    """

    separator = account_card.split(" ")
    if len(separator) < 2:
        return "Некорректный ввод"

    account_card_type = " ".join(separator[:-1])
    account_card_number = separator[-1]

    if "Счет" in account_card_type:
        masked_number = get_mask_account(account_card_number)
    else:
        masked_number = get_mask_card_number(account_card_number)

    return f"{account_card_type} {masked_number}"
