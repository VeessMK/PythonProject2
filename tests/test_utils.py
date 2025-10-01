import json
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


def test_successful_loading():
    test_data = [{"id": 1, "amount": 100}, {"id": 2, "amount": 200}]

    with patch("src.utils.open", mock_open()):
        with patch("json.load") as mock_json_load:
            with patch("os.path.exists") as mock_exists:
                with patch("os.path.getsize") as mock_size:
                    mock_exists.return_value = True
                    mock_size.return_value = 100
                    mock_json_load.return_value = test_data
                    result = transaction_loading("success.json")
                    assert result == test_data


def test_empty_file():
    with patch("src.utils.open", mock_open()):
        with patch("os.path.exists") as mock_exists:
            with patch("os.path.getsize") as mock_size:
                mock_exists.return_value = True
                mock_size.return_value = 0
                result = transaction_loading("empty_file.json")
                assert result == []


def test_json_decode_error():
    with patch("src.utils.open", mock_open()):
        with patch("os.path.exists") as mock_exists:
            with patch("os.path.getsize") as mock_size:
                mock_exists.return_value = True
                mock_size.return_value = 100
                with patch("json.load", side_effect=json.JSONDecodeError("msg", "doc", 0)):
                    result = transaction_loading("invalid.json")
                    assert result == []


def test_io_error():
    with patch("src.utils.open", side_effect=IOError("IO error")):
        with patch("os.path.exists") as mock_exists:
            mock_exists.return_value = True
            result = transaction_loading("io_error.json")
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
    transaction = {"operationAmount": {"amount": "500.00", "currency": {"code": "GBP", "name": "GBP"}}}
    result = transaction_exchange(transaction)
    assert result == 500.00


@patch("src.utils.requests.get")
@patch("src.utils.load_dotenv")
@patch("src.utils.os.getenv")
def test_transaction_exchange_success_usd(mock_getenv, mock_load_dotenv, mock_requests_get):
    transaction = {"operationAmount": {"amount": "100.00", "currency": {"code": "USD", "name": "USD"}}}
    mock_response = mock_requests_get.return_value
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"result": 7500.50}
    mock_getenv.return_value = "test_api_key"
    result = transaction_exchange(transaction)
    assert result == 7500.50
    mock_requests_get.assert_called_once()
    mock_response.raise_for_status.assert_called_once()


@patch("src.utils.requests.get")
@patch("src.utils.load_dotenv")
@patch("src.utils.os.getenv")
def test_transaction_exchange_success_eur(mock_getenv, mock_load_dotenv, mock_requests_get):
    transaction = {"operationAmount": {"amount": "50.00", "currency": {"code": "EUR", "name": "EUR"}}}
    mock_response = mock_requests_get.return_value
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"result": 4500.25}
    mock_getenv.return_value = "test_api_key"
    result = transaction_exchange(transaction)
    assert result == 4500.25
    mock_requests_get.assert_called_once()


def test_transaction_exchange_missing_amount():
    transaction = {"operationAmount": {"currency": {"code": "RUB"}}}
    result = transaction_exchange(transaction)
    assert result == 0.0
