import random

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
