import json
import os.path

from flask import Flask
from flask import request, Response, send_file

mock_app = Flask(__name__)
__mock_data = {"companies": [dict(id=1, name="C01"), dict(id=2, name="C02")],
               "employees": [dict(id=1, name="E01", company_id=1),
                             dict(id=2, name="E02", company_id=1),
                             dict(id=3, name="E03", company_id=1),
                             dict(id=4, name="E04", company_id=2),
                             dict(id=5, name="E05", company_id=2),
                             ]}


def token_in_body(token: str):
    rsp = base_json_response()
    rsp.data = json.dumps({"procCode": 200,
                           "payload": {"jwtAuthenticationResponse": {"token": token},
                                       "message": "", "exception": None}})
    return rsp


def token_in_header(token: str):
    rsp = base_json_response()
    rsp.headers["token"] = token
    return rsp


def base_json_response():
    rsp = Response()
    rsp.status_code = 200
    rsp.headers = {"Content-Type": "application/json"}
    return rsp


@mock_app.route("/init_in_header", methods=["GET"])
def init_in_header(): return token_in_header("Jwt Init Token In Header")


@mock_app.route("/init_in_body", methods=["GET"])
def init_in_body(): return token_in_body("Jwt Init Token In Body")


@mock_app.route("/exchange_in_body", methods=["GET"])
def exchange_in_body(): return token_in_body("Jwt Exchange Token In Body")


@mock_app.route("/exchange_in_header", methods=["GET"])
def exchange_in_header(): return token_in_header("Jwt Exchange Token In Header")


@mock_app.route("/refresh_in_header", methods=["GET"])
def refresh_in_header(): return token_in_header("Jwt Refresh Token In Header")


@mock_app.route("/refresh_in_body", methods=["GET"])
def refresh_in_body(): return token_in_body("Jwt Refresh Token In Body")


@mock_app.route("/post_method_json", methods=["POST"])
def post_method_json():
    if request.json["username"] and request.json["pwd"]:
        rsp = base_json_response()
        rsp.data = json.dumps({"procCode": 200})
        return rsp


@mock_app.route("/post_method_variable/<int:id>", methods=["POST"])
def post_method_variable(id):
    rsp = base_json_response()
    rsp.data = json.dumps({"procCode": 200, "path_variable": id})
    return rsp


@mock_app.route("/post_method_path_variable", methods=["POST"])
def post_method_path_variable():
    rsp = base_json_response()
    rsp.data = json.dumps({"procCode": 200, "path_variable": int(request.args.get("id"))})
    return rsp


@mock_app.route("/put_method_json", methods=["PUT"])
def put_method_json():
    if request.json["username"] and request.json["pwd"]:
        rsp = base_json_response()
        rsp.data = json.dumps({"procCode": 200})
        return rsp


@mock_app.route("/put_method_variable/<int:id>", methods=["PUT"])
def put_method_variable(id):
    rsp = base_json_response()
    rsp.data = json.dumps({"procCode": 200, "path_variable": id})
    return rsp


@mock_app.route("/put_method_path_variable", methods=["PUT"])
def put_method_path_variable():
    rsp = base_json_response()
    rsp.data = json.dumps({"procCode": 200, "path_variable": int(request.args.get("id"))})
    return rsp


@mock_app.route("/delete_method_json", methods=["DELETE"])
def delete_method_json():
    if request.json["username"] and request.json["pwd"]:
        rsp = base_json_response()
        rsp.data = json.dumps({"procCode": 200})
        return rsp


@mock_app.route("/delete_method_variable/<int:id>", methods=["DELETE"])
def delete_method_variable(id):
    rsp = base_json_response()
    rsp.data = json.dumps({"procCode": 200, "path_variable": id})
    return rsp


@mock_app.route("/delete_method_path_variable", methods=["DELETE"])
def delete_method_path_variable():
    rsp = base_json_response()
    rsp.data = json.dumps({"procCode": 200, "path_variable": int(request.args.get("id"))})
    return rsp


@mock_app.route("/get_method_variable/<int:id>", methods=["GET"])
def get_method_variable(id):
    rsp = base_json_response()
    rsp.data = json.dumps({"procCode": 200, "path_variable": id})
    return rsp


@mock_app.route("/get_method_path_variable", methods=["GET"])
def get_method_path_variable():
    rsp = base_json_response()
    rsp.data = json.dumps({"procCode": 200, "path_variable": int(request.args.get("id"))})
    return rsp


@mock_app.route("/download_file", methods=["POST"])
def download_file():
    return send_file('download_file.txt')


@mock_app.route("/upload_file", methods=["POST"])
def upload_file():
    file = request.files['file']
    file.save(os.path.join(os.path.dirname(__file__), "aiai", "upload_target.txt"))
    rsp = base_json_response()
    rsp.data = json.dumps({"procCode": 200})
    return rsp

@mock_app.route("/upload_file/1", methods=["POST"])
def upload_file1():
    file = request.files['file']
    file.save(os.path.join(os.path.dirname(__file__), "aiai", "upload_target.txt"))
    rsp = base_json_response()
    rsp.data = json.dumps({"procCode": 200})
    return rsp


@mock_app.route("/test_headers", methods=["GET"])
def headers_tester():
    rsp = base_json_response()
    rsp.data = json.dumps({"procCode": 200, "headers": dict(request.headers)})
    return rsp


@mock_app.route("/company/<int:company_id>", methods=["GET", "POST", "PUT", "DELETE"])
def company(company_id):
    rsp = base_json_response()
    ret = list(filter(lambda c: c.get("id") == company_id, __mock_data["companies"]))[0]
    rsp.data = json.dumps({**{"procCode": 200}, **ret})
    return rsp


@mock_app.route("/companies", methods=["GET"])
def all_companies():
    rsp = base_json_response()
    rsp.data = json.dumps({"procCode": 200, "companies": __mock_data["companies"]})
    return rsp


@mock_app.route("/all_employees", methods=["GET"])
def all_employees():
    rsp = base_json_response()
    rsp.data = json.dumps({"procCode": 200, "employees": __mock_data["employees"]})
    return rsp


@mock_app.route("/none_field_response", methods=["GET"])
def none_field_response():
    rsp = base_json_response()
    rsp.data = json.dumps({"procCode": 200, "employees": None})
    return rsp


if __name__ == '__main__':
    mock_app.run()
