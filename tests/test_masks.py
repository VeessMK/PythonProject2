import pytest

from src.masks import get_mask_account, get_mask_card_number


class TestGetMaskCardNumber:

    def test_correct_mask_card(self):
        result = get_mask_card_number("7000792289606361")
        assert result == "7000 79** **** 6361"

    @pytest.mark.parametrize(
        "value, expected",
        [
            ("70007922896063611111", "Номер карты должен содержать 16 цифр"),  # 20 цифр
            ("700079228960636", "Номер карты должен содержать 16 цифр"),  # 15 цифр
            ("700079228960636a", "Номер карты должен содержать только цифры"),  # буквы
            ("", "Номер карты должен содержать только цифры"),  # пустая строка
        ],
    )
    def test_incorrect_card_mask(self, value: str, expected: str):
        assert get_mask_card_number(value) == expected


class TestGetMaskAccount:

    def test_correct_mask_account(self):
        result = get_mask_account("73654108430135874305")
        assert result == "**4305"

    @pytest.mark.parametrize(
        "value, expected",
        [
            ("73654108430135874305555", "Некорректный ввод: номер счета должен содержать 20 цифр"),  # 23 цифры
            ("7365410843013587430", "Некорректный ввод: номер счета должен содержать 20 цифр"),  # 19 цифр
            ("7365410843013587430a", "Некорректный ввод: номер счета должен содержать только цифры"),  # буквы
            ("", "Некорректный ввод: номер счета должен содержать только цифры"),  # пустая строка
        ],
    )
    def test_incorrect_account_mask(self, value: str, expected: str):
        assert get_mask_account(value) == expected
