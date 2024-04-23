# WORK IN PROGRESS
# uses code from the og file, but I wanted to separate it from the code that's good to go
# works, but it's not optimized at all

import random
from itertools import combinations, permutations
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

class AYTO_Game:
    def __init__(self):
        self.contestants = list(range(16))
        random.shuffle(self.contestants)
        self.perfect_pairs = [(self.contestants[i], self.contestants[i+1]) for i in range(0, 16, 2)]
        self.found_pairs = []
        self.guesses = []
        self.available_contestants = set(range(16))

    def new_round(self, guessed_pairs):
        self.guesses.append(guessed_pairs)
        correct_count = sum(1 for pair in guessed_pairs if pair in self.perfect_pairs)
        return correct_count
    
    def truth_booth(self, pair):
        result = pair in self.perfect_pairs
        if result:
            self.found_pairs.append(pair)
            self.perfect_pairs.remove(pair)
            self.available_contestants.difference_update(pair)
        return result
    
    def is_game_over(self):
        return len(self.found_pairs) == 8

def pair_contestants(available_contestants):
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
            new_pair = (available_contestants[0], available_contestants[index])
            # Add the new pair to new_pairs if it hasn't been tried before. Else try another pair.
            if new_pair not in previous_pairs:
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


def adjust_pairs(current_pairs):
    """ Adjust pairs by swapping one member of an incorrect pair with another. """
    # Find new configurations that have not been tried before
    if len(current_pairs) < 2:
        return current_pairs  # Not enough pairs to swap

    new_pairs = current_pairs.copy()
    # Swap the first element of the first pair with the first element of the second pair
    new_pairs[0] = (current_pairs[0][0], current_pairs[1][0])
    new_pairs[1] = (current_pairs[0][1], current_pairs[1][1])

    return new_pairs
    
def strategic_pairing(game):
    """ Plays the AYTO game using strategic guessing and feedback utilization. """
    round_count = 0
    available_contestants = list(game.available_contestants)
    previous_pairs = set()

    while not game.is_game_over():
        # Avoid repeating pairs
        current_pairs = create_new_pairs(previous_pairs, available_contestants) # creates new set of pairs
        correct_count = game.new_round(current_pairs) # submits pairs to test for correctness
        round_count += 1 # increases rounds

        if correct_count == 0:
            game.truth_booth(current_pairs[0]) # just submits the first one, unnecessary since we know there are no correct pairs
            for n in range(len(current_pairs)):
                previous_pairs.add(current_pairs[n]) # adds whole list to previous pairs so we don't use them again
        else: # if there is at least one correct pair in the list
            while correct_count >= 1:    
                truth_result = game.truth_booth(current_pairs[0]) # submits the pair to 
                previous_pairs.add(current_pairs[0]) # adds pair to previous list
                current_pairs.pop(0) # removes the already tested pair

                if truth_result == True and correct_count > 1: # if it was right and there are more than 1
                    correct_count = game.new_round(current_pairs)
                    round_count += 1
                    continue
                elif truth_result == True and correct_count == 1: # if it was right, but that's the last correct pair
                    for n in range(len(current_pairs)):
                        previous_pairs.add(current_pairs[n]) # adds rest of list to previous pairs so we don't use them again
                    break
                elif truth_result == False and correct_count >= 1: # wrong, but there's still more right ones
                    new_pairs = adjust_pairs(current_pairs)
                    correct_count = game.new_round(new_pairs)
                    round_count += 1
                    continue
                else:
                    return "something went wrong"
    return round_count


# Example usage
#random.seed(42)
game = AYTO_Game()
rounds = strategic_pairing(game)
print(rounds)
