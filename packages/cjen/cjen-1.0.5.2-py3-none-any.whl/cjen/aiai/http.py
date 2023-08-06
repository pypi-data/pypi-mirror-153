import datetime
import os
from enum import unique, Enum
from typing import IO

import requests
import yaml
from requests_toolbelt import MultipartEncoder

import cjen
from cjen.mama.operate.json import factory
from cjen.bigtangerine import BigTangerine
from cjen.commons import _get_method_params
from cjen.exceptions import _check_uri, NetWorkErr, _check_instance
import cjen.dada.smile


def url_log_content(resp, log_type):
    date = datetime.datetime.now().strftime('%y-%m-%d %I:%M:%S')
    method = resp.request.method
    url = resp.url
    return "{date} {log_type} {method} {url}\n".format(date=date, log_type=log_type, method=method, url=url)


def body_log_content(resp, io: IO):
    request_body_content(resp.request.body, io)
    response_body_content(resp.content, io)


def request_body_content(request_body, io: IO):
    if request_body and type(request_body) == bytes:
        io.write("  -- request {request_body}\n".format(request_body=str(request_body, encoding="UTF-8")))
    if request_body and type(request_body) == MultipartEncoder:
        io.write("  -- request {request_body}\n".format(request_body=str(request_body)))


def response_body_content(resp_body, io: IO):
    if resp_body:
        io.write("  -- response {resp_body}\n".format(resp_body=str(resp_body, encoding="UTF-8")))


@cjen.haha(LogPath=os.getcwd(), LogName="httpd.log", Mode='a')
def httpd_log(resp, io: IO):
    io.write(url_log_content(resp, "info"))
    body_log_content(resp, io)


@cjen.haha(LogPath=os.getcwd(), LogName="httpd.log", Mode='a')
def httpd_err_log(resp, io: IO):
    io.write(url_log_content(resp, "error"))
    body_log_content(resp, io)


@cjen.haha(LogPath=os.getcwd(), LogName="httpd.log", Mode='a')
def httpd_connection_err_log(err, io: IO):
    date = datetime.datetime.now().strftime('%y-%m-%d %I:%M:%S')
    io.write("{date} error {err}\n".format(date=date, err=str(err)))


def _multipart_form(func):
    def __inner__(ins: BigTangerine, *args, **kwargs):
        data_form = kwargs.get("data")
        files = {}
        others = {}
        for k, v in data_form.items():
            if os.path.exists(v) and os.path.isfile(v):
                files[k] = v
            else:
                others[k] = v
        if not files: raise Exception("there is no file!")
        for k, v in files.items():
            with open(v, 'rb') as f:
                *rest, postfix = f.name.split(".")
                files[k] = (os.path.basename(f.name), f.read(), _file_type(file_postfix=f".{postfix}"))

        kwargs["form_data"] = MultipartEncoder(fields={**files, **others})
        ins.headers["Content-Type"] = kwargs["form_data"].content_type
        return func(ins, *args, **kwargs)

    return __inner__


def _file_type(*, file_postfix):
    with open(os.path.join(os.path.dirname(__file__), "file-content-type.yaml"), "r") as f:
        content_type = yaml.load(f.read(), Loader=yaml.FullLoader).get("ContentType")
        if content_type.get(file_postfix):
            return content_type.get(file_postfix)
    raise Exception(f"{file_postfix} can not support !")


@unique
class ContentType(Enum):
    JSON = "json"
    FILE_STREAM = "stream"


def _response(func):
    def __inner__(ins: BigTangerine, *args, **kwargs):
        if kwargs.get("resp").status_code == 200:
            httpd_log(kwargs.get("resp"))
            if "application/json" in kwargs.get("resp").headers.get("Content-Type"):
                kwargs["response_content"] = kwargs.get("resp")

                kwargs["resp"] = kwargs.get("resp").json() if kwargs.get("resp").content else None

                return func(ins, *args, **kwargs)
            kwargs["resp"] = kwargs.get("resp").content
            return func(ins, *args, **kwargs)
        else:
            httpd_err_log(kwargs.get("resp"))
            raise NetWorkErr(f'{kwargs.get("url")} {kwargs.get("resp").status_code}')

    return __inner__


