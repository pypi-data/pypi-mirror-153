from cjen.sco.step_definitions import StepDefinitions


class ContextArgs(dict):
    def __init__(self, seq=None, **kwargs):
        if seq:
            super(ContextArgs, self).__init__(seq, **kwargs)
        else:
            super(ContextArgs, self).__init__(**kwargs)


class ContextManager(object):
    def __init__(self):
        self.__cache = {}

    def update(self, E=None, **F):
        if E is not None and isinstance(E, ContextManager):
            self.__cache.update(E.__cache, **F)
        elif E is not None:
            self.__cache.update(E, **F)
        else:
            self.__cache.update(**F)

    def pick_up(self, *, context_args: ContextArgs):
        return dict(zip(list(context_args.keys()), [self.get(key) for key in list(context_args.values())]))

    @property
    def content(self):
        return self.__cache

    def pop(self, key):
        return self.__cache.pop(key)

    def get(self, key):
        return self.__cache.get(key)

    def __getitem__(self, key):
        return self.__cache.__getitem__(key)

    def __setitem__(self, key, value):
        self.__cache.__setitem__(key, value)


class BigTangerine(object):
    """
    主要的工作类，运行的对象需继承改类型，才能使用一系列装饰器

    定义的方法主要可以如下几种例子:

        针对 POST 请求:

        def method_name(self, data, resp=None, meta_json:MetaJson=None, meta_mysql:MetaMysql=None, **kwargs)

        针对 GET 请求:

        def method_name(self, params, resp=None, meta_json:MetaJson=None, meta_mysql:MetaMysql=None, **kwargs)

        针对 PUT:

        def method_name(self, data, resp=None, meta_json:MetaJson=None, meta_mysql:MetaMysql=None, **kwargs)

        针对 url 中带有参数的请求,以 POST 请求为例:

        def method_name(self, path_variable:dict, data, resp=None, meta_json:MetaJson=None, meta_mysql:MetaMysql=None, **kwargs)
    参数的解释

        data, params, path_variable 为请求参数，根据请求类型固定名称

        resp 为接口返回内容，参数名为固定

        meta_json: 可选参数 需搭配@orange.json.factory 使用

        meta_mysql: 可选参数 需搭配@orange.mysql.factory 使用

        ** kwarg: 固定写法

    """

    def __init__(self): ...

    def __new__(cls, *args, **kwargs):
        self = super(BigTangerine, cls).__new__(cls)
        self.headers = {}
        self.context = ContextManager()
        cls.check_methods(self)
        self.step_definitions = StepDefinitions()
        return self

    # TODO 增加BigTangerine 中定义方法的检查
    @classmethod
    def check_methods(cls, ins): pass

    @classmethod
    def is_class(cls, instance):
        return isinstance(instance, BigTangerine)
