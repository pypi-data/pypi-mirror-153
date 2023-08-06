import importlib


def import_string(dotted_path):
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError:
        raise ImportError(
            '{} doesn\'t look like a module path'.format(dotted_path),
        )

    module = importlib.import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError:
        raise ImportError(
            'Module "{}" does not define a "{}" attribute/class'.format(
                module_path,
                class_name,
            ),
        )
