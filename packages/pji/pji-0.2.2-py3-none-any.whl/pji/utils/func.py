from hbutils.reflection import dynamic_call, sigsupply


def _empty_func(*args, **kwargs):
    pass


def wrap_empty(func):
    """
    wrap a function which can be None
    :param func: optional function
    :return: final function
    """

    if func:
        return dynamic_call(sigsupply(func, _empty_func))
    else:
        return _empty_func
