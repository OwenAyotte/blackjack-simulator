from blackjack_core.blackjack_classes import Hand, Card
import json
import os

"""
Defines the BlackjackAlgorithm class, which itself contains 3 sub-algorithms for different stages of the game.
These sub-algorithms determine how the algorithm plays hands, its' card counting strategy, and betting strategy.

Sub-algorithms are subclasses of the SelectionAlgorithm, CountingAlgorithm, and BettingAlgorithm classes.
All unique sub-algorithms are imported into the betting_simulation.py module. 

Currently, most of the algorithms are either sourced from Wikipedia (in particular, the card counting ones) or incredibly simple. 
"""



class BlackjackAlgorithm:
    """Base class for Blackjack algorithms.
    This class is designed to serve as a collection of algorithms used in various stages of a Blackjack game.
    """




    def __init__(self, selection_alg, count_alg, betting_alg, base_bet, decks, games, starting_balance):
        self.all_scores = [] #list of lists scores for the algorithm, used to track performance across multiple rounds.
        self.current_scores = [] #list of scores for the current round, used to track performance in a single round.
        
        self.selection_alg= selection_alg
        self.count_alg = count_alg
        self.betting_alg = betting_alg
        self.base_bet = base_bet #The base bet amount, used to calculate the actual bet amount.
        self.decks = decks

        #these two aren't used in the algorithm, but are included in the json file for reference.

        self.games = games
        self.starting_balance = starting_balance 
        self.played_cards = [] #List of cards that have been played. 
        self.running_count = 0 #The Count, used to determine the quality of the deck.

          

    def make_selection(self, hand, dealer_hand):
        """Make a choice based on the current game state.
        This method should be overridden by subclasses."""
        return self.selection_alg.select(hand, dealer_hand)
    
      

    def count_card(self, card):
        """Updates the running count based on the card drawn.
        In addition, appends the card to the played_cards list."""
        count_change = self.count_alg.count(card)
        self.played_cards.append(card)
        return count_change
        
    def determine_bet(self):
        """Returns the bet amount based on the current count and the base bet.
        If the bet returned by this method is greater than the current balance, it will be capped at such outside this class."""


        if len(self.played_cards) != 0:
            true_count = self.running_count / (len(self.played_cards) / (self.decks * 52))
        else:
            true_count = 0



        bet = self.base_bet * self.betting_alg.get_bet_multiplier(self.running_count)
        bet = round(bet)  # Round to integer
        if bet < 1:
            bet = 1 # Ensure minimum bet is 1


        return bet

    def __str__(self):
        return f"{self.name}"
    
    def print_description(self):
        """Prints the descriptions of all sub_algorithms."""
        print(self.selection_alg.description())
        print(self.count_alg.description())
        print(self.betting_alg.description())
        
        
    
    def log_score(self, score):
        """Logs the score of the algorithm."""
        self.current_scores.append(score)

    def log_round(self):
        """Logs the current round's scores to the all_scores list. In addition, resets the current_scores and other data list for the next round."""

        self.all_scores.append(self.current_scores.copy())


        self.current_scores = []  # Reset current scores for the next round
        self.count = 0
        self.played_cards = []
        self.running_count = 0  # Reset running count for the next round

    def save_scores(self):
        """Saves the scores to a file."""

        

        notes = input("Enter any notes for this simulation run: ")

        file_name = self.determine_file_name()  


        simulation_data = {
            "name": self.betting_alg.__str__() + " - " + self.selection_alg.__str__() + " - " + self.count_alg.__str__(),
            "notes": notes,
            "base_bet": self.base_bet,
            "decks": self.decks,
            "games": self.games,
            "starting_balance": self.starting_balance,

            
        }


        #hypothetically i could just use json.dump on the simulation_data dict (w/ the scores in it), but the formatting would suck when read by a human
        #the below code formats it so that each unique round is on a new line



        metadata = simulation_data= json.dumps(simulation_data, indent=2)

        scores_lines = []
        for sublist in self.all_scores:
            scores_lines.append("  " + json.dumps(sublist))
            
        scores_json = "[\n" + ",\n".join(scores_lines) + "\n]" 

        final_json = metadata[:-2] + ',\n  "scores": ' + scores_json + "\n}"


        # Save to a file
        with open(file_name, "w") as f:
            f.write(final_json)

    def determine_file_name(self):
        """Prompts the user for a file name to save the scores to. Gives option for user to enter a custom file name or use a default one.
        If the file name already exists, it will append a number to the file name to avoid overwriting."""

        file_name_yn = ""
        while file_name_yn not in ["y", "n"]:
            file_name_yn = input("Do you want to use a custom file name? (y/n): ").strip().lower()

        if file_name_yn == "y":
            file_name = input("Enter the file name (without extension): ").strip()
        else:
            file_name = "simulation_results"



        file_number = ""
        divider = ""

        while os.path.exists(file_name + divider + str(file_number) + ".json"):
            if file_number == "":
                file_number = 1
                divider = "_"
            else:
                file_number += 1
            
        complete_file_name = file_name + divider + file_number + ".json"
            
        if file_number != "" and file_name_yn == "y":
            print("A file of that name already exists.")
        print(f"Saving results to {complete_file_name}")

        return complete_file_name

        
