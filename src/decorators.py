from functools import wraps


def log(filename=None):
    def inner(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            try:
                result = function(*args, **kwargs)
                report = f"{function.__name__} ok, result is: {result}"
                if filename:
                    with open(filename, "a") as file:
                        file.write(f"{report}\n")
                print(report)
            except Exception as e:
                report = f"{function.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}"
                if filename:
                    with open(filename, "a") as file:
                        file.write(f"{report}\n")
                print(report)

        return wrapper

    return inner


@log("log")
def my_function(x, y):
    return x + y


my_function("10", 20)
