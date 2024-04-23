from game_mechanics import AYTO_Game, pair_contestants
import random

def random_brute_force_alg(game):
    rounds = 0
    while not game.is_game_over():
        available_contestants = list(game.available_contestants)
        pairs = pair_contestants(available_contestants)
        if pairs is not None:
            game.new_round(pairs) # calls new round to get number of correct pairs (isn't necessary)
            pair_to_submit = random.choice(pairs) # randomly chooses a pair to submit to the truth booth
            if pair_to_submit[0] != pair_to_submit[1]: # checks if the pair is the same number twice
                game.truth_booth(pair_to_submit) # rechooses the pair to submit
        rounds += 1
    return rounds

if __name__ == "__main__":
    game = AYTO_Game()
    rounds_taken = random_brute_force_alg(game)
    print(rounds_taken)
