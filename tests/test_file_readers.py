from unittest.mock import mock_open, patch

from src.file_readers import csv_reader, xlsx_reader


class TestCSVReader:

    @patch("builtins.open", new_callable=mock_open, read_data="id;amount;date\n1;100;2024-01-01\n2;200;2024-01-02")
    def test_csv_reader_success(self, mock_file):
        result = csv_reader("test.csv")

        mock_file.assert_called_once_with("test.csv", "r", encoding="utf-8")

        assert len(result) == 2
        assert result[0] == {"id": "1", "amount": "100", "date": "2024-01-01"}
        assert result[1] == {"id": "2", "amount": "200", "date": "2024-01-02"}

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_csv_reader_file_not_found(self, mock_file):
        result = csv_reader("nonexistent.csv")

        assert result == []
        mock_file.assert_called_once_with("nonexistent.csv", "r", encoding="utf-8")


class TestXLSXReader:

    @patch("pandas.read_excel")
    def test_xlsx_reader_success(self, mock_read_excel):
        mock_data = [
            {"id": 1, "amount": 100.0, "date": "2024-01-01"},
            {"id": 2, "amount": 200.0, "date": "2024-01-02"},
        ]

        mock_df = mock_read_excel.return_value
        mock_df.to_dict.return_value = mock_data

        result = xlsx_reader("test.xlsx")

        mock_read_excel.assert_called_once_with("test.xlsx")
        mock_df.to_dict.assert_called_once_with("records")

        assert result == mock_data
        assert len(result) == 2
        assert result[0]["id"] == 1
        assert result[0]["amount"] == 100.0

    @patch("pandas.read_excel", side_effect=FileNotFoundError)
    def test_xlsx_reader_file_not_found(self, mock_read_excel):

        result = xlsx_reader("nonexistent.xlsx")

        assert result == []
        mock_read_excel.assert_called_once_with("nonexistent.xlsx")
