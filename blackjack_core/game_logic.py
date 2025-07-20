from blackjack_core.blackjack_classes import Hand
from blackjack_core.constants import BLACKJACK_PAYOUT_RATIO, TIE_PAYOUT_RATIO, WIN_PAYOUT_RATIO, LOSS_PAYOUT_RATIO
from blackjack_core.utility import continue_prompt, clear_screen



         
def split(deck, hand):
    """NOT TO BE USED DIRECTLY, USE split_hand INSTEAD!
    Takes a hand, and returns two hands featuring the cards from it as well as an additional card.
    Only works if the hand only has two cards and cards share a value (not to be confused with sharing a rank)."""
    if len(hand.cards) != 2:
        
        return None

    if hand.cards[0].get_value() != hand.cards[1].get_value():
        return None

    #creates two new hands with the first card of the original hand
    first_hand = Hand(deck, "PLAYER", starting_card=hand.cards[0])
    second_hand = Hand(deck, "PLAYER", starting_card=hand.cards[1])

    return [first_hand, second_hand]


def split_hand(hand, dealer_hand, deck, betting_manager,algorithm):
    """Calls split function, if successful, allows each split hand to be played and returns them in a list.""" 


    if betting_manager.can_increment_split() == False: #if player has already split 3 times
        pass
    elif betting_manager.can_make_bet() == False: 
        pass
    else:
        new_hands = split(deck, hand) #attempts to split the hand, returns two new hands if successful, None if not
        if new_hands is None:
            pass
        else:
            betting_manager.make_bet() 
            #Recursively calls play_hand on the two new hands
            first_hand = play_hand(new_hands[0], dealer_hand, deck, betting_manager, algorithm) 
            second_hand = play_hand(new_hands[1], dealer_hand, deck, betting_manager, algorithm)
            return [first_hand, second_hand] #list will be unpacked into individual hands in blackjack_round
        
    return None #if the split was not successful, return None
        
        

def calculate_blackjack_payout(blackjack_hands, dealer_hand, betting_manager):
    """Manages payout in the case of a blackjack beng possessed by the user. 
    Returns payout for all user hands that are blackjacks."""
    blackjack_payout = 0 

    if blackjack_hands: #if there are any blackjacks in the user's hands, print them before progessing to non-busts

      
        

        if dealer_hand.blackjack_check():
            #if the dealer also has a blackjack, all blackjacks award the inital betting amount back
       
            
            for hand in blackjack_hands:
                #note that this function doesn;t check if the hand is doubled down, as blackjacks are not allowed to be doubled down
                #since doing so would require a 3rd card to be drawn
                blackjack_payout += betting_manager.get_bet()  * TIE_PAYOUT_RATIO
                blackjack_payout = round(blackjack_payout) #rounds payout to nearest dollar
                #rounding to the nearest dollar is only done with blackjacks, as otherwise the payout is already an integer
            

        else:
            
            for hand in blackjack_hands:
                
                blackjack_payout += betting_manager.get_bet() * BLACKJACK_PAYOUT_RATIO
                blackjack_payout = round(blackjack_payout) #rounds payout to nearest dollar


        
    
    return blackjack_payout 

def dealer_hits(dealer_hand, non_busted_hands, betting_manager):
    """Allows the dealer to hit until they have at least 17.
    Returns payout of all non-busted hands if dealer busts, otherwise 0."""

    payout = 0 

    dealer_has_hit= False #used to check if dealer has hit at least once, used to avoid re-printing dealer hand if it isnt modified 
    if dealer_hand.get_total() < 17: #if dealer has less than 17 dealer must hit
        pass
    while dealer_hand.get_total() < 17: #dealer must hit until they have at least 17
        dealer_hand.draw()
        dealer_has_hit = True 

      

    

        if dealer_hand.check_bust(): #if dealer busts, all user hands are winners
            

            for hand in non_busted_hands:
         
                payout += betting_manager.get_bet() * hand.get_doubled_down() * WIN_PAYOUT_RATIO 
            return payout #ends round, all non-busted hands win
        



    return 0


def handle_misc_hands(hands, multiplier, betting_manager):
    """Handles hands that are scored after the dealer has hit, opposed to ones such as blackjacks and busts. 
    Returns the payout."""
    if not hands:
        return 0
    
  
    payout = 0    
    
    for hand in hands:
        
        #multiplier inuitively handles win/push/tie payout amounts
        payout += betting_manager.get_bet() * hand.get_doubled_down() * multiplier 


    return payout

        
def dealer_hits(dealer_hand, non_busted_hands, betting_manager):
    """Allows the dealer to hit until they have at least 17.
    Returns payout of all non-busted hands if dealer busts, otherwise 0."""

    payout = 0 

    
    while dealer_hand.get_total() < 17: #dealer must hit until they have at least 17
        dealer_hand.draw()
        
    

        if dealer_hand.check_bust(): #if dealer busts, all user hands are winners
            for hand in non_busted_hands:
                payout += betting_manager.get_bet() * hand.get_doubled_down() * WIN_PAYOUT_RATIO 
            return payout #ends round, all non-busted hands win
        


    return 0




def play_hand(hand, dealer_hand, deck, betting_manager, algorithm):
    """Allows player to hit, double down, split, or stand.
    Returns the payout for the player."""

    failed_action = False #used to check if an action has failed, such as not having enough money to double down or split
    
    OPTION_CHOICER = """What would you like to do?\n\t1. Hit\n\t2. Double Down\n\t3. Split\n\t4. Stand"""
    

    
    while (hand.check_standing() == False): #busting/reaching 21 sets standing to True (check draw card method of Hand), so both cases are covered
        

        player_selection = algorithm.make_selection(hand, dealer_hand) #uses the algorithm to make a selection

        
        if failed_action: #if an action has failed, the player is forced to stand
            #later iterations of this code may allow for algorithms to handle such actions themselves, but this is the most direct way to do so
            #besides, in most cases the algorithms are simple enough that such simple handling is fitting
            player_selection = algorithm.second_choice(hand, dealer_hand)



        if player_selection == "1": #HIT
            #Draw card
            hand.draw()

        elif player_selection == "2": #DOUBLE DOWN
            if betting_manager.make_bet(): #ensures that the player has enough money to double down
                hand.draw()
                hand.double_down()
                hand.stand() #automatically stands after doubling down
                
                
            else:
                failed_action = True #if the player does not have enough money to double down, set failed_action to True

           

        elif player_selection == "3": #SPLIT
            #split hand function plays the two new hands to completion
            #so function output can be returned directly in the case where the split is successful
            split_result = split_hand(hand, dealer_hand, deck, betting_manager)
            if split_result is not None:
                return split_hand(hand, dealer_hand, deck, betting_manager)
            else:
                failed_action = True
            
            

        elif player_selection == "4": #STAND
            #Set standing to True, ends loop and lets dealer start hitting
            hand.stand()

        

        

        


    return hand 