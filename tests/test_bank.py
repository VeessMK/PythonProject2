from src.bank import process_bank_operations_regex, process_bank_search


class TestProcessBankSearch:

    def test_search_by_description(self):
        data = [
            {"description": "Перевод организации ООО Рога", "amount": 1000},
            {"description": "Оплата услуг связи", "amount": -500},
            {"description": "Зарплата от ООО Рога", "amount": 2000},
        ]

        result = process_bank_search(data, "рога")
        assert len(result) == 2
        assert result[0]["description"] == "Перевод организации ООО Рога"
        assert result[1]["description"] == "Зарплата от ООО Рога"

    def test_search_case_insensitive(self):
        data = [
            {"description": "Перевод организации", "amount": 1000},
            {"description": "ОПЛАТА УСЛУГ", "amount": -500},
        ]

        result = process_bank_search(data, "оплата")
        assert len(result) == 1
        assert result[0]["description"] == "ОПЛАТА УСЛУГ"

    def test_search_no_results(self):
        data = [
            {"description": "Перевод организации", "amount": 1000},
            {"description": "Оплата услуг", "amount": -500},
        ]

        result = process_bank_search(data, "зарплата")
        assert len(result) == 0
        assert result == []

    def test_empty_data(self):
        result = process_bank_search([], "поиск")
        assert result == []

    def test_empty_search_string(self):
        data = [
            {"description": "Перевод организации", "amount": 1000},
        ]

        result = process_bank_search(data, "")
        assert result == []


class TestProcessBankOperationsRegex:

    def test_count_with_word_boundaries(self):
        data = [
            {"description": "Денежный перевод", "amount": 1000},
            {"description": "Переводной пункт", "amount": -500},  # Не должно считаться
            {"description": "Перевод средств", "amount": 2000},
        ]

        categories = ["перевод"]
        result = process_bank_operations_regex(data, categories)

        assert result["перевод"] == 2

    def test_case_insensitive_count(self):
        data = [
            {"description": "ПЕРЕВОД организации", "amount": 1000},
            {"description": "оплата услуг", "amount": -500},
            {"description": "Зарплата", "amount": 2000},
        ]

        categories = ["перевод", "оплата", "зарплата"]
        result = process_bank_operations_regex(data, categories)

        assert result["перевод"] == 1
        assert result["оплата"] == 1
        assert result["зарплата"] == 1

    def test_no_matching_categories(self):
        data = [
            {"description": "Перевод организации", "amount": 1000},
            {"description": "Оплата услуг", "amount": -500},
        ]

        categories = ["инвестиции", "кредит"]
        result = process_bank_operations_regex(data, categories)

        assert result["инвестиции"] == 0
        assert result["кредит"] == 0

    def test_empty_data(self):
        result = process_bank_operations_regex([], ["перевод", "оплата"])
        assert result == {}

    def test_empty_categories(self):
        data = [
            {"description": "Перевод организации", "amount": 1000},
        ]

        result = process_bank_operations_regex(data, [])
        assert result == {}


def test_integration_both_functions():
    data = [
        {"description": "Перевод ООО Рога", "amount": 1000},
        {"description": "Оплата связи Билайн", "amount": -500},
        {"description": "Зарплата от ООО Рога", "amount": 2000},
        {"description": "Оплата интернета", "amount": -300},
    ]

    search_result = process_bank_search(data, "рога")
    assert len(search_result) == 2

    categories = ["перевод", "зарплата"]
    count_result = process_bank_operations_regex(search_result, categories)

    assert count_result["перевод"] == 1
    assert count_result["зарплата"] == 1
