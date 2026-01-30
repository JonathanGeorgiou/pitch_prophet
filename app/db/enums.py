from enum import StrEnum, IntEnum

class Outcome(StrEnum):
    HOME_WIN = "HOME_WIN"
    AWAY_WIN = "AWAY_WIN"
    DRAW = "DRAW"

class Points(IntEnum):
    # Returned for predicting the score exactly correct
    CORRECT_SCORE = 3
    # Returned for predicting the correct result
    CORRECT_RESULT = 1
    # Returned for getting the prediction wrong
    INCORRECT_PREDICTION = 0
    # Returned for missing the fixture block
    MISSED_PREDICTION_BLOCK = -1
    # Returned missed predictions that have already been accounted for
    MISSED_AND_ACCOUNTED_FOR = 0