from app import create_pagination
import pytest


CASES = [
    (2, 4, (1, 2, 3, 4)),
    (5, 9, (1, "...", 4, 5, 6, "...", 9)),
    (4, 17, (1, 2, 3, 4, 5, "...", 17)),
    (18, 20, (1, "...", 17, 18, 19, 20))
]


@pytest.mark.parametrize("current_page,total_pages,expected", CASES)
def test_pagination(current_page: int, total_pages: int, expected: tuple):
    texts = tuple(
        data.get("text") for data in create_pagination(
            "", current_page, total_pages, ""
        )
    )
    assert texts == expected


@pytest.mark.parametrize("current_page,total_pages,expected", CASES)
def test_pagination(current_page: int, total_pages: int, expected: tuple):
    texts = tuple(
        data.get("text") for data in create_pagination(
            "", current_page, total_pages, ""
        )
    )
    assert texts == expected
