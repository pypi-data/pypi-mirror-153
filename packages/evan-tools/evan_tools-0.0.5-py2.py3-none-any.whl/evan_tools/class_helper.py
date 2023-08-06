import functools


def to_string(fn=None, *, symbol="_"):
    if fn is None:
        return functools.partial(to_string, symbol=symbol)

    def string(self):
        items = [f"{k}={v}" for k, v in self.__dict__.items() if not k.startswith(symbol)]
        return f"{self.__class__.__name__} ({', '.join(items)})"

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        fn.__str__ = string
        return fn(*args, **kwargs)

    return wrapper
