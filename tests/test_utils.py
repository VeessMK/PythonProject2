from unittest.mock import mock_open, patch

from src.utils import transaction_exchange, transaction_loading


def test_file_not_found():
    with patch("src.utils.open", side_effect=FileNotFoundError):
        result = transaction_loading("nonexistent_file.json")
        assert result == []


def test_file_not_list():
    with patch("src.utils.open", mock_open()):
        with patch("json.load") as mock_json_load:
            mock_json_load.return_value = {"key": "value"}

            result = transaction_loading("not_list.json")
            assert result == []


def test_empty_list():
    with patch("src.utils.open", mock_open()):
        with patch("json.load") as mock_json_load:
            mock_json_load.return_value = []

            result = transaction_loading("empty.json")
            assert result == []


def test_transaction_exchange_rub_no_conversion_needed():

    transaction = {"operationAmount": {"amount": "1000.50", "currency": {"code": "RUB", "name": "руб."}}}

    result = transaction_exchange(transaction)

    assert result == 1000.50


@patch("src.utils.requests.get")
@patch("src.utils.load_dotenv")
@patch("src.utils.os.getenv")
def test_transaction_exchange_missing_api_key(mock_getenv, mock_load_dotenv, mock_requests_get):

    transaction = {"operationAmount": {"amount": "100.00", "currency": {"code": "USD", "name": "USD"}}}

    mock_getenv.return_value = None

    result = transaction_exchange(transaction)
    assert result == 100.00
    mock_load_dotenv.assert_called_once()
    mock_getenv.assert_called_once_with("API_KEY")
    mock_requests_get.assert_not_called()


def test_transaction_exchange_missing_operation_amount():
    transaction = {"id": 123, "state": "EXECUTED", "description": "Перевод"}
    result = transaction_exchange(transaction)

    assert result == 0.0


def test_transaction_exchange_unknown_currency():

    transaction = {
        "operationAmount": {"amount": "500.00", "currency": {"code": "GBP", "name": "GBP"}}  # Фунты стерлингов
    }

    result = transaction_exchange(transaction)

    assert result == 500.00  # Должен вернуть исходную сумму для неизвестной валюты
