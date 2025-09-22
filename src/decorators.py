import datetime
from functools import wraps


def log(filename=None):
    """
    Автоматически логирует начало и конец функции, а также её результаты и ошибки.
    Ошибки всегда выводятся в консоль, даже если задан файл.
    """

    def write_log(message, is_error=False):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"

        # Всегда выводим ошибки в консоль
        if is_error or filename is None:
            print(log_message)

        # Если задан файл, пишем все логи в файл
        if filename:
            with open(filename, "a", encoding="utf-8") as file:
                file.write(f"{log_message}\n")

    def inner(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            inputs = f"args: {args}, kwargs: {kwargs}"
            write_log(f"{function.__name__} started. {inputs}")

            try:
                result = function(*args, **kwargs)
                write_log(f"{function.__name__} finished. Result: {result}")
                return result

            except Exception as e:
                error_message = f"{function.__name__} error: {type(e).__name__}: {str(e)}. Inputs: {args}, {kwargs}"
                write_log(error_message, is_error=True)
                raise

        return wrapper

    return inner


@log(filename="log.txt")
def my_function(x, y):
    return x + y


@log()
def another_function(a, b):
    return a / b
