from cjen.mama.meta_data import MetaData


def value(func):
    """
    使用条件：MetaData 或 其子类使用

    位置： 装饰函数的顶层装饰器
    作用: 返回 MetaData 中 属性的值
    :param func:
    :return:


    使用场景：如果期望返回 MetaData中定义的 Field的值，则需使用该装饰器

    位置： 装饰函数的顶层装饰器

    作用: 返回 MetaData 中 属性的值

    :param func:
    :return: 返回字段值

    """

    def __inner__(ins: MetaData, *args, **kwargs):
        field = func(ins, *args, **kwargs) if func.__name__ == '__inner__' else func.__name__
        return ins.meta_data.get(field)

    return __inner__


# TODO 待实现
def change_key_in_dict(*, source: list[str], change_to: list[str]):
    def __wrapper__(func):
        def __inner__(ins: MetaData, *args, **kwargs):
            pass

        return __inner__

    return __wrapper__


# TODO 待实现
def change_key_in_list(*, source: list[str], change_to: list[str]):
    def __wrapper__(func):
        def __inner__(ins: MetaData, *args, **kwargs):
            pass

        return __inner__

    return __wrapper__
