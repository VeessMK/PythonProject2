import os

import pytest

from src.decorators import another_function, my_function


def test_log_exception_handling(capsys):
    """Тест обработки ошибок с выводом в консоль"""
    with pytest.raises(ZeroDivisionError):
        another_function(10, 0)

    captured = capsys.readouterr()
    console_output = captured.out

    assert "another_function started" in console_output
    assert "another_function error: ZeroDivisionError" in console_output
    assert "Inputs: (10, 0)" in console_output
    assert "another_function finished" not in console_output  # Исправлено


def test_another_function_type_error(capsys):
    """Тест обработки TypeError с выводом в консоль"""
    with pytest.raises(TypeError):
        another_function("10", 2)

    captured = capsys.readouterr()
    console_output = captured.out

    assert "another_function started" in console_output
    assert "another_function error: TypeError" in console_output
    assert "Inputs: ('10', 2)" in console_output


def test_function_success_execution(capsys):
    """Тест успешного выполнения функции"""
    # Очищаем файл перед тестом
    if os.path.exists("log.txt"):
        os.remove("log.txt")

    # Вызываем функцию с файловым логированием
    result = my_function(3, 4)
    assert result == 7

    # Проверяем вывод в консоль (должен быть пустым, так как используется файл)
    captured = capsys.readouterr()
    console_output = captured.out
    assert console_output == ""

    # Проверяем, что файл создан и содержит логи
    assert os.path.exists("log.txt")

    with open("log.txt", "r", encoding="utf-8") as f:
        log_content = f.read()

    assert "my_function started" in log_content
    assert "my_function finished" in log_content  # Исправлено
    assert "my_function error" not in log_content
    assert "args: (3, 4)" in log_content


def test_console_output_success(capsys):
    """Тест вывода в консоль при успешном выполнении"""
    result = another_function(10, 2)
    assert result == 5.0

    captured = capsys.readouterr()
    console_output = captured.out

    assert "another_function started" in console_output
    assert "another_function finished" in console_output  # Исправлено
    assert "args: (10, 2)" in console_output