##########################################################
# Selection Algorithms
# These algorithms define if the player hits, doubles down, splits or stands.
##########################################################

class SelectionAlgorithm:
    """Base class for selection algorithms.
    This class is designed to serve as a the basis for algorithms used to determine if the player hits/doubles down/splits/stands.
    """

    def select(self, hand, dealer_hand):
        """Make a choice based on the current game state.
        This method should be overridden by subclasses."""
        raise NotImplementedError("This method should be overridden by subclasses.")
    
    def description(self):
        """Returns a description of the algorithm."""
        return "- No description. subclass must implement this method."
    
    def __str__(self):
        return "Default Selection Algorithm (do not use this!)"

class AlwaysHit(SelectionAlgorithm):
    """Always hits, regardless of the hand or dealer's hand."""
    def select(self, hand, dealer_hand):
        return "1"

    def description(self):
        return " - Always hits, regardless of the hand or dealer's hand, relying on landing a 21."

    def __str__(self):
        return "Always Hit"

class AlwaysStand(SelectionAlgorithm):
    """Always stands, regardless of the hand or dealer's hand."""
    def select(self, hand, dealer_hand):
        return "4"

    def description(self):
        return " - Always stands, regardless of the hand or dealer's hand."

    def __str__(self):
        return "Always Stand"

class MaxCaution(SelectionAlgorithm):
    """Hits on 11 or less, stands on 12 or more."""
    def select(self, hand, dealer_hand):
        if hand.get_total() <= 11:
            return "1"
        else:
            return "4"

    def description(self):
        return " - Hits on 11 or less, stands on 12 or more. Always avoids busting."

    def __str__(self):
        return "Max Caution"

class DealerStrategy(SelectionAlgorithm):
    """Implements the dealer's strategy: hits on 16 or less, stands on 17 or more."""
    def select(self, hand, dealer_hand):
        if hand.get_total() <= 16:
            return "1"
        else:
            return "4"

    def description(self):
        return " - Hits on 16 or less, stands on 17 or more."

    def __str__(self):
        return "Dealer Strategy"

##########################################################
# Counting Algorithms
# These algorithms alter the algorithm's count based on the cards drawn.
# Each implements a count(card) method and a description.
##########################################################

class CountingAlgorithm:
    """Base class for counting algorithms.
    This class is designed to serve as a collection of algorithms used to count cards in Blackjack.
    """

    def count(self, card):
        """Returns the modification to the count based on the card drawn.
        This method should be overridden by subclasses."""
        raise NotImplementedError("This method should be overridden by subclasses.")
    
    def description(self):
        """Returns a description of the algorithm."""
        return "- No description. Subclass must implement this method."
    
    def __str__(self):
        return "Default Counting Algorithm (do not use this!)"

class NoCardCount(CountingAlgorithm):
    """For algorithms that do not count cards, always returns 0."""
    def count(self, card):
        return 0

    def description(self):
        return " - No card counting."

    def __str__(self):
        return "No Card Count"

class HiLoCount(CountingAlgorithm):
    """Hi-Lo card counting algorithm."""
    def count(self, card):
        hi_lo_dict = {
            2: 1, 3: 1, 4: 1, 5: 1, 6: 1,
            7: 0, 8: 0, 9: 0,
            10: -1, 11: -1
        }
        value = card.get_value()
        return hi_lo_dict.get(value, 0)

    def description(self):
        return "2-6 = +1 | 7-9 = 0 | 10-Ace = -1."

    def __str__(self):
        return "Hi-Lo Count"

class HiOpt1Count(CountingAlgorithm):
    """Hi-Opt I card counting algorithm."""
    def count(self, card):
        hi_opt_1_dict = {
            3: 1, 4: 1, 5: 1, 6: 1,
            2: 0, 7: 0, 8: 0, 9: 0, 11: 0,
            10: -1
        }
        value = card.get_value()
        return hi_opt_1_dict.get(value, 0)

    def description(self):
        return "3-6 = +1 | 2/7-9/Ace = 0 | 10-K = -1."

    def __str__(self):
        return "Hi-Opt I Count"

