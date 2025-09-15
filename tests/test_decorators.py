from src.decorators import my_function


def test_expected_result(capsys):
    my_function(10, 20)
    capsys.readouterr()
    assert "my_function ok, result is: 30"


def test_typeerror_crash(capsys):
    my_function("10", 20)
    capsys.readouterr()
    assert "my_function error: TypeError. Inputs: ('10', 20), {}"


def test_str_input(capsys):
    my_function("a", "b")
    capsys.readouterr()
    assert "my_function ok, result is: ab"
