# Pitch Prophet

A Python application to manage and score weekly football match predictions for family games. 

## Project Goals (MVP)
The goal of this MVP is to replace a cumbersome Excel-based system with a robust Python backend. It provides a structured database to store players, teams, fixtures, and predictions, alongside a scoring engine that automatically calculates points based on custom game rules (including correct scores, results, and time-block penalties).

## Getting Started

### Prerequisites
- [uv](https://github.com/astral-sh/uv) (Python package manager)

### Installation
1. Clone the repository.
2. Synchronize dependencies:
   ```bash
   uv sync
   ```

### Database Setup
1. **Initialize the Database:** This creates the SQLite database and all required tables.
   ```bash
   python -m scripts.init_db
   ```
2. **Seed the Database:** Populates the database with test players, teams, and fixtures to play with.
   ```bash
   python -m scripts.seed_db
   ```

### Running Tests
We use `pytest` for unit testing the scoring logic.
```bash
uv run pytest
```

## Future Goals
- **REST API:** Build a FastAPI or Flask layer to allow programmatic access to scores and leaderboards.
- **Web UI:** Create a modern frontend (e.g., NiceGUI or flet) so players can submit their predictions via a browser or app.
- **API Integration:** Automatically fetch real Premier League fixtures and results from an external football data API.
