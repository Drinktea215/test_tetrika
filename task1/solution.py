def strict(func):
    annotations = func.__annotations__

    def wrapper(*args, **kwargs):
        for name, value in zip(func.__code__.co_varnames, args):
            if name in annotations and not isinstance(value, annotations[name]):
                raise TypeError
        return func(*args, **kwargs)

    return wrapper


@strict
def sum_two(a: int, b: int) -> int:
    return a + b

if __name__ == '__main__':
    print(sum_two(1, 2))  # >>> 3
    print(sum_two(1, 2.4))  # >>> TypeError
