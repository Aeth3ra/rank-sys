import sqlite3
from config import Config

def addGame(conn: sqlite3.Connection, game: str):
    conn.execute("INSERT OR IGNORE INTO games VALUES (?)", (game,))

def addSeason(conn: sqlite3.Connection, game: str, num: int):
    cursor = conn.cursor()
    
    # Check that game exists in database
    # cursor.execute("SELECT * FROM games WHERE game_name = ?", (game,))
    # if cursor.fetchone() is None:
    #     raise ValueError

    try:
        cursor.execute("INSERT INTO seasons (season_num, game_name) VALUES (?, ?)",
                       (num, game))
    except sqlite3.IntegrityError:
        # print(f"{game} Season {num} already exists!")
        print(f"Error creating Season {num} for {game}!")

def getSeasonId(conn: sqlite3.Connection, game: str, num: int) -> int:
    sql = """--sql
        SELECT season_id FROM seasons 
        WHERE upper(game_name) = upper(?) 
        AND season_num = ?;"""
    cursor = conn.execute(sql, (game, num))
    return cursor.fetchone()[0]

def addPlayer(conn: sqlite3.Connection, player: str):
    conn.execute("INSERT OR IGNORE INTO players VALUES (?)", (player,))

def newRating(conn: sqlite3.Connection, season_id: int, player: str, config: Config = Config()):
    try:
        sql = "INSERT INTO ratings (player_name, season_id, mu, sigma) VALUES (?, ?, ?, ?)"
        conn.execute(sql, (player, season_id, config.mu, config.sigma))
    except sqlite3.IntegrityError:
        # print(f"{player} is already in Season with id {season_id}!")
        print(f"Error adding {player} to Season with id {season_id}!")

def getRatingId(conn: sqlite3.Connection, player: str, season_id: int) -> int:
    sql = """--sql
        SELECT rating_id FROM ratings
        WHERE upper(player_name) = upper(?)
        AND season_id = ?;"""
    cursor = conn.execute(sql, (player, season_id))
    return cursor.fetchone()[0]