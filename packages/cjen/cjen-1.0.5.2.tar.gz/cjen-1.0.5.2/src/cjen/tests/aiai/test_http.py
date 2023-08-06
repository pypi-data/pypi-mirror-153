import os.path

import allure
import cjen
from cjen import BigTangerine


class MockService(BigTangerine):
    @cjen.http.base_url(uri="http://127.0.0.1:5000")
    def __init__(self): super().__init__()

    @cjen.headers.contentType(value="application/json")
    @cjen.http.post_mapping(uri="post_method_json")
    def post_method_json(self, *, data, resp=None, **kwargs):
        with allure.step("tttt"):
            print(resp)
            assert resp.get("procCode") == 200

    @cjen.http.post_mapping(uri="post_method_variable/{id}")
    def post_method_variable(self, *, path_variable: dict, resp=None, **kwargs):
        assert resp.get("procCode") == 200
        assert resp.get("path_variable") == path_variable.get("id")

    @cjen.http.post_mapping(uri="post_method_path_variable?id={id}")
    def post_method_path_variable(self, *, path_variable: dict, resp=None, **kwargs):
        assert resp.get("procCode") == 200
        assert resp.get("path_variable") == path_variable.get("id")

    @cjen.http.post_mapping(uri="download_file")
    def download_file(self, *, resp=None, **kwargs):
        path = os.path.join(os.path.dirname(__file__), "test_download_file")
        with open(path, "wb") as f:
            f.write(resp)
        with open(path, "r") as f:
            assert f.read() == "TestDownLoadFile"
        os.remove(path)

    @cjen.http.get_mapping(uri="get_method_path_variable?id={id}")
    def get_method_path_variable(self, *, path_variable: dict, resp=None, **kwargs):
        assert resp.get("procCode") == 200
        assert resp.get("path_variable") == path_variable.get("id")

    @cjen.http.get_mapping(uri="get_method_variable/{id}")
    def get_method_variable(self, *, path_variable: dict, resp=None, **kwargs):
        assert resp.get("procCode") == 200
        assert resp.get("path_variable") == path_variable.get("id")

    @cjen.headers.contentType(value="application/json")
    @cjen.http.put_mapping(uri="put_method_json")
    def put_method_json(self, *, data, resp=None, **kwargs): ...

    @cjen.http.put_mapping(uri="put_method_variable/{id}")
    def put_method_variable(self, *, path_variable, resp=None, **kwargs): ...

    @cjen.http.put_mapping(uri="put_method_path_variable?id={id}")
    def put_method_path_variable(self, *, path_variable, resp=None, **kwargs): ...

    @cjen.headers.contentType(value="application/json")
    @cjen.http.delete_mapping(uri="delete_method_json")
    def delete_method_json(self, *, data, resp=None, **kwargs): ...

    @cjen.http.delete_mapping(uri="delete_method_variable/{id}")
    def delete_method_variable(self, *, path_variable: dict, resp=None, **kwargs): ...

    @cjen.http.delete_mapping(uri="delete_method_path_variable?id={id}")
    def delete_method_path_variable(self, *, path_variable: dict, resp=None, **kwargs): ...

    @cjen.http.upload_mapping(uri="upload_file")
    def upload_file(self, *, data, resp=None, **kwargs):
        assert resp.get("procCode") == 200
        path = os.path.join(os.path.dirname(__file__), "upload_target.txt")
        with open(path, "r") as f:
            assert f.read() == "TestUploadFile"
        os.remove(path)

    @cjen.http.upload_mapping(uri="upload_file/{id}")
    def upload_file1(self, path_variable, data, resp=None, **kwargs):
        assert resp.get("procCode") == 200
        path = os.path.join(os.path.dirname(__file__), "upload_target.txt")
        with open(path, "r") as f:
            assert f.read() == "TestUploadFile"
        os.remove(path)


@allure.feature("测试POST请求")
def test_post():
    mock = MockService()
    with allure.step("测试Post请求: 参数为Json"):
        mock.post_method_json(data=dict(username="xx", pwd="yyy"))
    with allure.step("测试Post请求: 参数在URL"):
        mock.post_method_variable(path_variable=dict(id=1))
    with allure.step("测试Post请求: 参数在URL1"):
        mock.post_method_path_variable(path_variable=dict(id=1))


def test_download():
    mock = MockService()
    mock.download_file()


def test_get():
    mock = MockService()
    mock.get_method_variable(path_variable=dict(id=2))
    mock.get_method_path_variable(path_variable=dict(id=2))


def test_upload():
    mock = MockService()
    mock.upload_file(data=dict(file=os.path.join(os.path.dirname(__file__), "upload_source.txt")))

def test_upload1():
    mock = MockService()
    mock.upload_file1(path_variable = dict(id = 1),data=dict(file=os.path.join(os.path.dirname(__file__), "upload_source.txt")))


def test_put():
    mock = MockService()
    mock.put_method_json(data=dict(username="xx", pwd="yyy"))
    mock.put_method_variable(path_variable=dict(id=1))
    mock.put_method_path_variable(path_variable=dict(id=1))


def test_delete():
    mock = MockService()
    mock.delete_method_json(data=dict(username="xx", pwd="yyy"))
    mock.delete_method_variable(path_variable=dict(id=1))
    mock.delete_method_path_variable(path_variable=dict(id=1))


