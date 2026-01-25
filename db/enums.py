from enum import StrEnum, IntEnum

class Outcome(StrEnum):
    HOME_WIN = "HOME_WIN"
    AWAY_WIN = "AWAY_WIN"
    DRAW = "DRAW"

class Points(IntEnum):
    CORRECT_SCORE = 3
    CORRECT_RESULT = 1
    INCORRECT_PREDICTION = 0
    MISSED_PREDICTION = -1