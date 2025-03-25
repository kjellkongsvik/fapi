from fapi.hello import Hello


def test_hello():
    h = Hello()
    assert h.val == 45
