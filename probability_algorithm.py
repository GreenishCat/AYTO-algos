from game_mechanics import AYTO_Game, pair_contestants
import random

def create_new_pairs(previous_pairs, available_contestants):
    available_contestants = (list(available_contestants))
    random.shuffle(available_contestants)
    
    created_pairs=[]

    while available_contestants:
        
        valid_pair = False
        index = 1
        while not valid_pair:
            new_pair = (available_contestants[0], available_contestants[index])
            # Add the new pair to new_pairs if it hasn't been tried before. Else try another pair.
            if tuple(sorted(new_pair)) not in [tuple(sorted(pair)) for pair in previous_pairs]:
                created_pairs.append(new_pair)
                valid_pair = True
            elif index == (len(available_contestants) - 1):
                created_pairs.append(new_pair)
                valid_pair = True
            else: 
                index += 1
            

        for contestant in new_pair:
            available_contestants.remove(contestant)
        
    return created_pairs

def adjust_pairs(guessed_pairs, correct_count, pair_probabilities):
    for pair in guessed_pairs:
        sorted_pair = tuple(sorted(pair))
        if sorted_pair not in pair_probabilities:
            pair_probabilities[sorted_pair] = [0, 0]
        pair_probabilities[sorted_pair][1] += 1
        if correct_count > 0:
            pair_probabilities[sorted_pair][0] += 1
            correct_count -= 1
    return pair_probabilities

def select_truth_booth_pair(guessed_pairs, pair_probabilities):
    max_uncertainty = -1
    selected_pair = None
    for pair in guessed_pairs:
        sorted_pair = tuple(sorted(pair))
        correct, total = pair_probabilities.get(sorted_pair, (0, 0))
        if total > 0:
            uncertainty = 1 - abs(correct / total - 0.5)
            if uncertainty > max_uncertainty:
                max_uncertainty = uncertainty
                selected_pair = pair
    return selected_pair

def prob_optimized_algo():
    game = AYTO_Game()
    rounds = 0
    pair_probabilities = {}

    while not game.is_game_over():
        rounds += 1
        if rounds == 1:
            guessed_pairs = pair_contestants(game.available_contestants)
        else:
            guessed_pairs = create_new_pairs(game.guesses[-1], game.available_contestants)
        
        correct_count = game.new_round(guessed_pairs)
        pair_probabilities = adjust_pairs(guessed_pairs, correct_count, pair_probabilities)
        
        truth_booth_pair = select_truth_booth_pair(guessed_pairs, pair_probabilities)
        game.truth_booth(truth_booth_pair)
    return rounds

if __name__ == "__main__":
    game = AYTO_Game()
    rounds_taken = prob_optimized_algo(game)
    print(rounds_taken)
