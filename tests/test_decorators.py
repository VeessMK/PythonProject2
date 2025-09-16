import os

import pytest

from src.decorators import another_function, log


def test_log_exception_handling(capsys):

    with pytest.raises(ZeroDivisionError):
        another_function(10, 0)

    captured = capsys.readouterr()
    console_output = captured.out

    assert "another_function started" in console_output
    assert "another_function error: ZeroDivisionError" in console_output
    assert "Inputs: (10, 0)" in console_output


def test_another_function_type_error(capsys):
    with pytest.raises(TypeError):
        another_function("10", 2)

    captured = capsys.readouterr()
    console_output = captured.out

    assert "another_function error: TypeError" in console_output
    assert "Inputs: ('10', 2)" in console_output


def test_function_success_execution():
    if os.path.exists("log.txt"):
        os.remove("log.txt")

        assert "my_function ok" in log
        assert log.count("my_function ok") == 2
        assert "my_function error" not in log
