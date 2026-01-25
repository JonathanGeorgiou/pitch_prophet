import pytest

from db import models
from db.enums import Outcome, Points
from db.models import Prediction, Result
from services.scoring import get_outcome, calculate_points, is_prediction_missed


@pytest.mark.parametrize("home_goals, away_goals, expected_outcome", [
    (2, 1, Outcome.HOME_WIN),
    (1, 2, Outcome.AWAY_WIN),
    (2, 2, Outcome.DRAW),
])
def test_get_outcome(home_goals: int, away_goals: int, expected_outcome: Outcome):
    actual = get_outcome(home_goals, away_goals)
    assert actual == expected_outcome

@pytest.mark.parametrize("prediction, expected_result", [
    (Prediction(predicted_home_goals=2, predicted_away_goals=1), False),
    (Prediction(predicted_home_goals=None, predicted_away_goals=None), True),
    (Prediction(predicted_home_goals=1, predicted_away_goals=None), True),
])
def test_is_prediction_missed(prediction: Prediction, expected_result: bool):
    actual = is_prediction_missed(prediction)
    assert actual == expected_result

@pytest.mark.parametrize("result, prediction, expected_points", [
    (Result(home_goals=2, away_goals=1), Prediction(predicted_home_goals=2, predicted_away_goals=1), Points.CORRECT_SCORE),
    (Result(home_goals=1, away_goals=2), Prediction(predicted_home_goals=0, predicted_away_goals=1), Points.CORRECT_RESULT),
    (Result(home_goals=3, away_goals=3), Prediction(predicted_home_goals=0, predicted_away_goals=0),Points.CORRECT_RESULT),
    (Result(home_goals=2, away_goals=2), Prediction(predicted_home_goals=2, predicted_away_goals=1), Points.INCORRECT_PREDICTION),
    (Result(home_goals=1, away_goals=1), Prediction(predicted_home_goals=None, predicted_away_goals=None), Points.MISSED_PREDICTION),
])
def test_calculate_points(result: models.Result, prediction: models.Prediction, expected_points: Points):
    actual = calculate_points(result, prediction)
    assert actual == expected_points


