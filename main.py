from game_mechanics import AYTO_Game
from brute_force_algorithm import random_brute_force_alg
from greedy_algorithm import greedy_alg
from probability_algorithm import prob_optimized_algo

import matplotlib.pyplot as plt
import seaborn as sns
import statistics

def main():
    print("Starting histogram for Brute Force")
    round_sample = [] # rounds taken for each game will be appended here to be plotted later.
    for new_game in range(10000):
        game = AYTO_Game()
        rounds_taken = random_brute_force_alg(game)
        round_sample.append(rounds_taken)
    # Creates a histrogram of rounds taken.
    median_value = statistics.median(round_sample)
    mean_value = statistics.mean(round_sample)
    sns.histplot(round_sample).set(title='Random Brute Force Algorithm', xlabel='Rounds')
    plt.figtext(0.5, 0.7, f'Median: {median_value}\nMean: {mean_value}', ha="left", fontsize=12, bbox={"facecolor":"white", "alpha":0.5, "pad":5})
    # Saves histogram to working directory.
    plt.savefig('brute_force_histogram')
    plt.close()
    print("Finished histogram for Brute Force\n")

    print("Starting histogram for Greedy")
    round_sample = [] # rounds taken for each game will be appended here to be plotted later.
    for new_game in range(10000):
        game = AYTO_Game()
        rounds_taken = greedy_alg(game)
        round_sample.append(rounds_taken)
    # Creates a histrogram of rounds taken.
    median_value = statistics.median(round_sample)
    mean_value = statistics.mean(round_sample)
    sns.histplot(round_sample).set(title='Greedy Algorithm', xlabel='Rounds')
    plt.figtext(0.5, 0.7, f'Median: {median_value}\nMean: {mean_value}', ha="left", fontsize=12, bbox={"facecolor":"white", "alpha":0.5, "pad":5})
    # Saves histogram to working directory.
    plt.savefig('greedy_histogram')
    plt.close()
    print("Finished histogram for Greedy\n")


    print("Starting histogram for Opimitized")
    round_sample = [] # rounds taken for each game will be appended here to be plotted later.
    for new_game in range(10000):
        game = AYTO_Game()
        rounds_taken = prob_optimized_algo()
        round_sample.append(rounds_taken)
    # Creates a histrogram of rounds taken.
    median_value = statistics.median(round_sample)
    mean_value = statistics.mean(round_sample)
    sns.histplot(round_sample).set(title='Probability-Based Algorithm', xlabel='Rounds')
    plt.figtext(0.5, 0.7, f'Median: {median_value}\nMean: {mean_value}', ha="left", fontsize=12, bbox={"facecolor":"white", "alpha":0.5, "pad":5})
    # Saves histogram to working directory.
    plt.savefig('probability_optimized_histogram')
    plt.close()
    print("Finished histogram for Optimized\n")

if __name__ == '__main__':
    main()
