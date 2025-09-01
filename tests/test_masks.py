import pytest

from src.masks import get_mask_account, get_mask_card_number


def test_correct_mask_card(card_number: str) -> str:
    assert get_mask_card_number(card_number) == "7000 79** **** 6361"


@pytest.mark.parametrize(
    "value, expected",
    [
        ("70007922896063611111", "Некорректный ввод"),
        ("", "Некорректный ввод"),
    ],
)
def test_correct_card_mask(value: str, expected: str) -> str:
    assert get_mask_account(value) == expected


def test_correct_mask_account(account_number: str) -> str:
    assert get_mask_account(account_number) == "**4305"


@pytest.mark.parametrize(
    "value, expected",
    [
        ("73654108430135874305555", "Некорректный ввод"),
        ("", "Некорректный ввод"),
    ],
)
def test_correct_mask_card_number(value: str, expected: str) -> str:
    assert get_mask_card_number(value) == expected
