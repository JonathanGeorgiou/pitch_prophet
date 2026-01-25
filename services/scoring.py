from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

import db.db
import db.models as models
from db.db import SessionLocal
from db.enums import Outcome, Points


def get_outcome(home_goals: int, away_goals: int) -> Outcome:
    if home_goals > away_goals:
        return Outcome.HOME_WIN
    if away_goals > home_goals:
        return Outcome.AWAY_WIN
    return Outcome.DRAW

def is_prediction_missed(prediction: models.Prediction) -> bool:
    return prediction.predicted_home_goals is None or prediction.predicted_away_goals is None

def calculate_points(result: models.Result, prediction: models.Prediction) -> Points:
    # Check if prediction was missed: -1 point
    if is_prediction_missed(prediction):
        ## check fixture time
        ##
        return Points.MISSED_PREDICTION

    ## Check for exact prediction: 3 points
    if (result.home_goals == prediction.predicted_home_goals and
        result.away_goals == prediction.predicted_away_goals):
        return Points.CORRECT_SCORE

    ## Check for correct result: 1 point
    predicted_outcome = get_outcome(prediction.predicted_home_goals, prediction.predicted_away_goals)
    actual_outcome = get_outcome(result.home_goals, result.away_goals)

    if actual_outcome == predicted_outcome:
        return Points.CORRECT_RESULT
    else:
        return Points.INCORRECT_PREDICTION


def score_fixtures(session: Session) -> None:
    players = session.query(models.Player).all()

    predictions = session.scalars(
        select(models.Prediction)
        .join(models.Fixture)
        .where(models.Fixture.kickoff_time < datetime.now()
        )).all()
    for prediction in predictions:
        print(prediction.predicted_away_goals)