def _url(*, uri: str):
    def __wrapper__(func):
        def __inner__(ins: BigTangerine, *args, **kwargs):
            path_variable = kwargs.get("path_variable")
            kwargs["url"] = "/".join([ins.base_url, uri])
            if path_variable:
                kwargs["url"] = kwargs["url"].format(**path_variable)
            return func(ins, *args, **kwargs)

        return __inner__

    return __wrapper__


def base_url(*, uri: str):
    def __wrapper__(func):
        def __inner__(ins: BigTangerine, *args, **kwargs):
            ins.__setattr__("base_url", uri)
            return func(ins, *args, **kwargs)

        return __inner__

    return __wrapper__


def _delete(func):
    @_http_headers
    @_http_json(method=requests.delete)
    @_http_default(method=requests.delete)
    def __inner__(ins: BigTangerine, *args, **kwargs):
        return func(ins, *args, **kwargs)

    return __inner__


# def _get(func):
#     def __inner__(ins: BigTangerine, *args, **kwargs):
#         headers = {**ins.headers, **kwargs.get("headers")} if kwargs.get("headers") else ins.headers
#         kwargs["resp"] = requests.get(url=kwargs["url"], headers=headers,
#                                       params=kwargs.get("params"))


def _http_headers(func):
    def __inner__(ins: BigTangerine, *args, **kwargs):
        kwargs["headers"] = {**ins.headers, **kwargs.get("headers")} if kwargs.get("headers") else ins.headers
        return func(ins, *args, **kwargs)

    return __inner__


def _resp_is_not_none(**kwargs): return kwargs.get("resp") is None


def _have_content_type(**kwargs): return kwargs["headers"].get("Content-Type") is not None


def _is_json(**kwargs): return "json" in kwargs["headers"].get("Content-Type")


def _is_upload(**kwargs): return "multipart/form-data" in kwargs["headers"].get("Content-Type")


def _http_json(*, method):
    def __wrapper__(func):
        def __inner__(ins: BigTangerine, *args, **kwargs):
            if _resp_is_not_none(**kwargs) and _have_content_type(**kwargs) and _is_json(**kwargs):
                try:
                    kwargs["resp"] = method(url=kwargs["url"], headers=kwargs["headers"], json=kwargs.get("data"))
                except OSError as err:
                    httpd_connection_err_log(err)
            return func(ins, *args, **kwargs)

        return __inner__

    return __wrapper__


def _http_file(*, method):
    def __wrapper__(func):
        def __inner__(ins: BigTangerine, *args, **kwargs):
            if _resp_is_not_none(**kwargs) and _have_content_type(**kwargs) and _is_upload(**kwargs):
                try:
                    kwargs["resp"] = method(url=kwargs["url"], headers=kwargs["headers"], data=kwargs.get("form_data"))
                except OSError as err:
                    httpd_connection_err_log(err)
            return func(ins, *args, **kwargs)

        return __inner__

    return __wrapper__


def _http_default(*, method):
    def __wrapper__(func):
        def __inner__(ins: BigTangerine, *args, **kwargs):
            if _resp_is_not_none(**kwargs):
                try:
                    kwargs["resp"] = method(url=kwargs["url"], headers=kwargs["headers"], data=kwargs.get("data"))
                except OSError as err:
                    httpd_connection_err_log(err)
            return func(ins, *args, **kwargs)

        return __inner__

    return __wrapper__


def _get(func):
    def __inner__(ins: BigTangerine, *args, **kwargs):
        headers = {**ins.headers, **kwargs.get("headers")} if kwargs.get("headers") else ins.headers
        kwargs["resp"] = requests.get(url=kwargs["url"], headers=headers, params=kwargs.get("params"))

        return func(ins, *args, **kwargs)

    return __inner__


def _post(func):
    @_http_headers
    @_http_json(method=requests.post)
    @_http_file(method=requests.post)
    @_http_default(method=requests.post)
    def __inner__(ins: BigTangerine, *args, **kwargs):
        return func(ins, *args, **kwargs)

    return __inner__


def _put(func):
    @_http_headers
    @_http_json(method=requests.put)
    @_http_default(method=requests.put)
    def __inner__(ins: BigTangerine, *args, **kwargs):
        return func(ins, *args, **kwargs)

    return __inner__


