from game_mechanics import AYTO_Game, pair_contestants
from itertools import combinations

def greedy_alg(game):
    rounds = 0
    potential_pairs = set(combinations(game.available_contestants, 2)) # creates a set of all potential pairs

    while not game.is_game_over():
        if rounds != 0 and correct_count == 0:
            for pair in pairs:
                potential_pairs.difference_update(pair) # since all the pairs in the list are incorrect, removes all of them from the list of potential pairs

        if rounds == 0 or correct_count == 0: # on the first round or if all the pairs in a previous list were wrong
            pairs = pair_contestants(list(game.available_contestants)) # creates a new list of pairs randomly
        else: # if it's not the first round
            pairs = []
            used_contestants = set() # set to keep track of what pairs have been used
            for pair in sorted(potential_pairs, key=lambda x: -pair_score(x, game.found_pairs)): # iterates over potential pairs, sorting them based on their pair score
                if pair[0] not in used_contestants and pair[1] not in used_contestants: # checks if neither contestant in the pair has been used yet in this round
                    pairs.append(pair)
                    used_contestants.update(pair)
                    if len(used_contestants) >= len(game.available_contestants): # checks if all available contestants have been used
                        break

        correct_count = game.new_round(pairs) # starts new round
        rounds += 1

        if not pairs: # checks if no pairs were formed
            remaining_contestants = list(game.available_contestants - used_contestants)
            if len(remaining_contestants) == 2:
                tb_pair = tuple(remaining_contestants)
                tb_result = game.truth_booth(tb_pair)
            continue

        if pairs: # if pairs were formed
            tb_pair = max(pairs, key=lambda x: pair_score(x, game.found_pairs)) # selects best pair based on pair score
            tb_result = game.truth_booth(tb_pair) # sends pair to truth booth

            if tb_result == True:
                potential_pairs.difference_update(impossible_pairs(tb_pair, potential_pairs)) # updates set of all potential pairs
            elif tb_result == False:
                potential_pairs.discard(tb_pair) # removes the tested pair from potential pairs since it's incorrect

    return rounds

def pair_score(pair, found_pairs):
    """"""
    pair = tuple(sorted(pair))
    if pair in found_pairs: # if pair already found to be correct, deprioritizes it
        return -1
    else:
        return 1

def impossible_pairs(found_pair, potential_pairs):
    found_pair = tuple(sorted(found_pair))
    impossible = set()
    for x in potential_pairs:
        x = tuple(sorted(x))
        if found_pair[0] in x or found_pair[1] in x:
            if x != found_pair:
                impossible.add(x)
    return impossible

if __name__ == "__main__":
    game = AYTO_Game()
    rounds_taken = greedy_alg(game)
    print(rounds_taken)
