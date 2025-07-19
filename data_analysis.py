import numpy as np
import matplotlib.pyplot as plt
import json
from blackjack_core.utility import clear_screen, continue_prompt


"""This module serves as a tool analyzing and visualizing simulation results of a blackjack algorithm.
In particular, it graphs both the average score of each round as well as the individual scores of each round.
A linear fit can be plotted on top of this, but that's up to user discretion due to the fact that the data may not have a linear trend.
Additional information such as standard deviation of final scores and average profit/loss is also printed to the console.



Truth be told, it's mostly a proof of concept, since I doubt the data needs to be analyzed with particular depth.
Future commits may increase amount of things this module does, but for the time being I'm satisfied with it being basic.

"""

# Default alpha value defined here, so it can be easily changed in one place
# In the event that multiple simulations contain roughly the same amount of scores, changing the value while running the program would grow tedious.
DEFAULT_ALPHA = 0.04




def fill_missing_scores(scores):    
    """
    Equalizes lengths of sublists contained in scores by repeating the last entry.
    Returns the modified scores and the length of the longest run.
    """

    longest_run = 0


    
    for run in scores:
        if len(run) > longest_run:
            longest_run = len(run)

    for run in scores:
        while len(run) < longest_run:
            run.append(run[-1])

    return scores, longest_run

def average_scores(scores):
    """
    Returns a numpy array containing the average score of each round.
    """
    return np.mean(scores, axis=0)

def plot_all_scores(scores_array, alpha_value):
    """Plots every data point in given array."""
    unique_x_values = np.arange(scores_array.shape[1])
    # Create a repeated x array for each score in the scores_array
    x = np.tile(unique_x_values, scores_array.shape[0])


    all_points = plt.scatter(x, scores_array.flatten(), color="#4747ff", alpha=alpha_value,s =7, edgecolors="none", label="Chips per Round")
    return all_points

def plot_averages(averages):
    """Plots the average of each round."""
    averages, = plt.plot(range(len(averages)), averages, "o", color="#ff5722", label = "Average Score")
    return averages

def plot_linear_fit(averages):
    """Attempts to plot a linear fit using the average scores. """

    x = range(len(averages))
    coeffs = np.polyfit(range(len(averages)), averages, deg=1)
    polynomial_function = np.poly1d(coeffs)
    lin_fit, = plt.plot(range(len(averages)), polynomial_function(x), color="#49c131", linewidth = 4, label="Linear Fit")

    return lin_fit


    


def get_survival_metrics(scores, round_number=-1):
    """Returns a np array containing the rounds lasted of each game played, 
    as well as a np array consisting of boolean operators denoting whether the game resulted in a bust.
    The round number can be specified, if not, the last round is used by default."""


    rounds_lasted = []
    bust_states = []

    for i in scores:
        rounds_lasted.append(len(i))
        if i[round_number] == 0:
            bust_states.append(True)
        else:
            bust_states.append(False)

    rounds_lasted = np.array(rounds_lasted)
    bust_states = np.array(bust_states)



    return rounds_lasted, bust_states

def analyse_survival_metrics(rounds_lasted, bust_states):
    """Returns the average amount of rounds lasted by the algorithm, as well as the percentage of games that ended in a bust"""

    average = np.average(rounds_lasted)

    bust_percentage = (np.sum(bust_states == True) / len(bust_states)) / 100

    return average, bust_percentage


def get_standard_deviation(all_scores, round_number=-1):
    """Returns the standard deviation of the scores of the specified round across all runs."""


    round_scores = np.array([round[round_number] for round in all_scores])
    return np.std(round_scores)

def get_mean_score(scores_collection, round_number=-1):
    """Returns the mean score of the specified round across all runs."""

    return np.mean([run[round_number] for run in scores_collection])

def print_statistics(scores_collection, starting_balance, round_number=-1):
    """Prints statistics about the simulation results."""



    rounds_lasted, bust_states = get_survival_metrics(scores_collection, round_number)
    average_rounds_lasted, bust_percentage = analyse_survival_metrics(rounds_lasted, bust_states)



    #Handles differences  in analysis between user inputted round and automatically examined last round   
    if round_number == -1:
        round_description = "final round"
        print(f"The longest run lasted {scores_collection.shape[1]} rounds.")
        print(f"Average amount of rounds lasted by algorithm: {average_rounds_lasted:.2f}")
    else:
        round_description = f"round #{round_number}"

    
   
    print(f"Percentage of rounds that ended in a Bust by {round_description}: {bust_percentage:.2f}%")
    print(f"Average profit/loss after {round_description}: {get_mean_score(scores_collection, round_number) - starting_balance:.2f} chips")
    print(f"Standard deviation of scores after {round_description}: {get_standard_deviation(scores_collection, round_number):.2f}")


