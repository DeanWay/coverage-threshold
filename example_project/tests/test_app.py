from src.app import is_big_number


def test_is_big_number() -> None:
    assert is_big_number(9001) == "That's a big number!"
