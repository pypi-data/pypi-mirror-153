
from cjen import BigTangerine
from cjen.commons import _get_method_params
from cjen.exceptions import _check_method, _check_instance


def basicHeaders(*, headers: dict):

    """
    使用条件: 作用在 类型 BigTangerine 或 其子类的 对象

    位置：该装饰器一般放在 __init__ 函数中

    作用: 初始化Basic Header, Basic Header 是作为基准 Header 存在

    :param headers:
    :return:
    """
    def __wrapper__(func):
        # @_get_method_params(method=func)
        @_check_instance(decorator="headers.basicHeaders", expect=BigTangerine)
        @_check_method(decorator="headers.basicHeaders", method=func, expect="__init__")
        def __inner__(instance: BigTangerine, *args, **kwargs):
            instance.headers.update(headers)
            func(instance, *args, **kwargs)

        return __inner__

    return __wrapper__


def appendBasicHeaders(*, headers: dict):

    """
    使用条件: 作用在 类型 BigTangerine 或 其子类的 对象

    位置：Header 的 装饰器一般都放在顶层，在其它装饰器之前

    作用: 增加Basic Header

    :param headers:
    :return:
    """

    def __wrapper__(func):
        @_get_method_params(method=func)
        @_check_instance(decorator="headers.appendBasicHeaders", expect=BigTangerine)
        def __inner__(instance: BigTangerine, *args, **kwargs):
            instance.headers.update(headers)
            return func(instance, *args, **kwargs)

        return __inner__

    return __wrapper__


def accept(*, value: str):

    """
    使用条件: 作用在 类型 BigTangerine 或 其子类的 对象

    位置：针对装饰器所在的函数，发送请求时，临时新增的 Accept Header.

    作用: 新增临时 Accept Header

    :param value:
    :return:
    """

    def __wrapper__(func):
        @_get_method_params(method=func)
        @_check_instance(decorator="headers.accept", expect=BigTangerine)
        def __inner__(instance: BigTangerine, *args, **kwargs):
            kwargs["headers"] = {**kwargs.get("headers", {"Accept": value}), **{"Accept": value}}
            return func(instance, *args, **kwargs)

        return __inner__

    return __wrapper__


def contentType(*, value: str):

    """
    使用条件: 作用在 类型 BigTangerine 或 其子类的 对象

    位置：针对装饰器所在的函数，发送请求时，临时新增的 Content-Type Header.

    作用: 新增临时 Content-Type Header

    :param value:
    :return:
    """

    def __wrapper__(func):
        @_get_method_params(method=func)
        @_check_instance(decorator="headers.contentType", expect=BigTangerine)
        def __inner__(instance: BigTangerine, *args, **kwargs):
            kwargs["headers"] = {**kwargs.get("headers", {"Content-Type": value}), **{"Content-Type": value}}
            return func(instance, *args, **kwargs)

        return __inner__

    return __wrapper__


def addHeaders(*, headers: dict):
    """
    使用条件: 作用在 类型 BigTangerine 或 其子类的 对象

    位置：针对装饰器所在的函数，发送请求时，临时新增的Header.

    作用: 新增临时 Header

    :param headers:
    :return:
    """

    def __wrapper__(func):
        @_get_method_params(method=func)
        @_check_instance(decorator="headers.addHeaders", expect=BigTangerine)
        def __inner__(instance: BigTangerine, *args, **kwargs):
            kwargs["headers"] = {**kwargs.get("headers", headers), **headers}
            return func(instance, *args, **kwargs)

        return __inner__

    return __wrapper__
