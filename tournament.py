from enum import Enum


class Result(Enum):
    WIN = 1
    LOSS = 0
    DRAW = 0.5
    SKIP = None


class Player:
    def __init__(self, pin, name, rating):
        self.pin = pin
        self.name = name
        self.rating = rating
