import sqlite3

def addGame(game: str, conn: sqlite3.Connection):
    conn.execute("INSERT OR IGNORE INTO games VALUES (?)", (game,))

def addSeason(game: str, num: int, conn: sqlite3.Connection):
    addGame(game, conn)
    try:
        conn.execute("INSERT INTO seasons (season_num, game_name) VALUES (?, ?)",
                       (num, game))
    except sqlite3.IntegrityError:
        print(f"{game} Season {num} already exists!")

def addPlayer(player: str, conn: sqlite3.Connection):
    conn.execute("INSERT OR IGNORE INTO players VALUES (?)", (player,))