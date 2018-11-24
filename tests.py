import pytest
from bot import Bot


def test_mutate_number():
    i = 0
    for _ in range(1000):
        i = Bot._invert_bit(i)
        assert i < 64, "Value i is %d should be less than 64" % i