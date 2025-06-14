import inspect
import functools


def strict(func):
    sig = inspect.signature(func)
    annotations = func.__annotations__

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        bound = sig.bind(*args, **kwargs)
        for name, value in bound.arguments.items():
            if name in annotations:
                expected = annotations[name]
                if type(value) is not expected:
                    raise TypeError(
                        f"Argument '{name}' must be of type {expected.__name__}, "
                        f"got {type(value).__name__}"
                    )
        return func(*args, **kwargs)

    return wrapper