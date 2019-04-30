"""UFGO rating calculator

This module is designed to calculate the rating by the method of V. Korsak.
The description: http://forum.ufgo.org/viewtopic.php?f=3&t=1260
"""

from collections import defaultdict
from math import exp


class RatingException(Exception):
    pass


def validate_rating(rating: (int, float)):
    if not isinstance(rating, (int, float)):
        raise RatingException('Rating should be integer or float type')

    if rating < 100:
        raise RatingException('Rating should be greater or equal to 100')


def a_factor(rating: (int, float)):
    """A-factor for given rating

    Used to calculate winning expectancy of a match-up.

    :param rating: greater or equal to 100
    :return a-factor: between 70 and 200
    """
    validate_rating(rating)

    if rating < 2700:
        return 205 - rating / 20
    else:
        return 70


def winning_expectancy(player_rating: (int, float), opponent_rating: (int, float)):
    """Winning expectancy of player vs. opponent match-up

    :param player_rating: greater or equal to 100
    :param opponent_rating: greater or equal to 100
    :return winning expectancy of player: between 0 and 1
    """

    # get rating of weaker player and calculate a-factor
    lower_rating = min(player_rating, opponent_rating)

    # get rating difference
    rating_diff = abs(player_rating - opponent_rating)

    # calculate winning expectancy of weaker player
    lower_win_exp = 1 / (exp(rating_diff / a_factor(lower_rating)) + 1)

    if player_rating <= opponent_rating:
        return lower_win_exp
    else:
        return 1 - lower_win_exp


def k_factor(rating: (int, float)):
    """K-factor for given rating

    Used to calculate rating growth of a player.

    :param rating: greater or equal to 100
    :return k-factor: between 10 and 122
    """
    validate_rating(rating)

    if rating < 200:
        k = 122 - rating * 0.06
    elif rating < 1300:
        k = 120 - rating * 0.05
    elif rating < 2000:
        k = 107 - rating * 0.04
    elif rating < 2400:
        k = 87 - rating * 0.03
    elif rating < 2600:
        k = 63 - rating * 0.02
    elif rating < 2700:
        k = 37 - rating * 0.01
    else:
        k = 10

    return k


def abnormal_rating(player_rating: (int, float), number_of_rounds: int):
    """Abnormal rating for a player, who played a given number of rounds.

    Used to determine if player has played much better than expected.

    :param player_rating: greater or equal to 100
    :param number_of_rounds: int > 0
    :return abnormal_rating: threshold that is greater than rating
    """
    abnormal_growth = number_of_rounds * k_factor(player_rating) * (0.45 + (3100 - player_rating) / 50000)

    return player_rating + abnormal_growth


def calculate_rating(player_rating: float, opponent_rating: float, result=1):
    """Calculate new rating for a player after match-up.

    :param player_rating: greater or equal to 100
    :param opponent_rating: greater or equal to 100
    :param result: None - not ranked game; 0 - loss; 0.5 - draw; 1 - win
    :return next_rating: greater or equal to 100
    """
    if result is None:
        return player_rating

    win_prob = winning_expectancy(player_rating, opponent_rating)
    growth = k_factor(player_rating) * (result - win_prob + (3100 - player_rating) / 50000)

    next_rating = max(player_rating + growth, 100)
    return next_rating


def count_rated_rounds(tournament_data: dict):
    """Count rounds with results for each player

    :param tournament_data: tournament table with match-ups
    :return rated_rounds: dictionary with number of rated rounds for each player
    """
    rated_rounds = defaultdict(int)

    for player in tournament_data:
        for pairing in tournament_data[player]:
            if not (pairing[0] is None or pairing[1] is None):
                rated_rounds[player] += 1

    return rated_rounds


def calculate_round(current_ratings: dict, round_data: dict):
    """Calculate ratings after round for each player

    :param current_ratings: ratings before round
    :param round_data: round results for each player
    :return: ratings after round
    """
    round_ratings = current_ratings.copy()

    for player in round_data:
        opponent, result = round_data[player]

        if opponent is not None:
            round_ratings[player] = calculate_rating(current_ratings[player], current_ratings[opponent], result)

    return round_ratings


def calculate_tournament(initial_ratings: dict, tournament_data: dict, recalculate_on_abnormal: bool = True):
    """Calculate rating for tournament

    :param initial_ratings: ratings for each player
    :param tournament_data: tournament table
    :param recalculate_on_abnormal: do recalculation if abnormal ratings found
    :return:
    """
    rounds = len(list(tournament_data[1]))
    rated_rounds = count_rated_rounds(tournament_data)
    finish_ratings = initial_ratings.copy()
    for current_round in range(rounds):
        round_data = {}
        for player in tournament_data:
            round_data[player] = tournament_data[player][current_round]
        finish_ratings = calculate_round(finish_ratings, round_data)

    if not recalculate_on_abnormal:
        return finish_ratings

    abnormal_counter = 0
    abnormal_data = {}

    # replace initial rating with finish rating for players with abnormal result
    for player in initial_ratings:

        if finish_ratings[player] >= abnormal_rating(initial_ratings[player], rated_rounds[player]):
            abnormal_data[player] = finish_ratings[player]
            abnormal_counter += 1
        else:
            abnormal_data[player] = initial_ratings[player]

    # recalculate if abnormal result was found
    if abnormal_counter:
        return calculate_tournament(abnormal_data, tournament_data, recalculate_on_abnormal)
    else:
        return finish_ratings
