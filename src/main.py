from openskill.models import PlackettLuce, PlackettLuceRating
from database import *


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
    season_id = getSeasonId(conn, "Lockout", 1)
    rating_id = getRatingId(conn, "Aethera", season_id)
    updateRating(conn, rating_id, 26, 8.1)
    # cursor.execute("DELETE FROM seasons WHERE season_id = 2")