def display_graph(averages, alpha_value, scores_collection, show_averages, show_all_scores, show_linear_fit):
    """Displays the graphs of the averages and all scores. Sets visibility of the plots based on 3 boolean parameters."""

    plt.xlabel("Round Number")
    plt.ylabel("Chips")
    

    averages_plot = plot_averages(averages)
    all_scores_plot = plot_all_scores(scores_collection, alpha_value)
    lin_fit_plot = plot_linear_fit(averages)

    averages_plot.set_visible(show_averages)
    all_scores_plot.set_visible(show_all_scores)    
    lin_fit_plot.set_visible(show_linear_fit)

    handles = []
    labels = []

    if show_all_scores:
        # Mimics scatter format, to get around issues with legend displaying plots with high alpha transparantly
        mimic_scatter = plt.scatter([], [], color="#4747ff", label="Chips per Round", alpha=1, s=30)
        handles.append(mimic_scatter)
        labels.append("Chips per Round")

    if show_averages:
        handles.append(averages_plot)
        labels.append("Average Score")

    if show_linear_fit:
        handles.append(lin_fit_plot)
        labels.append("Linear Fit")


    plt.legend(handles, labels, loc="upper left")
    plt.show()


def print_algorithm_details(data, file_name):
    """Prints the details of the algorithm used in the simulation."""
    print(file_name)
    print(data["name"])
    print(f"\tNotes: {data['notes']}")
    print(f"\tBase Bet: {data['base_bet']}")
    print(f"\tDecks: {data['decks']}")
    print(f"\tGames: {data['games']}")
    print(f"\tStarting Balance: {data['starting_balance']}")
    print()
    


def main():
    clear_screen()

    file_name = input("Enter the name of the file containing the simulation results (leave empty for: simulation_results.json): ").strip()
    if file_name == "":
        file_name = "simulation_results.json"
    elif not file_name.endswith(".json"):
        file_name += ".json"

    try:
        with open(file_name) as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"File '{file_name}' not found. Please check the file name and try again.")
        return
    

    alpha_value = DEFAULT_ALPHA  
    scores_collection = data["scores"]
    starting_balance = data["starting_balance"]

    scores_collection, most_rounds = fill_missing_scores(scores_collection)
    scores_collection = np.array(scores_collection)


    

    averages = average_scores(scores_collection)

    clear_screen()

    print_algorithm_details(data, file_name)
    print_statistics(scores_collection, starting_balance, -1)

    show_averages = True
    show_all_scores = True
    show_linear_fit = False

    # Dictionary to dynamically change the prompt messages based on if they'd hide or show the a specific plot
    show_hide = {True: "Hide", False: "Show"}

    continue_prompt("\nPress Enter to display the graph.")

    display_graph(averages, alpha_value, scores_collection, show_averages, show_all_scores, show_linear_fit)

    
    continue_prompt()



    choice = None

    while choice != "3":
        clear_screen()
        print("Would you like to view statistics for a specific round cutoff, alter the graphs, or exit?")
        print("Enter your choice: ")
        print("\t1. View statistics for specified round cutoff.\n\t2. Alter graphs.\n\t3. Exit.")
        choice = input(" >").strip()
        if choice == "1":
            print()
            try:
                round_number = int(input("Enter the round number to analyze: ").strip())

            # validate the input
            except ValueError:
                print("Invalid input. Please enter a valid round number.")
                continue
            if round_number < 0 or round_number >= scores_collection.shape[1]:
                print("Round number out of range. Please enter a valid round number.")
                continue

            print_statistics(scores_collection, starting_balance, round_number)

        elif choice == "2":
            graphing_choice = None
            while graphing_choice != "6":
                clear_screen()
                print("Graphing options:")
                print(f"\t1. {show_hide[show_linear_fit]} linear fit\n\t2. {show_hide[show_all_scores]} all scores\n\t3. {show_hide[show_averages]} averages\n\t4. Change alpha value of all scores ({alpha_value})\n\t5. Show Graph \n\t6. Exit")
                graphing_choice = input(" >").strip()


                if graphing_choice == "1":
                    
                    show_linear_fit = not show_linear_fit
                    print(f"Linear fit is now {'visible' if show_linear_fit else 'hidden'}.")
                    
                
                elif graphing_choice == "2":
                    show_all_scores = not show_all_scores
                    print(f"All scores are now {'visible' if show_all_scores else 'hidden'}.")

                    
                elif graphing_choice == "3":
                    show_averages = not show_averages
                    print(f"Averages are now {'visible' if show_averages else 'hidden'}.")
                    

                elif graphing_choice == "4":
                    #sets the alpha value of all scores
                    print("Due to the different amount of scores this program can graph, the default alpha value may not fit your needs.")
                    print(f"Current alpha value is {alpha_value}.")
                    print("Please enter a new alpha value (between 0 and 1): ")
                    try:
                        new_value = float(input(" >").strip())
                        if new_value < 0 or new_value > 1:
                            raise ValueError
                        
                    except ValueError:
                        print("Invalid input. Please enter a valid alpha value between 0 and 1.")
                        continue_prompt()

                        continue


                    alpha_value = new_value
                    print("Alpha value set to", alpha_value)
                    continue_prompt
                   

                    

                    

                elif graphing_choice == "5":
                    display_graph(averages, alpha_value, scores_collection, show_averages, show_all_scores, show_linear_fit)

                    
                            


                else:
                    print("Invalid choice. Please try again.")
           

            
            
 


    

    


if __name__ == "__main__":
    main()


