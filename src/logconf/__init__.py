from .dsl import DSLBase


def logconf(dsl_expression):
    return to_dict_recursive(dsl_expression)


def to_dict_recursive(start):
    if isinstance(start, (DSLBase, dict)):
        if isinstance(start, DSLBase):
            start = start.to_dict()

        return {k: to_dict_recursive(v) for k, v in start.items()}
    elif isinstance(start, list):
        return [to_dict_recursive(i) for i in start]
    else:
        return start

