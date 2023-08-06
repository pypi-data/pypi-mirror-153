
from cjen.bigtangerine import ContextManager


class MetaData(object):
    """
    无法配合使用 装饰器 @property
    """

    def __init__(self):
        self.cols = list(filter(
            lambda method: callable(getattr(self, method)) and not method.startswith("_") and not method.endswith(
                "_") and method != "factory" and method != "is_class"
            ,
            dir(self)))
        self.meta_data = dict.fromkeys(self.cols, None)
        self.meta_source = None
        self.context = ContextManager()


    @classmethod
    def is_class(cls, instance):
        return isinstance(instance, MetaData)

    @staticmethod
    def factory(*, clazz, data):
        meta = clazz()
        meta.meta_source = data
        return meta


class MetaJson(MetaData): ...


class MetaMysql(MetaData): ...
