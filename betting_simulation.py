import algorithms
from algorithms import BlackjackAlgorithm
from blackjack_core.utility import clear_screen, BettingManager
from blackjack_core.blackjack import game
from blackjack_core.blackjack_classes import Deck

"""
This module serves as a the program used to select a Blackjack algorithm and run a betting simulation.
It subalgorithms from the algorithms module and allows the user to select a combination to form the algorithm used in the simulation.
It then runs a betting simulation using constants defined below.
The data is saved to a file for later analysis.
"""



#Constants for betting simulations, defined here for ease of modification
#All constants are saved to the json file for later reference
BASE_BET = 500  
DECKS = 16 
GAMES = 900
STARTING_BALANCE = 5000 



def import_algoritms(algorithm_type):
    """Dynamically imports all subclasses of a given base class from a module."""
    # Go through everything defined in algorithms.py
    algorithms = []
    for subclass in algorithm_type.__subclasses__():
        algorithms.append(subclass())
       

    return algorithms


def select_subalgorithm(algorithms, algorithm_category):
    """Prompts the user to select a subalgorithm from a list."""
    print("Available Algorithms:")
    for i, algo in enumerate(algorithms):
        print(f"{i + 1}. {algo}")

    while True:
        clear_screen()
        try:
            print(f"Select an {algorithm_category} algorithm by number: ")

            for i, algo in enumerate(algorithms):
                print(f"{i + 1}. {algo}")

            choice = int(input(">")) - 1
            if 0 <= choice < len(algorithms):
                print(f"{algorithms[choice]}")
                print(f"{algorithms[choice].description()}")
                confirm = input("Is this the algorithm you want to use? (y to confirm): ").strip().lower()
                if confirm == 'y':
                    return algorithms[choice]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def construct_algorithm(selection_algorithms, betting_algorithms, counting_algorithms):
    """Constructs a BlackjackAlgorithm instance based on user input."""
    selection = select_subalgorithm(selection_algorithms, "selection")
    counting = select_subalgorithm(counting_algorithms, "counting")

    if counting != counting_algorithms[0]: 
        betting = select_subalgorithm(betting_algorithms, "betting")
    else:
        betting = betting_algorithms[0] #no use in betting if no counting algorithm is selected




    #constants are passed to the algorithm not only to inform decision making, but also to save metadata about the simulation

    return BlackjackAlgorithm(selection, counting, betting, BASE_BET, DECKS, GAMES, STARTING_BALANCE)
    


if __name__ == "__main__":
    clear_screen()
    selection_algorithms = import_algoritms(algorithms.SelectionAlgorithm)
    counting_algorithms = import_algoritms(algorithms.CountingAlgorithm)
    betting_algorithms = import_algoritms(algorithms.BettingAlgorithm)

    algorithm = construct_algorithm(selection_algorithms, betting_algorithms, counting_algorithms)
    clear_screen()

    print("Algorithm Details:")
    algorithm.print_description()


    input("Press Enter to start the simulation...")
    clear_screen()
    print("Starting Blackjack Simulation...")


    for i in range(GAMES):
        deck = Deck(DECKS)
        betting_manager = BettingManager(STARTING_BALANCE)
        game(betting_manager, deck, algorithm)
        


    algorithm.save_scores()  #saves the scores to a file, so that they can be analyzed later
    print("Simulation complete. Thank you for playing!")
    


    

