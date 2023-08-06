import sys

from cjen import BigTangerine, JWTFrom, JWTAction
import cjen


class JWTMockService(BigTangerine):
    @cjen.http.base_url(uri="http://127.0.0.1:5000")
    def __init__(self):
        super().__init__()

    @cjen.http.post_mapping(uri="login")
    @cjen.jwt(json_path="$.payload.jwtAuthenticationResponse.token", key="jwt", jwt_from=JWTFrom.BODY,
              action=JWTAction.INIT)
    def login(self, data, resp=None, **kwargs): ...

    @cjen.http.get_mapping(uri="init_in_header")
    @cjen.jwt(json_path="$.token", key="jwt", jwt_from=JWTFrom.HEADER, action=JWTAction.INIT)
    def init_in_header(self, resp=None, **kwargs): ...

    @cjen.http.get_mapping(uri="init_in_body")
    @cjen.jwt(json_path="$.payload.jwtAuthenticationResponse.token", key="jwt", jwt_from=JWTFrom.BODY,
              action=JWTAction.INIT)
    def init_in_body(self, resp=None, **kwargs): ...

    @cjen.http.get_mapping(uri="exchange_in_header")
    @cjen.jwt(json_path="$.token", key="jwt", jwt_from=JWTFrom.HEADER,
              action=JWTAction.EXCHANGE)
    def exchange_in_header(self, resp=None, **kwargs): ...

    @cjen.http.get_mapping(uri="exchange_in_body")
    @cjen.jwt(json_path="$.payload.jwtAuthenticationResponse.token", key="jwt", jwt_from=JWTFrom.BODY,
              action=JWTAction.EXCHANGE)
    def exchange_in_body(self, resp=None, **kwargs): ...

    @cjen.http.get_mapping(uri="refresh_in_header")
    @cjen.jwt(json_path="$.token", key="jwt", jwt_from=JWTFrom.HEADER,
              action=JWTAction.REFRESH)
    def refresh_in_header(self, resp=None, **kwargs): ...

    @cjen.http.get_mapping(uri="refresh_in_body")
    @cjen.jwt(json_path="$.payload.jwtAuthenticationResponse.token", key="jwt", jwt_from=JWTFrom.BODY,
              action=JWTAction.REFRESH)
    def refresh_in_body(self, resp=None, **kwargs): ...


def test_init_body_exchange_body_refresh_body():
    mock = JWTMockService()
    mock.init_in_body()
    assert mock.headers["jwt"] == "Jwt Init Token In Body"
    mock.exchange_in_body()
    assert mock.headers["jwt"] == "Jwt Exchange Token In Body"
    mock.refresh_in_body()
    assert mock.headers["jwt"] == "Jwt Refresh Token In Body"


def test_init_header_exchange_header_refresh_header():
    mock = JWTMockService()
    mock.init_in_header()
    assert mock.headers["jwt"] == "Jwt Init Token In Header"
    mock.exchange_in_header()
    assert mock.headers["jwt"] == "Jwt Exchange Token In Header"
    mock.refresh_in_header()
    assert mock.headers["jwt"] == "Jwt Refresh Token In Header"

