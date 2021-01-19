def decorator(func):
    def wrapper(main_arg, *args, **kwargs):
        print(main_arg, *args, **kwargs)
        return func(main_arg, *args, **kwargs)
    return wrapper


@decorator
def my_func(a, b, c=0):
    return a + b + c


print(my_func(1, 2, 3))