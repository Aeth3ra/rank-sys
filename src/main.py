from openskill.models import PlackettLuce, PlackettLuceRating
from database import *
from dotenv import load_dotenv
import sqlite3, os
load_dotenv()

def getConnection() -> sqlite3.Connection:
    database = "data/" + os.getenv("DB") + ".db"
    conn = sqlite3.connect(database)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def getMmr(player: PlackettLuceRating):
    return player.ordinal(alpha=25, target=100)

def parseMatchInput():
    user_input = ""
    teams = []
    user_input = input(f"Enter the members of Team {len(teams)+1}: ")
    while user_input or not teams:
        teams.append([member.strip() for member in user_input.split(',')])
        user_input = input(f"Enter the members of Team {len(teams)+1}: ")
    
    user_input = input("Enter the scores for the teams: ")
    scores = [int(score.strip()) for score in user_input.split(',')]

    return teams, scores


with getConnection() as conn:
    addSeason("Minecraft", 1, conn)
    # cursor.execute("DELETE FROM seasons WHERE season_id = 2")