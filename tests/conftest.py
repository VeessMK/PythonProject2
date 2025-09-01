from typing import Any, Dict, List

import pytest


@pytest.fixture
def card_number() -> str:
    return "7000792289606361"


@pytest.fixture
def account_number() -> str:
    return "73654108430135874305"


@pytest.fixture
def maestro_template() -> str:
    return "Maestro 1596837868705199"


@pytest.fixture
def mastercard_template() -> str:
    return "MasterCard 7158300734726758"


@pytest.fixture
def visa_classic_template() -> str:
    return "Visa Classic 6831982476737658"


@pytest.fixture
def visa_platinum_template() -> str:
    return "Visa Platinum 8990922113665229"


@pytest.fixture
def visa_gold_template() -> str:
    return "Visa Gold 5999414228426353"


@pytest.fixture
def account_template() -> str:
    return "Счет 73654108430135874305"


@pytest.fixture
def date_template() -> str:
    return "2024-03-11T02:26:18.671407"


@pytest.fixture
def list_for_filter_by_state() -> List[Dict[str, Any]]:
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


@pytest.fixture
def list_for_filter_without_state() -> List[Dict[str, Any]]:
    return [
        {"id": 41428829, "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "date": "2018-10-14T08:21:33.419441"},
    ]


@pytest.fixture
def list_for_sorting_by_date() -> List[Dict[str, Any]]:
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]
