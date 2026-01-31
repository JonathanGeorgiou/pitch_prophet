from datetime import datetime
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Prediction, Result, Player, Fixture, PredictionScore
from app.db.db import SessionLocal
from app.db.enums import Outcome, Points


def get_outcome(home_goals: int, away_goals: int) -> Outcome:
    if home_goals > away_goals:
        return Outcome.HOME_WIN
    if away_goals > home_goals:
        return Outcome.AWAY_WIN
    return Outcome.DRAW

def is_prediction_missed(prediction: Prediction | None) -> bool:
    if prediction is None:
        return True
    return prediction.predicted_home_goals is None or prediction.predicted_away_goals is None

def calculate_points(result: Result, prediction: Prediction | None) -> int:
    # Safety Check: If there's no prediction, it's 0 points (Incorrect)
    if prediction is None or is_prediction_missed(prediction):
        return Points.MISSED_AND_ACCOUNTED_FOR

    ## Check for exact prediction: 3 points
    if (result.home_goals == prediction.predicted_home_goals and
        result.away_goals == prediction.predicted_away_goals):
        return Points.CORRECT_SCORE

    ## Check for correct result: 1 point
    assert prediction.predicted_home_goals is not None
    assert prediction.predicted_away_goals is not None
    predicted_outcome = get_outcome(prediction.predicted_home_goals, prediction.predicted_away_goals)
    actual_outcome = get_outcome(result.home_goals, result.away_goals)

    if actual_outcome == predicted_outcome:
        return Points.CORRECT_RESULT
    else:
        return Points.INCORRECT_PREDICTION

def _get_fixtures_by_time_and_players(session: Session) -> tuple[dict[datetime, list[Fixture]], Sequence[Player]]:
    players: Sequence[Player] = session.scalars(select(Player)).all()
    # Only get finished fixtures that have a result recorded
    fixtures = session.scalars(
        select(Fixture).join(Fixture.result).where(Fixture.status == "finished")
    ).all()
    fixtures_by_time: dict[datetime, list[Fixture]]  = {}
    for fixture in fixtures:
        fixtures_by_time.setdefault(fixture.kickoff_time, []).append(fixture)
    return fixtures_by_time, players

def _score_player_for_fixture_group(session: Session, player: Player, group: list[Fixture]):
    penalty_applied = False

    for fixture in group:
        # Get the prediction for the player for each fixture in the group
        pred = fixture.get_prediction_for_player(player)

        # Calculate the points per fixture, this should return 3, 1 or 0
        points = calculate_points(fixture.result, pred)

        # Apply the penalty to the first missed prediction in the block
        if pred is None and not penalty_applied:
            points = Points.MISSED_PREDICTION_BLOCK
            penalty_applied = True

        # C. Save the Match Score
        score_entry = PredictionScore(
            player_id=player.id,
            fixture_id=fixture.id,
            prediction_id=pred.id if pred else None,
            points_awarded=points
        )
        session.add(score_entry)

def score_fixtures(session: Session) -> None:
    print("Scoring Predictions...")

    fixtures_by_time, players = _get_fixtures_by_time_and_players(session)
    print(fixtures_by_time.values())

    for player in players:
        for group in fixtures_by_time.values():
            print(f"Scoring {player.name}'s Predictions for Fixtures {group}")
            _score_player_for_fixture_group(session, player, group)

    session.commit()


if __name__ == '__main__':
    score_fixtures(SessionLocal())