def get_mapping(*, uri: str, json_clazz=None):
    """
    使用范围：BigTangerine 或其 子类对象

    位置：装饰函数的上层装饰器. 如果有使用Header装饰器，在Header装饰器之后，如果没有 则是顶层装饰器

    发送 GET 请求，并返回结果

    :param json_clazz: 如果期望返回数据直接生成MetaJson, 则指定该生成的类型
    :param uri:
    :return:
    """

    def __wrapper__(func):
        @_get_method_params(method=func)
        @_check_instance(decorator="http.get_mapping", expect=BigTangerine)
        @_check_uri(uri=uri)
        @_url(uri=uri)
        @_get
        @_response
        @factory(clazz=json_clazz)
        def __inner__(ins: BigTangerine, *args, **kwargs):
            func(ins, *args, **kwargs)
            return kwargs.get("resp")

        return __inner__

    return __wrapper__


def post_mapping(*, uri: str, json_clazz=None):
    """
    使用范围：BigTangerine 或其 子类对象

    位置：装饰函数的上层装饰器，如果有使用Header装饰器，在Header装饰器之后，如果没有 则是顶层装饰器

    发送 Post 请求，并返回结果

    :param json_clazz:

    :param uri:
    :return:
    """

    def __wrapper__(func):
        @_get_method_params(method=func)
        @_check_instance(decorator="http.post_mapping", expect=BigTangerine)
        @_check_uri(uri=uri)
        @_url(uri=uri)
        @_post
        @_response
        @factory(clazz=json_clazz)
        def __inner__(ins: BigTangerine, *args, **kwargs):
            func(ins, *args, **kwargs)
            return kwargs.get("resp")

        return __inner__

    return __wrapper__


def put_mapping(*, uri: str, json_clazz=None):
    """
    使用范围：BigTangerine 或其 子类对象

    位置：装饰函数的上层装饰器，如果有使用Header装饰器，在Header装饰器之后，如果没有 则是顶层装饰器

    发送 PUT 请求，并返回结果

    :param json_clazz:

    :param uri:
    :return:
    """

    def __wrapper__(func):
        @_get_method_params(method=func)
        @_check_instance(decorator="http.put_mapping", expect=BigTangerine)
        @_check_uri(uri=uri)
        @_url(uri=uri)
        @_put
        @_response
        @factory(clazz=json_clazz)
        def __inner__(ins: BigTangerine, *args, **kwargs):
            func(ins, *args, **kwargs)
            return kwargs.get("resp")

        return __inner__

    return __wrapper__


def upload_mapping(*, uri: str, json_clazz=None):
    """
    使用范围：BigTangerine 或其 子类对象

    位置：装饰函数的上层装饰器，如果有使用Header装饰器，在Header装饰器之后，如果没有 则是顶层装饰器

    发送 上传文件 请求，并返回结果

    :param json_clazz:
    :param uri:
    :return:
    """

    def __wrapper__(func):
        @_get_method_params(method=func)
        @_check_instance(decorator="http.upload_mapping", expect=BigTangerine)
        @_check_uri(uri=uri)
        @_url(uri=uri)
        @_multipart_form
        @_post
        @_response
        @factory(clazz=json_clazz)
        def __inner__(ins: BigTangerine, *args, **kwargs):
            func(ins, *args, **kwargs)
            return kwargs.get("resp")

        return __inner__

    return __wrapper__


def delete_mapping(*, uri: str, json_clazz=None):
    """
    使用范围：BigTangerine 或其 子类对象

    位置：位置：装饰函数的上层装饰器，如果有使用Header装饰器，在Header装饰器之后，如果没有 则是顶层装饰器

    发送 delete 请求，并返回结果

    :param json_clazz:
    :param uri:
    :return:
    """

    def __wrapper__(func):
        @_get_method_params(method=func)
        @_check_instance(decorator="http.delete_mapping", expect=BigTangerine)
        @_check_uri(uri=uri)
        @_url(uri=uri)
        @_delete
        @_response
        @factory(clazz=json_clazz)
        def __inner__(ins: BigTangerine, *args, **kwargs):
            func(ins, *args, **kwargs)
            return kwargs.get("resp")

        return __inner__

    return __wrapper__
