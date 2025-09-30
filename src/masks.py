import logging
import os

log_file = os.path.join(os.path.dirname(__file__), "..", "logs", "masks.log")
log_file = os.path.abspath(log_file)

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def get_mask_card_number(number_of_card: str) -> str:
    """
    Маскирует номер карты в формате XXXX XX** **** XXXX
    :param number_of_card: Номер карты (16 цифр)
    :return: Маскированный номер или сообщение об ошибке
    """
    logger.info(f"Начало маскировки номера карты: {number_of_card}")

    if not number_of_card.isdigit():
        error_msg = "Номер карты должен содержать только цифры"
        logger.error(f"{error_msg}. Введено: '{number_of_card}'")
        return error_msg

    if len(number_of_card) != 16:
        error_msg = "Номер карты должен содержать 16 цифр"
        logger.error(f"{error_msg}. Получено {len(number_of_card)} цифр: '{number_of_card}'")
        return error_msg

    try:
        first_part = number_of_card[:6]
        last_part = number_of_card[-4:]
        masked_part = "** ****"
        masked_number = f"{first_part[:4]} {first_part[4:6]}{masked_part} {last_part}"

        logger.info(f"Успешная маскировка карты: {number_of_card} -> {masked_number}")
        return masked_number

    except Exception as e:
        error_msg = f"Ошибка при маскировке номера карты: {str(e)}"
        logger.exception(f"{error_msg}. Номер карты: {number_of_card}")
        return "Ошибка при обработке номера карты"


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер cчёта в формате **XXXX
    :param account_number: Номер счёта (20 цифр)
    :return: Маскированный номер или сообщение об ошибке
    """
    logger.info(f"Начало маскировки номера счета: {account_number}")

    if not account_number.isdigit():
        error_msg = "Некорректный ввод: номер счета должен содержать только цифры"
        logger.error(f"{error_msg}. Введено: '{account_number}'")
        return error_msg

    if len(account_number) != 20:
        error_msg = "Некорректный ввод: номер счета должен содержать 20 цифр"
        logger.error(f"{error_msg}. Получено {len(account_number)} цифр: '{account_number}'")
        return error_msg

    try:
        last_part = account_number[-4:]
        masked_part = "**"
        masked_number = f"{masked_part}{last_part}"

        logger.info(f"Успешная маскировка счета: {account_number} -> {masked_number}")
        return masked_number

    except Exception as e:
        error_msg = f"Ошибка при маскировке номера счета: {str(e)}"
        logger.exception(f"{error_msg}. Номер счета: {account_number}")
        return "Ошибка при обработке номера счета"
