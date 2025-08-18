def get_mask_card_number(number_of_card: str) -> str:
    """
    Маскирует номер карты в формате XXXX XX** **** XXXX
    :param number_of_card: Номер карты (16 цифр)
    :return: Маскированный номер или сообщение об ошибке
    """

    if not number_of_card.isdigit():
        return "Некорректный ввод"
    if len(number_of_card) != 16:
        return "Некорректный ввод"

    first_part = number_of_card[:6]
    last_part = number_of_card[-4:]

    masked_part = "** ****"

    masked_number = f"{first_part[:4]} {first_part[4:6]}{masked_part} {last_part}"

    return masked_number


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер cчёта в формате **XXXX
    :param account_number: Номер счёта (20 цифр)
    :return: Маскированный номер или сообщение об ошибке
    """
    if not account_number.isdigit():
        return "Некорректный ввод"
    if len(account_number) != 20:
        return "Некорректный ввод"

    last_part = account_number[-4:]

    masked_part = "**"

    masked_number = f"{masked_part}{last_part}"

    return masked_number
