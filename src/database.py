import sqlite3
from config import Config

def addGame(conn: sqlite3.Connection, game: str):
    conn.execute("INSERT OR IGNORE INTO games VALUES (?)", (game,))

def addSeason(conn: sqlite3.Connection, game: str, num: int):
    addGame(game, conn)
    try:
        conn.execute("INSERT INTO seasons (season_num, game_name) VALUES (?, ?)",
                       (num, game))
    except sqlite3.IntegrityError:
        print(f"{game} Season {num} already exists!")

def addPlayer(conn: sqlite3.Connection, player: str):
    conn.execute("INSERT OR IGNORE INTO players VALUES (?)", (player,))

def getSeasonId(conn: sqlite3.Connection, game: str, num: int) -> int:
    cursor = conn.cursor()
    sql = """--sql
        SELECT season_id FROM seasons 
        WHERE upper(game_name) = upper(?) 
        AND season_num = ?;"""
    cursor.execute(sql, (game, num))
    return cursor.fetchone()[0]

def newRating(conn: sqlite3.Connection, season_id: int, player: str, config: Config = Config()):
    pass