import re
import warnings


class MethodWrongErr(Exception): ...


class InstanceWrongErr(Exception): ...


class JwtWrongErr(Exception): ...


class RequestParamErr(Exception): ...


class NetWorkErr(Exception): ...


class JsonPathNotFoundErr(Exception): ...


class FactoryParamsWarning(UserWarning): ...


class NoMetaErr(Exception): ...


class UnSupportCharErr(Exception): ...


def _check_method(*, decorator: str, method, expect):
    def __wrapper__(func):
        def __inner__(ins, *args, **kwargs):
            if not method.__name__ == expect: raise MethodWrongErr(f"{decorator} should on the {expect} method")
            return func(ins, *args, **kwargs)

        return __inner__

    return __wrapper__


def _check_instance(*, decorator: str, expect):
    def __wrapper__(func):
        def __inner__(ins, *args, **kwargs):
            if not expect.is_class(ins): raise InstanceWrongErr(f"{decorator} should on the {expect.__name__}")
            return func(ins, *args, **kwargs)

        return __inner__

    return __wrapper__


def _check_uri(*, uri: str):
    def __wrapper__(func):
        def __inner__(ins, *args, **kwargs):
            for variable in re.findall(r'{(\w+)}', uri):
                if not kwargs.get("path_variable"):
                    raise RequestParamErr(f"{uri} contain variable,the params must have 'path_variable'")
                if type(kwargs.get("path_variable")) != dict:
                    raise RequestParamErr("path_variable must is dict")
                if not kwargs.get("path_variable").get(variable):
                    raise RequestParamErr(f"{uri} contain {variable}, but path_variable do not have '{variable}'")
            return func(ins, *args, **kwargs)

        return __inner__

    return __wrapper__


def _check_params_factory(*, clazz):
    """
    检查 调用 Factory装饰器时，函数参数中是否包含 Meta 对象
    如果 传入的参数包含多个参数则提示错误
    :param clazz:  MetaJson 或 MetaMysql
    :return:
    """

    def __wrapper__(func):
        def __inner__(ins, *args, **kwargs):

            params = kwargs.get("method.__annotations__").values()
            # 计算是否包含形如 obj: clazz 这样的参数
            count = len(list(filter(lambda param: issubclass(param, clazz), params)))
            # 计算是否包含形如 obj: list[clazz] 这样的参数
            if count != 1:
                count += len(list(
                    filter(lambda param: param.__origin__ == list and issubclass(param.__args__[0], clazz), params)))
            # 只能包含其中的任一一个
            if count != 1: warnings.warn(f"{clazz} params number should = 1, Now {count}", FactoryParamsWarning)
            return func(ins, *args, **kwargs)

        return __inner__

    return __wrapper__


def _check_meta_exist(*, meta_name: str):
    def __wrapper__(func):
        def __inner__(ins, *args, **kwargs):
            if not kwargs.get(meta_name):
                raise NoMetaErr(f'{meta_name} is not exists')
            return func(ins, *args, **kwargs)

        return __inner__

    return __wrapper__


def _un_support_char(*, content: str, char: str, err_msg: str):
    def __wrapper__(func):
        def __inner__(ins, *args, **kwargs):
            if char in content:
                raise UnSupportCharErr(err_msg)
            return func(ins, *args, **kwargs)

        return __inner__

    return __wrapper__
