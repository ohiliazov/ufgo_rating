import pytest
import random
from rating import validate_rating, RatingException
import string


def generate_valid_ratings(limit=3000):
    current = 100

    while current < limit:
        yield current
        current += random.random()


def generate_invalid_float_ratings():
    current = 0

    while current < 100:
        yield current
        current += random.random()


def generate_invalid_string_ratings(times=50):
    for _ in range(times):
        rnd_string = random.sample(string.printable, 10)
        random.shuffle(rnd_string)
        yield ''.join(rnd_string)


def test_valid_rating_int():
    for rating in range(100, 3001):
        validate_rating(rating)


def test_valid_rating_float():
    for rating in generate_valid_ratings():
        validate_rating(rating)


def test_invalid_rating_float():
    for rating in generate_invalid_float_ratings():
        with pytest.raises(RatingException) as exc:
            validate_rating(rating)

        assert str(exc.value) == 'Rating should be greater or equal to 100'


def test_invalid_rating_string():
    for rating in generate_invalid_string_ratings():
        with pytest.raises(RatingException) as exc:
            validate_rating(rating)

        assert str(exc.value) == 'Rating should be integer or float type'
