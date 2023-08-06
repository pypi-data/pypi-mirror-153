import jsonpath

from cjen import BigTangerine
from enum import Enum

from cjen.commons import _get_method_params
from cjen.exceptions import JwtWrongErr


class JWTFrom(Enum):
    BODY = 0,
    HEADER = 1


class JWTAction(Enum):
    INIT = 101
    EXCHANGE = 102
    REFRESH = 103


def jwt(*, key: str, json_path: str, jwt_from: JWTFrom = JWTFrom.BODY, action: JWTAction = JWTAction.INIT):
    """
    主要用于JWT登陆方式:1. 在Header中初始化 jwt token,2. 在Header中交换 jwt token

    目前只支持返回格式为json

    :param action: INIT: 登陆时获取token, EXCHANGE: 中间过程交换token, REFRESH:接口交互中实时刷新token
    :param jwt_from: 用于交换的token的位置 JWTFrom.BODY 响应体中, JWTFrom.HEADER 响应头中
    :param key: header中 存放token的key
    :param json_path: 获取token 的json 路径
    :return:
    """

    def __wrapper__(func):
        # @_get_method_params(method=func)
        def __inner__(ins: BigTangerine, *args, **kwargs):
            rsp = kwargs.get("resp") if jwt_from == JWTFrom.BODY else dict(kwargs.get("response_content").headers)
            if not jsonpath.jsonpath(rsp, json_path):
                if action == JWTAction.INIT or action == JWTAction.EXCHANGE:
                    raise JwtWrongErr(f"can not find jwt key in {rsp}")
            else:
                ins.headers[key] = jsonpath.jsonpath(rsp, json_path)[0] if json_path else rsp
            return func(ins, *args, **kwargs)

        return __inner__

    return __wrapper__