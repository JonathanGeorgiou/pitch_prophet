from datetime import datetime, timezone
from app.db.db import SessionLocal
from app.db.models import Player, Team, Fixture, Result, Prediction


def seed():
    with SessionLocal() as session:
        # 1. Create 4 Players
        player_names = ["Jonathan", "George", "Papi", "Nicolas"]
        players = [Player(name=name) for name in player_names]
        session.add_all(players)
        session.flush()  # This gets us the IDs from the DB without committing yet

        # 2. Create 20 Teams (enough for 10 fixtures)
        team_names = ["Liverpool", "Bournemouth", "Arsenal", "Chelsea", "Man Utd", "Spurs",
                      "Aston Villa", "Newcastle", "Brighton", "Fulham", "Man City", "Wolves",
                      "West Ham", "Everton", "Burnley", "Leeds", "Brentford", "Crystal Palace",
                      "Forest", "Sunderland"]
        teams = [Team(name=name) for name in team_names]
        session.add_all(teams)
        session.flush()

        # 3. Create 10 Fixtures across 3 kickoff blocks
        # We'll use 12:30, 15:00, and 17:30
        times = [
            datetime(2026, 1, 1, 12, 30, tzinfo=timezone.utc),
            datetime(2026, 1, 1, 15, 00, tzinfo=timezone.utc),
            datetime(2026, 1, 1, 17, 30, tzinfo=timezone.utc),
        ]

        fixtures = []
        for i in range(10):
            f = Fixture(
                home_team_id=teams[i * 2].id,
                away_team_id=teams[i * 2 + 1].id,
                kickoff_time=times[i % 3],  # Rotates through the 3 time slots
                status="finished"
            )
            fixtures.append(f)
        session.add_all(fixtures)
        session.flush()

        # 4. Create Results for all 10 fixtures
        for f in fixtures:
            res = Result(fixture_id=f.id, home_goals=2, away_goals=1)  # Let's make every game 2-1 for simplicity
            session.add(res)

        # 5. Create some "Scenarios" for Predictions
        # Jonathan (Player 0) -> Predicts everything exactly (2-1)
        # Alice (Player 1) -> Predicts everything as a 1-1 Draw (Correct result for some? No)
        # Bob (Player 2) -> Misses everything at the 15:00 slot
        # Charlie (Player 3) -> Misses everything completely

        for f in fixtures:
            # Jonathan predicts all
            session.add(
                Prediction(player_id=players[0].id, fixture_id=f.id, predicted_home_goals=2, predicted_away_goals=1,
                           submitted_time=datetime.now(timezone.utc)))

            # Alice predicts all
            session.add(
                Prediction(player_id=players[1].id, fixture_id=f.id, predicted_home_goals=1, predicted_away_goals=1,
                           submitted_time=datetime.now(timezone.utc)))

            # Bob only predicts games NOT at the second time slot (15:00)
            if f.kickoff_time != times[1]:
                session.add(
                    Prediction(player_id=players[2].id, fixture_id=f.id, predicted_home_goals=2, predicted_away_goals=1,
                               submitted_time=datetime.now(timezone.utc)))

        session.commit()
        print("Successfully seeded 4 players, 20 teams, 10 fixtures, and predictions!")


if __name__ == "__main__":
    seed()
