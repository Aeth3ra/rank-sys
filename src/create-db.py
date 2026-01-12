import sqlite3, os
from dotenv import load_dotenv

load_dotenv()

sql_statements = [
    """--sql
    CREATE TABLE IF NOT EXISTS games (
        game_name   TEXT PRIMARY KEY
    );""",

    """--sql
    CREATE TABLE IF NOT EXISTS seasons (
        season_id   INTEGER PRIMARY KEY,
        season_num  INTEGER NOT NULL,
        game_name   TEXT NOT NULL,
        UNIQUE (season_num, game_name),
        FOREIGN KEY (game_name) REFERENCES games (game_name)
    );""",

    """--sql
    CREATE TABLE IF NOT EXISTS players (
        player_name TEXT PRIMARY KEY
    );""",

    """--sql
    CREATE TABLE IF NOT EXISTS ratings (
        rating_id   INTEGER PRIMARY KEY,
        player_name TEXT NOT NULL,
        season_id   INTEGER NOT NULL,
        mu          REAL NOT NULL,
        sigma       REAL NOT NULL,
        FOREIGN KEY (player_name) REFERENCES players (player_name),
        FOREIGN KEY (season_id) REFERENCES seasons (season_id),
        UNIQUE (player_name, season_id)
    );""",

    """--sql
    CREATE TABLE IF NOT EXISTS matches (
        match_id    INTEGER PRIMARY KEY,
        season_id   INTEGER NOT NULL,
        timestamp   INTEGER NOT NULL,
        FOREIGN KEY (season_id) REFERENCES seasons (season_id)
    );""",

    """--sql
    CREATE TABLE IF NOT EXISTS teams (
        team_id     INTEGER PRIMARY KEY,
        match_id    INTEGER NOT NULL,
        score       INTEGER NOT NULL,
        FOREIGN KEY (match_id) REFERENCES matches (match_id)
    );""",

    """--sql
    CREATE TABLE IF NOT EXISTS participations (
        team_id     INTEGER NOT NULL,
        rating_id   INTEGER NOT NULL,
        PRIMARY KEY (team_id, rating_id)
    );"""
]

database = "data/" + os.getenv("DB") + ".db"

with sqlite3.connect(database) as conn:
    cursor = conn.cursor()
    for statement in sql_statements:
        cursor.execute(statement)
    print("Tables created.")