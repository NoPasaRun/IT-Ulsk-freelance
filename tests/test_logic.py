from typing import List

from app import create_pagination, generate_distribution, generate_histogram_y
import pytest

from models import Company
CASES_2 = [
    (
        [
            Company(offers=[1, 2, 3]), Company(offers=[2, 6, 4]), Company(offers=[1, 4, 1]),
            Company(offers=[2, 6, 4]), Company(offers=[1, 3, 4]), Company(offers=[4, 4, 3])
        ],
        "offers",
        4,
        {"total": 18, "data": {1: 4, 2: 3, 3: 3, 4: 6, "Other": 2}, "amount": 4}
    ),
    (
        [
            Company(technologies=[1, 2, 3]), Company(technologies=[2, 6, 4]), Company(technologies=[1, 4, 1]),
            Company(technologies=[2, 6, 4]), Company(technologies=[1, 3, 4]), Company(technologies=[4, 4, 3])
        ],
        "technologies",
        5,
        {"total": 18, "data": {1: 4, 2: 3, 3: 3, 4: 6, 6: 2}, "amount": 5}
    )
]


CASES_3 = [
    (
        [Company(income=42_640_000), Company(income=36_450_000)], 5,
        [f"{num} млн" for num in [36.45, 37.69, 38.93, 40.16, 42.64]]
    )
]


@pytest.mark.parametrize("queryset,attr_name,limit,expected", CASES_2)
def test_distribution(queryset: List[Company], attr_name: str, limit: int, expected: dict):
    assert generate_distribution(queryset, attr_name, limit) == expected


@pytest.mark.parametrize("queryset,limit,expected", CASES_3)
def test_histogram(queryset: List[Company], limit: int, expected: dict):
    assert generate_histogram_y(queryset, limit) == expected
