import datetime
from functools import wraps


def log(filename=None):
    """
    Автоматически логирует начало и конец функции, а также её результаты и ошибки.
    """

    def write_log(message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"

        if filename:
            with open(filename, "a", encoding="utf-8") as file:
                file.write(f"{log_message}\n")
        else:
            print(log_message)

    def inner(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            inputs = f"args: {args}, kwargs: {kwargs}"
            write_log(f"{function.__name__} started. {inputs}")

            try:
                result = function(*args, **kwargs)
                write_log(f"{function.__name__} ok.")
                return result

            except Exception as e:
                error_message = f"{function.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}"
                write_log(error_message)
                raise

        return wrapper

    return inner


@log(filename="log.txt")
def my_function(x, y):
    return x + y


@log()
def another_function(a, b):
    return a / b
