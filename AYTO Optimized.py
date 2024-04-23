import random
from itertools import combinations
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import statistics

class AYTO_Game:
    """game set up for the algorithms to use"""
    def __init__(self):
        """initializes variables and the contestants to pair"""
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

def create_new_pairs(previous_pairs, available_contestants):
    available_contestants = (list(available_contestants))
    random.shuffle(available_contestants)
    
    created_pairs=[]

    while available_contestants:
        
        valid_pair = False
        index = 1
        while not valid_pair:
            #print(available_contestants)
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
        
        #print(created_pairs)

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

def play_game():
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
    print(rounds)
    return rounds

#random.seed(42)
# game = AYTO_Game()
# rounds = play_game()
# print(rounds)

round_sample = [] # rounds taken for each game will be appended here to be plotted later.
for new_game in range(10000):
    game = AYTO_Game()
    rounds_taken = play_game()
    round_sample.append(rounds_taken)
# Creates a histrogram of rounds taken.
print(f"median: {statistics.median(round_sample)}\nmean: {statistics.mean(round_sample)}")
median_value = statistics.median(round_sample)
mean_value = statistics.mean(round_sample)
sns.histplot(round_sample).set(title='optimized', xlabel='Rounds')
plt.figtext(0.5, 0.7, f'Median: {median_value}\nMean: {mean_value}', ha="left", fontsize=12, bbox={"facecolor":"white", "alpha":0.5, "pad":5})
# Saves histogram to working directory.
plt.savefig('fshifas')
plt.close()