class HiOpt2Count(CountingAlgorithm):
    """Hi-Opt II card counting algorithm."""
    def count(self, card):
        hi_opt_2_dict = {
            4: 2, 5: 2,
            2: 1, 3: 1, 6: 1, 7: 1,
            8: 0, 9: 0, 11: 0,
            10: -2
        }
        value = card.get_value()
        return hi_opt_2_dict.get(value, 0)

    def description(self):
        return "2-3/6-7 = +1 | 4-5 = +2 | 8-9/Ace = 0 | 10-K = -2."

    def __str__(self):
        return "Hi-Opt II Count"

class ZenCount(CountingAlgorithm):
    """Zen Count card counting algorithm."""
    def count(self, card):
        zen_count_dict = {
            4: 2, 5: 2,
            2: 1, 3: 1, 6: 1, 7: 1,
            8: 0, 9: 0, 
            11: -1,
            10: -2
        }
        value = card.get_value()
        return zen_count_dict.get(value, 0)

    def description(self):
        return "2-3/6-7 = +1 | 4-5 = +2 | 8-9 = 0 | Ace = -1 | 10-K = -2."

    def __str__(self):
        return "Zen Count"

class HalvesCount(CountingAlgorithm):
    """Halves card counting algorithm."""
    def count(self, card):
        halves_dict = {
            5: 1.5,
            3: 1, 4: 1, 6: 1,
            2: 0.5, 7: 0.5,
            8: 0,
            9: -0.5, 11: -0.5,
            10: -1
        }
        value = card.get_value()
        return halves_dict.get(value, 0)

    def description(self):
        return "2/7 = +0.5 | 3-4/6 = +1 | 5 = +1.5 | 8 = 0 | 9/Ace = -0.5 | 10-K = -1."

    def __str__(self):
        return "Halves Count"

class OmegaIICount(CountingAlgorithm):
    """Omega II card counting algorithm."""
    def count(self, card):
        omega_ii_dict = {
            4: 2, 5: 2,
            2: 1, 3: 1, 6: 1, 7: 1,
            8: 0, 9: 0, 11: 0,
            10: -2
        }
        value = card.get_value()
        return omega_ii_dict.get(value, 0)

    def description(self):
        return "2-3/6-7 = +1 | 4-5 = +2 | 8-9/Ace = 0 | 10-K = -2."

    def __str__(self):
        return "Omega II Count"
    

    

##########################################################
# Betting Algorithms
# These algorithms return a betting multiplier as a function of the current count.
##########################################################

class BettingAlgorithm:
    """Base class for betting algorithms.
    This class is designed to serve as a collection of algorithms used to determine the betting strategy based on the current count.
    """

    def get_bet_multiplier(self, count):
        """Returns the betting multiplier based on the current count.
        This method should be overridden by subclasses."""
        raise NotImplementedError("This method should be overridden by subclasses.")
    
    def description(self):
        """Returns a description of the algorithm."""
        return "- No description. Subclass must implement this method."
    
    def __str__(self):
        return "Default Betting Algorithm (do not use this!)"
    

class FlatBetting(BettingAlgorithm):
    """Flat betting algorithm, always bets the base amount."""
    def get_bet_multiplier(self, count):
        return 1

    def description(self):
        return " - Always bets the base amount, regardless of the count."

    def __str__(self):
        return "Flat Betting"

class SuddenShift(BettingAlgorithm):
    """Sudden shift betting algorithm, increases bet fivefold if count is 5 or more.
    If count is -5 or less, decreases bet to 1/5 of the base amount."""
    def get_bet_multiplier(self, count):
        if count >= 5:
            return 5
        elif count <+ -5:
            return 1/5
        else:
            return 1

    def description(self):
        return " - Bets 5x the base bet if count is 5 or more, and 1/5 of the base bet if count is -5 or less."

    def __str__(self):
        return "Sudden Rise Betting"
    
class LinearScale(BettingAlgorithm):
    """Linear scale betting algorithm, increases/decreases bet by a 20th of the base bet for each count above/below 0."""
    def get_bet_multiplier(self, count):
        if count > 0:
            return 1 + (count / 20)
        elif count < 0:
            return 1 - (abs(count) / 20)
        else:
            return 1

    def description(self):
        return " - Bet has 1/20th added/removed from it for every point on the count."

    def __str__(self):
        return "Linear Scale Betting"

class TimeBider(BettingAlgorithm):
    """Algorith that returns 0 unless the count is above 10, in which case bet, returns 20. """
    def get_bet_multiplier(self, count):
        if count > 10:
            return 20
        else:
            return 0

    def description(self):
        return " - Bets 1 chip, until count is above 10. Then bets 20x the base bet."

    def __str__(self):
        return "Time Bider"