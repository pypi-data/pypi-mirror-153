import pytest

from cjen.bigtangerine import ContextManager, ContextArgs


@pytest.fixture(scope='function')
def context_data():
    context = ContextManager()
    data = dict(x=1, y=2)
    context.update(data)
    return context


def test_update_dict(context_data):
    data = dict(x=3, y=4)
    context_data.update(data)
    assert context_data.get("x") == 3
    assert context_data.get("y") == 4
    assert context_data["x"] == 3
    assert context_data["y"] == 4


def test_update_tuple(context_data):
    context_data.update(z=1, j=2)
    assert context_data.get("z") == 1
    assert context_data["z"] == 1
    assert context_data.get("j") == 2
    assert context_data["j"] == 2


def test_update_context(context_data):
    target = ContextManager()
    target.update(context_data)
    assert target["x"] == 1
    assert target["y"] == 2


def test_pick_up(context_data):
    pick = context_data.pick_up(context_args=ContextArgs(c="x", d="y"))
    assert pick["c"] == 1
    assert pick["d"] == 2
