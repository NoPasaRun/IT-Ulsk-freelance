import pytest

from db import Session
from models import Rating


@pytest.fixture()
def session():
    with Session() as ses:
        yield ses
    ses.rollback()


def test_check_total(session):
    count_1 = Rating.count(session)
    session.add(Rating(id=1000_000, name="Test"))
    count_2 = Rating.count(session)

    assert count_1 + 1 == count_2


def test_get(session):
    session.add(Rating(id=1000_000, name="Test"))
    rating = Rating.get(session, 1_000_000)

    assert rating is not None

