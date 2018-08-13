import functools
import json


def to_json(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        result = func(*args, **kwargs)
        t = json.dumps(result)
        print(t)
        return t

    return wrapped


@to_json
def get_data():
    return {
        'data': 42
    }


# print(get_data())  # вернёт '{"data": 42}'
