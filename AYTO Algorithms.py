import random
from itertools import combinations
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import statistics

class AYTO_Game:
    """game set up for the algorithms to use"""
    def __init__(self):
        """initializes variables and the constestants to pair"""
        self.contestants = list(range(0,16)) # creates the list of contestants, numbered 0 - 15
        random.shuffle(self.contestants) # shuffles the list of contestants
        self.perfect_pairs = [tuple(sorted((self.contestants[i], self.contestants[i+1]))) for i in range(0, 16, 2)] # creates pairs
        self.found_pairs = []
        self.guesses = []
        self.available_contestants = set(range(0,16))

    def new_round(self, guessed_pairs):
        """code for what happens when round is over/start of new round"""
        self.guesses.append(guessed_pairs) # adds guessed pair to the list of guesses
        correct_count = sum(1 for pair in guessed_pairs if tuple(sorted(pair)) in self.perfect_pairs) # increases count of correct pairs if the pair was correct
        #print(f"correct_count: {correct_count}\nfound pairs: {self.found_pairs}\n----")
        return correct_count # returns how many pairs were correct from the given guessed pairs
    
    def truth_booth(self, pair):
        """truth booth code, determines if a pair is correct or not"""
        pair = tuple(sorted(pair))
        result = pair in self.perfect_pairs # checks if the chosen pair is in the list of perfect pairs
        if result == True: # if it is, adds it to list of found pairs
            self.found_pairs.append(pair)
            self.perfect_pairs.remove(pair)
            self.available_contestants.difference_update(pair)
        return result # returns T/F if the pair was correct
    
    def is_game_over(self):
        """checks if the game is over"""
        return len(self.found_pairs) == 8
    
def pair_contestants(available_contestants):
    """pairs the contestants together"""
    available_contestants = list(available_contestants)
    random.shuffle(available_contestants)
    pairs = [(available_contestants[i], available_contestants[i+1]) for i in range(0, len(available_contestants) - 1, 2)]
    return pairs

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
            #print(tb_pair)
            tb_result = game.truth_booth(tb_pair) # sends pair to truth booth

            if tb_result == True:
                #print(f"found pair: {tb_pair}")
                potential_pairs.difference_update(pairs_that_cannot_be(tb_pair, potential_pairs)) # updates set of all potential pairs
            elif tb_result == False:
                potential_pairs.discard(tb_pair) # removes the tested pair from potential pairs since it's incorrect

    print(game.found_pairs)
    return rounds

def pair_score(pair, found_pairs):
    """"""
    pair = tuple(sorted(pair))
    if pair in found_pairs: # if pair already found to be correct, deprioritizes it
        #print(f"pair found: {pair}")
        return -1
    else:
        return 1

def pairs_that_cannot_be(found_pair, potential_pairs):
    found_pair = tuple(sorted(found_pair))
    impossible = set()
    for x in potential_pairs:
        x = tuple(sorted(x))
        if found_pair[0] in x or found_pair[1] in x:
            if x != found_pair:
                impossible.add(x)
    return impossible

game = AYTO_Game()
print(f"perfect pairs:{game.perfect_pairs}")

#rounds_taken = random_brute_force_alg(game)
rounds_taken = greedy_alg(game)
#rounds_taken = optimized_algorithm(game)
print(rounds_taken)

round_sample = [] # rounds taken for each game will be appended here to be plotted later.
for new_game in range(10000):
    game = AYTO_Game()
    rounds_taken = greedy_alg(game)
    print(rounds_taken)
    round_sample.append(rounds_taken)
# Creates a histrogram of rounds taken.
median_value = statistics.median(round_sample)
mean_value = statistics.mean(round_sample)
sns.histplot(round_sample).set(title='greedy', xlabel='Rounds')
plt.figtext(0.5, 0.7, f'Median: {median_value}\nMean: {mean_value}', ha="left", fontsize=12, bbox={"facecolor":"white", "alpha":0.5, "pad":5})
# Saves histogram to working directory.
plt.savefig('greedy fhsjfa line')
plt.close()


# data = np.random.randn(1000)
 
# # # Plotting a basic histogram
# # plt.hist(data, bins=30, color='skyblue', edgecolor='black')
 
# # # Adding labels and title
# # plt.xlabel('Values')
# # plt.ylabel('Frequency')
# # plt.title('Basic Histogram')
 
# # # Display the plot
# # plt.show()

# def main():
#     """ Runs all three algorithms and outputs, to the working directory,
#      a png histrogram file of rounds taken for each algorithm."""
    
#     round_sample = [] # rounds taken for each game will be appended here to be plotted later.
#     for new_game in range(10000):
#         game = AYTO_Game()
#         rounds_taken = random_brute_force_alg(game)
#         round_sample.append(rounds_taken)
#     # Creates a histrogram of rounds taken.
#     sns.histplot(round_sample).set(title='Random Brute Force Algorithm', xlabel='Rounds')
#     # Saves histogram to working directory.
#     plt.savefig('brute_force_histogram')
#     plt.close()

#     round_sample = [] # rounds taken for each game will be appended here to be plotted later.
#     for new_game in range(10000):
#         game = AYTO_Game()
#         rounds_taken = greedy_alg(game)
#         round_sample.append(rounds_taken)
#     # Creates a histrogram of rounds taken.
#     sns.histplot(round_sample).set(title='Greedy Algorithm', xlabel='Rounds')
#     # Saves histogram to working directory.
#     plt.savefig('greedy_histogram')
#     plt.close()

#     """
#     round_sample = [] # rounds taken for each game will be appended here to be plotted later.
#     for new_game in range(10000):
#         game = AYTO_Game()
#         rounds_taken = optimized_alg(game)
#         round_sample.append(rounds_taken)
#     # Creates a histrogram of rounds taken.
#     sns.histplot(round_sample).set(title='Optimized Algorithm', xlabel='Rounds')
#     # Saves histogram to working directory.
#     plt.savefig('optimized_histogram')
#     plt.close()
#     """

# if __name__ == '__main__':
#     main()
