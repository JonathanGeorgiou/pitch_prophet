from unittest.mock import MagicMock

import pytest

from app.db.enums import Outcome, Points
from app.db.models import Prediction, Result, Player, Fixture
from app.services.scoring import get_outcome, calculate_points, is_prediction_missed, _score_player_for_fixture_group


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
    (Result(home_goals=1, away_goals=1), Prediction(predicted_home_goals=None, predicted_away_goals=None), Points.MISSED_AND_ACCOUNTED_FOR),
])
def test_calculate_points(result: Result, prediction: Prediction, expected_points: Points):
    actual = calculate_points(result, prediction)
    assert actual == expected_points


def test_missed_fixture_penalty():
    mock_session = MagicMock()
    mock_player = Player(id=1, name="Jonathan")

    f1 = MagicMock(spec=Fixture)
    f1.id = 101
    f1.result = Result(home_goals=1, away_goals=1)
    f1.get_prediction_for_player.return_value = None  # A Miss!

    f2 = MagicMock(spec=Fixture)
    f2.id = 102
    f2.result = Result(home_goals=1, away_goals=1)
    f2.get_prediction_for_player.return_value = None  # Another Miss!

    fixture_group = [f1, f2]

    # 2. ACT
    _score_player_for_fixture_group(mock_session, mock_player, fixture_group)

    calls = mock_session.add.call_args_list

    score_1 = calls[0].args[0]
    score_2 = calls[1].args[0]

    assert score_1.points_awarded == Points.MISSED_PREDICTION_BLOCK  # -1
    assert score_2.points_awarded == Points.MISSED_AND_ACCOUNTED_FOR  # 0



