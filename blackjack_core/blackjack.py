from blackjack_core.blackjack_classes import Deck, Hand
from blackjack_core.utility import clear_screen, continue_prompt, unpack_hands, sort_hands, BettingManager
from blackjack_core.game_logic import play_hand, split_hand, calculate_blackjack_payout, dealer_hits, print_and_score_hands
from blackjack_core.constants import MAX_DECKS

"""
Modification of blackjack program, designed to collect data regarding the preformance of blackjack algorithms.
Same as original blackjack.py available on my github page, with print statements and input prompts gutted, 
and with player actions being determined by the algorithm defined in algorithms.py.
"""



    



def blackjack_round(deck, betting_manager, algorithm):
    """Runs a round of blackjack, returns payout for the player."""
    payout = 0
    


    #initalizes hands for dealer and player
    player_hand = Hand(deck, "PLAYER", algorithm)
    dealer_hand = Hand(deck, "DEALER", algorithm, hidden=True)

    
    


    completed_hands = play_hand(player_hand, dealer_hand, deck, betting_manager, algorithm) 
    #returns a list of hands,w/ multiple hands/sublists if the player has split

    

    all_hands = unpack_hands(completed_hands) #unpacks all hands into a single list of hands

   



 
    busted_hands = [] #list of hands that are busts
    non_busted_hands = [] #list of hands that are not busts, as well as not blackjacks
    blackjack_hands = [] #list of hands that are blackjacks

    for hand in all_hands: #for each hand, check if it is a bust     
        if hand.check_bust():
            busted_hands.append(hand)
        elif hand.blackjack_check():
            blackjack_hands.append(hand)
        else:
            non_busted_hands.append(hand)

            
    
    dealer_hand.unhide()
    


    payout += calculate_blackjack_payout(blackjack_hands, dealer_hand, betting_manager) #calculates payout for blackjacks, if any exist

    if not blackjack_hands and dealer_hand.blackjack_check(): #if dealer is the only one with a blackjack, print message and return 0 payout
            
            return 0




    
        

    if not non_busted_hands: 
        pass
        
        return payout #if there are no non-busted hands, payout is returned early instead of going through the rest of the payout checks
    

    #dealer hits, if they bust, payout is returned early
    dealer_bust_payout = dealer_hits(dealer_hand, non_busted_hands, betting_manager) 
    if dealer_bust_payout != 0: 
        payout += dealer_bust_payout 
     
        return payout 
    
            



    sorted_hands = sort_hands(non_busted_hands, dealer_hand) #sorts hands into losing, tieing and winning hands

    for i in range(len(sorted_hands)):
        payout += print_and_score_hands(sorted_hands[i], i, betting_manager)
                

    return payout

def game(betting_manager, deck, algorithm):
    """Runs blackjack with the same deck and bet amount until the player either requests to stop or runs out of money.
    Returns True if the player wants to continue playing, False if they want to stop."""
    





    
    while deck.is_fresh() and (betting_manager.get_balance() > 0):
        algorithm.log_score(betting_manager.get_balance()) #logs the players balance at the start of the round

     

        betting_manager.set_bet(algorithm.determine_bet()) #gets the bet amount from the algorithm, sets it in the betting manager 

        if betting_manager.get_bet() >= betting_manager.get_balance(): 
            betting_manager.set_bet(betting_manager.get_balance()) #if the bet is greater than the balance, set it to the balance


        betting_manager.make_bet()
       

            
        
        
        round_payout = blackjack_round(deck, betting_manager, algorithm)
        betting_manager.payout(round_payout) 

       

    if deck.is_fresh():
        #this is only done if the deck has not been replenished, to simulate stopping the game before that point
        
        algorithm.log_score(betting_manager.get_balance()) 


    algorithm.log_round()  #logs the entire round
    


        
        
    
def bet_input_validation(bet, betting_manager):
    """Validates the bet input (handles cases where input is non-int, negative and exceeding balance). 
    Returns True if valid, False if not. Additionally, prints an error message if the bet is invalid."""
    try:
        bet = int(bet)  # Converts bet to int
    except ValueError:
        print("Bet must be an integer!")
        return False

    if bet <= 0:
        print("Bet must be greater than 0!")
        return False

    if bet > betting_manager.get_balance():
        print("You cannot bet more than you have!")
        return False

    betting_manager.set_bet(bet)
    return True
        

def deck_input_validation(deck_amount, deck_exists):
    """Validates the deck amount input (handles cases where input is non-int, negative and exceeding max).
    Returns True if valid, False if not. Additionally, prints an error message if the deck amount is invalid."""

    if deck_amount == "": #if the input is empty, check if deck exists, if so do not replace it
        if deck_exists:
            return True
        else: 
        
            return False
    try:
        deck_amount = int(deck_amount) 
    except ValueError:
        
        return False

    if deck_amount <= 0:
        
        return False

    if deck_amount > MAX_DECKS: 
        
        return False

    return True


def main():
    LINK = "LINK TO BLACKJACK PROGRAM DO NOT FORGET DO NOT FORGET"  

    print("Sorry, it would appear that you are trying to run the blackjack.py file directly.")
    print("This version of blackjack.py is designed to be run through the betting_simulation.py file, which will handle the algorithm selection and other setup.")
    print(f"If you would like to play blackjack without an algorithm, please use the program at: {LINK}")

        


if __name__ == "__main__":
    main()


    