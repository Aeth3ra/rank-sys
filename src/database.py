import sqlite3, os
from config import Config
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

def getConnection() -> sqlite3.Connection:
    database = "data/" + os.getenv("DB") + ".db"
    conn = sqlite3.connect(database, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn

def adaptDatetimeEpoch(val):
    """Adapt datetime.datetime to Unix timestamp."""
    return int(val.timestamp())

def convertTimestamp(val):
    """Convert Unix epoch timestamp to datetime.datetime object."""
    return datetime.fromtimestamp(int(val))

sqlite3.register_adapter(datetime, adaptDatetimeEpoch)
sqlite3.register_converter("timestamp", convertTimestamp)

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

def getTeamRatingIds(conn: sqlite3.Connection, team: list[str], season_id) -> list[int]:
    placeholders = ', '.join(['?'] * len(team))
    sql = f"""--sql
        SELECT rating_id FROM ratings
        WHERE season_id = ? AND player_name in ({placeholders});"""
    cursor = conn.execute(sql, (season_id, *team))
    return [row[0] for row in cursor.fetchall()]

def updateRating(conn: sqlite3.Connection, rating_id: int, mu: float, sigma: float):
    sql = "UPDATE ratings SET mu = ?, sigma = ? WHERE rating_id = ?"
    conn.execute(sql, (mu, sigma, rating_id))

def addMatch(conn: sqlite3.Connection, season_id: int, match_time: int) -> int:
    sql = "INSERT INTO matches (season_id, match_time) VALUES (?, ?) RETURNING match_id"
    cursor = conn.execute(sql, (season_id, match_time))
    return cursor.fetchone()[0]

def addTeam(conn: sqlite3.Connection, match_id: int, score: int) -> int:
    sql = "INSERT INTO teams (match_id, score) VALUES (?, ?) RETURNING team_id"
    cursor = conn.execute(sql, (match_id, score))
    return cursor.fetchone()[0]

def addParticipation(conn: sqlite3.Connection, team_id: int, rating_id: int):
    try:
        conn.execute("INSERT INTO participations VALUES (?, ?)", (team_id, rating_id))
    except sqlite3.IntegrityError:
        print(f"Error adding participation of rating_id {rating_id} to team with id {team_id}!")

def recordMatch(conn: sqlite3.Connection, game_name: str, season_num: int, 
                teams: list[list[str]], scores: list[int], match_time: datetime):
    """
    Record a match in the database, adding rows to the matches, 
    teams and participations tables.
    
    :param conn: sqlite3 connection object to the database
    :param season_id: database id of the season the match took place in
    :param teams: list of teams, where each team is a list of `rating_id`s
    :param scores: list of scores for each team, must be same length as `teams`
    :param timestamp: unix epoch time of match
    """
    season_id = getSeasonId(conn, game_name, season_num)
    teams_rating_ids = [getTeamRatingIds(conn, team, season_id) for team in teams]

    match_id = addMatch(conn, season_id, match_time)
    team_ids = [addTeam(conn, match_id, score) for score in scores]

    for team_ratings, team_id in zip(teams_rating_ids, team_ids):
        for rating_id in team_ratings:
            addParticipation(conn, team_id, rating_id)

def updateRatings(conn: sqlite3.Connection, season_id: int,
                  new_ratings: list[tuple[str, float, float]]):
    """
    Update the ratings of a list of players.
    
    :param conn: an sqlite3 conection object to the database
    :param season_id: id of the season the ratings below to
    :param new_ratings: list of tuples, where each tuple consists 
        of (player_name, mu, sigma)
    """
    for player_name, mu, sigma in new_ratings:
        rating_id = getRatingId(conn, player_name, season_id)
        updateRating(conn, rating_id, mu, sigma)