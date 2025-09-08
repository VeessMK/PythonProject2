import pytest

from src.widget import get_date, mask_account_card


def test_maestro_card_template(maestro_template: str) -> str:
    assert mask_account_card(maestro_template) == "Maestro 1596 83** **** 5199"


def test_mastercard_template(mastercard_template: str) -> str:
    assert mask_account_card(mastercard_template) == "MasterCard 7158 30** **** 6758"


def test_visa_classic_template(visa_classic_template: str) -> str:
    assert mask_account_card(visa_classic_template) == "Visa Classic 6831 98** **** 7658"


def test_visa_platinum_template(visa_platinum_template: str) -> str:
    assert mask_account_card(visa_platinum_template) == "Visa Platinum 8990 92** **** 5229"


def test_visa_gold_template(visa_gold_template: str) -> str:
    assert mask_account_card(visa_gold_template) == "Visa Gold 5999 41** **** 6353"


def test_account_template(account_template: str) -> str:
    assert mask_account_card(account_template) == "Счет **4305"


@pytest.mark.parametrize(
    "value, expected",
    [
        ("Счет 736541084301358743055", "Счет Некорректный ввод"),
        ("", "Некорректный ввод"),
    ],
)
def test_unexpected_input(value: str, expected: str) -> str:
    assert mask_account_card(value) == expected


def test_data(date_template: str) -> str:
    assert get_date(date_template) == "11.03.2024"


@pytest.mark.parametrize(
    "value, expected",
    [
        ("2026-12-31T23:59:59.999999", "31.12.2026"),
        ("2025-12-31T23:59:59.999999", "31.12.2025"),
        ("2025-02-29T12:00:00.000000", "29.02.2025"),
    ],
)
def test_unusual_data(value: str, expected: str) -> str:
    assert get_date(value) == expected
