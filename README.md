# Are You The One Algorithms

## Project Overview

This project simulates, on a basic level, the game show "Are You the One" where 16 contestants try to find their perfect matches. The show's format involves contestants pairing up each week based on who they believe their perfect match is, with feedback provided on the number of correct couples but not which specific pairs are correct. One couple is also tested in the "Truth Booth" to determine definitively if they are a perfect match. The game's ultimate goal is to find all perfect matches among the contestants.

This project is an attempt to simulate the game's above conditions as well as create three algorithms for determining the perfect pairs in the least amount of rounds.

## Algorithm #1 - Random Brute Force

This algorithm works on the principal of randomness. It finds all perfect matches by randomly pairing contestants and randomly selecting them to be tested in the truth booth. There is no strategy outside of random selection. The amount of correct pairs is not used.

## Algorithm #2 - Greedy

This algorithm uses minimal strategy to find pairs. It progressively eliminates possible pairs through trial and error and focuses on those that could be correct.

### Mechanics

- Creates a list of all possible pairs that serves as the basis for the majority of the strategy.
- Uses a scoring system to ranks pairs based on whether they have been found to be correct previously or not.
- Selects the highest-scoring pairs that have not been used in the current round and submits it to the truth booth
- If true, eliminates all possible pairs that contain a number used in the correct pair

### Helper Functions

#### pair_score
Scores pairs based on their likelihood of being correct. Gives a higher score to pairs not previously found to be perfect matches.

#### impossible_pairs
Determines which pairs are impossible given a confirmed perfect match. Helps refine the set of potential pairs further.

## Algorithm #3 - Probability

This algorithm tries to find all perfect matches in the game by using a probability-based system to evaluate and optimize pairing decisions.

### Mechanics
- Creates pairs either randomly or based on previous rounds information.
- Tracks the probability for each pair of correctness based on times in a list with at least one correct pair.
- Chooses pairs based on uncertainty, choosing pairs with the highest amount of uncertainty for better information gathering (uncertainty defined as pairs whose probability of being a correct match is closest to 50%)

### Helper Functions

#### create_new_pairs
Generates new pairs that have not been overused in previous rounds. Reduces the chance of repeating ineffective combinations.

#### adjust_pairs
Adjusts the tracking probabilities for each pair based on their performance in each round, and position in lists of pairs with multiple correct pairs. Refines/creates their likelihood scores for being a match.

#### select_truth_booth_pair
Uses the updated pair probabilities to choose the most informative pair for the truth booth test. Focuses on maximizing information gain.


