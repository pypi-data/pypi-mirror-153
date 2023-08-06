from cjen import BigTangerine
from cjen.exceptions import _check_instance


def add(*, content: dict):
    def __wrapper__(func):
        @_check_instance(decorator="context.add", expect=BigTangerine)
        def __inner__(ins: BigTangerine, *args, **kwargs):
            ins.context.update(content)
            return func(ins, *args, **kwargs)

        return __inner__

    return __wrapper__


def remove(*, key: str):
    @_check_instance(decorator="context.remove", expect=BigTangerine)
    def __wrapper__(func):
        def __inner__(ins: BigTangerine, *args, **kwargs):
            ins.context.pop(key)
            return func(ins, *args, **kwargs)

        return __inner__

    return __wrapper__
