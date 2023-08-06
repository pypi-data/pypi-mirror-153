import jsonpath

from cjen import BigTangerine
from cjen.commons import _get_method_params
from cjen.exceptions import JsonPathNotFoundErr, _check_instance, _check_params_factory
from cjen.mama.meta_data import MetaData, MetaJson


def factory(*, clazz):
    """
    使用条件: 作用在 类型 BigTangerine 或 其子类的 对象


    位置：放在http.post_mapping 等请求装饰器之后

    作用: 生成 MetaJson 对象

    注意：1. 只支持 obj:Class ，不支持 list[Class] 类型

    :param clazz: MetaJson 或其 子类
    :return: 返回单个对象
    """

    def __wrapper__(func):
        @_get_method_params(method=func)
        @_check_params_factory(clazz=MetaJson)
        @_check_instance(decorator="operate.json.factory", expect=BigTangerine)
        def __inner__(ins: BigTangerine, *args, **kwargs):
            for key, value in kwargs.get("method.__annotations__").items():
                if issubclass(value, MetaJson):
                    kwargs[key] = MetaData.factory(clazz=clazz, data=kwargs.get("resp"))
                    # 同步上下文
                    # 把BigTangerine 中的 上下文同步到 MetaData中的上下文
                    if ins.context:
                        kwargs[key].context.update(ins.context)
            return func(ins, *args, **kwargs)

        def __empty__(ins: BigTangerine, *args, **kwargs):
            return func(ins, *args, **kwargs)

        if clazz is None: return __empty__
        return __inner__

    return __wrapper__


def one(*, json_path: str):
    """
    使用条件: 作用在 类型 BigTangerine 或 其子类的 对象

    位置：紧接被装饰函数，与 many 可调换顺序

    作用: 从Json对象中

    使用注意：
        1. 只支持 obj:Class ，不支持 list[Class] 类型
    :return:
    """

    def __wrapper__(func):
        @_get_method_params(method=func)
        @_check_instance(decorator="operate.json.one", expect=MetaData)
        def __inner__(ins: MetaData, *args, **kwargs):
            field = func(ins, *args, **kwargs) if func.__name__ == '__inner__' else func.__name__

            json_data = jsonpath.jsonpath(ins.meta_source, json_path.format(**ins.context.content))
            if not json_data:
                raise JsonPathNotFoundErr(f"can not get the data from {json_path.format(**ins.context.content)}")
            ins.meta_data[field] = json_data[0]
            return field

        return __inner__

    return __wrapper__



def listOf(*, clazz):
    def __wrapper__(func):
        @_get_method_params(method=func)
        @_check_instance(decorator="operate.json.many", expect=MetaData)
        def __inner__(ins: MetaData, *args, **kwargs):
            field = func(ins, *args, **kwargs) if func.__name__ == '__inner__' else func.__name__
            ins.meta_data[field] = [MetaJson.factory(clazz=clazz, data=data) for data in ins.meta_data.get(field)]
            return field

        return __inner__

    return __wrapper__


def many(*, json_path: str, filter_keys: list[str] = None):
    """
    使用条件: 作用在 类型 BigTangerine 或 其子类的 对象

    位置：紧接被装饰函数，与 one 可调换顺序

    适用场景：在 json文件中选择匹配某个属性 {
        user:[
            {name="甲", type="1"},

            {name="乙", type="1"},

            {name="丙", type="2"},

        ]

    }
    的所有值,选取符合"$.user[?＠type==1]"的所有值
    作用: 从Json对象中获取满足条件的值

    :param json_path:
    :param filter_keys: 获取指定的Key-Value，如果不设置的则获取所有的Key-Value
    :return: 返回为一个list对象
    """

    def __wrapper__(func):
        @_get_method_params(method=func)
        @_check_instance(decorator="operate.json.many", expect=MetaData)
        def __inner__(ins: MetaData, *args, **kwargs):
            field = func(ins, *args, **kwargs) if func.__name__ == '__inner__' else func.__name__
            json_data = jsonpath.jsonpath(ins.meta_source, json_path)
            if not json_data: raise JsonPathNotFoundErr(f"can not get the data from {json_path}")

            ins.meta_data[field] = json_data if not filter_keys else [dict(
                zip(filter_keys, [obj.get(key) for key in filter_keys])) for obj in json_data]
            return field


        return __inner__

    return __wrapper__

