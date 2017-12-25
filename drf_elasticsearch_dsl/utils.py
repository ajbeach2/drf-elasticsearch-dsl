import importlib


def load_class(class_string):
    if(class_string is None):
        return None

    last = 0
    for e in reversed(class_string):
        if(e is "."):
            break
        else:
            last -= 1

    module = class_string[:last - 1]
    class_name = class_string[last:]

    return getattr(importlib.import_module(module), class_name)
