import pytest
from cjen import BigTangerine
import cjen


class HeaderMockService(BigTangerine):

    @cjen.http.base_url(uri="http://127.0.0.1:5000")
    @cjen.headers.basicHeaders(headers=dict(Basicheader="1"))
    def __init__(self): super().__init__()

    @cjen.http.get_mapping(uri="test_headers")
    def basic_headers(self, resp=None, **kwargs):
        assert resp.get("headers")["Basicheader"] == self.headers["Basicheader"]

    @cjen.headers.appendBasicHeaders(headers=dict(Appendbasicheaders="2"))
    @cjen.http.get_mapping(uri="test_headers")
    def append_basic_headers(self, resp=None, **kwargs):
        assert resp.get("headers")["Basicheader"] == self.headers["Basicheader"]
        assert resp.get("headers")["Appendbasicheaders"] == self.headers["Appendbasicheaders"]

    @cjen.headers.addHeaders(headers=dict(Newheader="3"))
    @cjen.http.get_mapping(uri="test_headers")
    def add_headers(self, resp=None, **kwargs):
        assert resp.get("headers")["Basicheader"] == self.headers["Basicheader"]
        assert resp.get("headers")["Newheader"] == "3"
        assert self.headers.get("Newheader") is None

    @cjen.headers.contentType(value="4")
    @cjen.http.get_mapping(uri="test_headers")
    def add_content_type(self, resp=None, **kwargs):
        assert resp.get("headers")["Basicheader"] == self.headers["Basicheader"]
        assert resp.get("headers")["Content-Type"] == "4"
        assert self.headers.get("Content-Type") is None

    @cjen.headers.accept(value="5")
    @cjen.http.get_mapping(uri="test_headers")
    def add_accept(self, resp=None, **kwargs):
        assert resp.get("headers")["Basicheader"] == self.headers["Basicheader"]
        assert resp.get("headers")["Accept"] == "5"
        assert self.headers.get("Accept") is None


def test_basic_headers():
    mock = HeaderMockService()
    mock.basic_headers()


def test_append_basic_headers():
    mock = HeaderMockService()
    mock.append_basic_headers()


def test_add_headers():
    mock = HeaderMockService()
    mock.add_headers()


def test_add_content_type():
    mock = HeaderMockService()
    mock.add_content_type()


def test_add_accept():
    mock = HeaderMockService()
    mock.add_accept()

