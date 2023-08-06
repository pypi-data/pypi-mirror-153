import pytest

if __name__ == '__main__':
    pytest.main(["aiai/test_http.py::test_download", "aiai/test_http.py::test_put", "-n=2"])
