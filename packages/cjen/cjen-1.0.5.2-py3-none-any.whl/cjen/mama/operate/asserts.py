from cjen import BigTangerine
from cjen.commons import _get_method_params
from cjen.exceptions import _check_instance, _check_meta_exist, _un_support_char
from cjen.mama.meta_data import MetaData

ALL_FIELDS = "ALL_FIELDS"


# TODO 待实现
def validation_all_metas(func):
    """
    使用条件: BigTangerine 及其 子类 对象

    位置：json.factory 或 mysql.factory 之后

    作用：执行对象函数所有 MetaData 参数的中含有asserts装饰器的方法
    :param func:
    :return:
    """

    @_get_method_params(method=func)
    @_check_instance(decorator="orange.assert.validation_fields", expect=BigTangerine)
    def __inner__(ins: BigTangerine, *args, **kwargs):
        pass

    return __inner__


# TODO 增加对装饰器的判断，看是否有 asserts
def validation_meta(*, meta_name: str, fields: str = ALL_FIELDS):
    """
    使用条件: BigTangerine 及其 子类 对象

    位置：json.factory 或 mysql.factory 之后

    作用：指定执行对象函数中 MetaData 参数的中含有asserts装饰器的方法

    :param meta_name: 参数名
    :param fields: 需要执行校验的Field名, 默认是所有Filed, 指定多个以";"分割  例如 "field1;filed2"
    :return:
    """

    def __wrapper__(func):
        @_get_method_params(method=func)
        @_check_meta_exist(meta_name=meta_name)
        @_un_support_char(content=fields, char="；", err_msg=f"orange.assert.validation_fields Please not use chinese ；")
        @_check_instance(decorator="orange.assert.validation_fields", expect=BigTangerine)
        def __inner__(ins: BigTangerine, *args, **kwargs):
            metas = kwargs.get(meta_name) if type(kwargs.get(meta_name)) == list else [kwargs.get(meta_name)]

            for meta in metas:
                method_names = list(filter(
                    lambda method: callable(getattr(meta, method)) and not method.startswith(
                        "_") and not method.endswith(
                        "_") and method != "factory" and method != "is_class"
                    ,
                    dir(meta)))

                if fields == ALL_FIELDS:  # 执行所有的参数校验
                    for method_name in method_names:
                        getattr(meta, method_name)()
                else:  # 执行部分校验
                    for field in fields.split(";"):
                        if field in method_names:
                            getattr(meta, field)()
                        else:
                            raise Exception(f'{meta_name} do not have {field}')
            return func(ins, *args, **kwargs)

        return __inner__

    return __wrapper__


def required(func):
    """
    使用条件：MetaData 及其 子类对象
    位置： 不限
    作用：验证某个字段非空
    :param func:
    :return:
    """

    @_check_instance(decorator="operate.assert.required", expect=MetaData)
    def __inner__(self, *args, **kwargs):
        field = func(self, *args, **kwargs) if func.__name__ == '__inner__' else func.__name__
        assert self.meta_data.get(field) is not None, f"{field} must not null"
        return field

    return __inner__


def not_equal(*, value):
    """
    使用条件：MetaData 及其 子类对象
    位置： 不限
    作用：验证某个字段不等于某一个值
    :param value:
    :return:
    """

    def __wrapper__(func):
        def __inner__(self, *args, **kwargs):
            field = func(self, *args) if func.__name__ == '__inner__' else func.__name__
            assert self.meta_data.get(field) == value, f"{self.meta_data.get(field)} should equal {value}"
            return field

        return __inner__

    return __wrapper__


def equal(*, value):
    """
    使用条件：MetaData 及其 子类对象
    位置： 不限
    作用：验证某个字段等于某一个值
    :param value:
    :return:
    """

    def __wrapper__(func):
        def __inner__(self, *args, **kwargs):
            field = func(self, *args, **kwargs) if func.__name__ == '__inner__' else func.__name__
            assert self.meta_data.get(field) == value, f"{self.meta_data.get(field)} should equal {value}"
            return field

        return __inner__

    return __wrapper__


def in_range(*, ranges: list):
    """
    使用条件：MetaData 及其 子类对象
    位置： 不限
    作用：验证某个字段的值在某个范围内
    :param ranges:
    :return:
    """

    def __wrapper__(func):
        def __inner__(self, *args, **kwargs):
            field = func(self, *args) if func.__name__ == '__inner__' else func.__name__

            assert self.meta_data.get(field) in ranges, f"{self.meta_data.get(field)} is not in  {ranges}"
            return field

        return __inner__

    return __wrapper__


def not_in_range(*, ranges: list):
    """
    使用条件：MetaData 及其 子类对象
    位置： 不限
    作用：验证某个字段的值不在某个范围内
    :param ranges:
    :return:
    """

    def __wrapper__(func):
        def __inner__(self, *args, **kwargs):
            field = func(self, *args) if func.__name__ == '__inner__' else func.__name__
            assert self.meta_data.get(field) not in ranges, f"{self.meta_data.get(field)} is in  {ranges}"
            return field

        return __inner__

    return __wrapper__
