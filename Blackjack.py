#
Blackjack
from itertools import count
import random

infinite = True

#config options
print("\nWelcome to BLACKJACK SIMULATOR")
print("Choose settings:")
print("Choose number of decks to shuffle together: ")
num_decks = int(input("Enter number of decks: "))
len_decks = num_decks * 52
print("Choose percentage (as a whole number) of decks at which to shuffle: ")
shuffle_perc = int(input("Enter shuffle percentage: "))
bet = int(input("Enter your starting bet : $"))
bank = 0

deck = []

def new_deck():
    std_deck = [
      # 2  3  4  5  6  7  8  9  10  J   Q   K   A
        2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11,
        2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11,
        2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11,
        2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11 
    ]

    #add more decks
    std_deck = std_deck * num_decks
    random.shuffle(std_deck)
    return std_deck

def cc(cards, count):
    for x in cards:
        if x in range(2, 6): count+=1
        elif x in range(7, 9): count = count
        elif x in range(10, 11): count-=1
        elif x == 1: count-=1
    return count

def play_hand(bank, bet):

    change_bet = str(input("Do you want to change your bet? Type yes or press Enter for no. "))
    if change_bet == "yes":
        bet = int(input("Enter your new bet: $"))
    print("\n")
    
    p_win = d_win = tie = 0
    count = 0

    dealer_cards = []
    player_cards = []

    # deal initial cards
    player_cards.append(deck.pop(0))
    dealer_cards.append(deck.pop(0))
    player_cards.append(deck.pop(0))  
    dealer_cards.append(deck.pop(0))    

    print("Dealer has [X,", str(dealer_cards[1]) + "]")
    print("You have: ", player_cards)

    p_sum = sum(player_cards)
    if p_sum == 21:
        print("Player BLACKJACK! \n")
        p_win+=1;
        bank+=bet
        return p_win, d_win, tie, count, bank

#split?
    split = False
    if player_cards[0] == player_cards[1]:
        action_taken = str(input("Do you want to split? Answer yes or no. "))
        if action_taken == "yes":
            split = True
            player_cards_1 = []
            player_cards_2 = []
            player_cards_1.append(player_cards[0])
            player_cards_1.append(deck.pop(0))
            player_cards_2.append(player_cards[1])
            player_cards_2.append(deck.pop(0))
            print("You now have a first total of " + str(sum(player_cards_1)) + " from these cards ", player_cards_1)
            action = str(input("Do you want to double? Type yes or press Enter for no. "))
            if action == "yes":
                bet = 2*bet
                print("Player bet doubled to: $" + str(bet)) 
            while sum(player_cards_1) < 21:
                action_taken = str(input("First hand: Do you want to stand or hit?  "))
                if action_taken == "hit":
                    player_cards_1.append(deck.pop(0))
                    if sum(player_cards_1) > 21:
                        for i in range(len(player_cards_1)):
                            if player_cards_1[i] == 11: 
                                player_cards_1[i] = 1
                            if sum(player_cards_1) < 21: break
                    print("You now have a first total of " + str(sum(player_cards_1)) + " from these cards ", player_cards_1)
                else: break
            print("You now have a second total of " + str(sum(player_cards_2)) + " from these cards ", player_cards_2)
            action = str(input("Do you want to double? Type yes or press Enter for no. "))
            if action == "yes":
                bet = 2*bet
                print("Player bet doubled to: $" + str(bet)) 
            while sum(player_cards_2) < 21:
                action_taken = str(input("Second hand: Do you want to stand or hit?  "))
                if action_taken == "hit":
                    player_cards_2.append(deck.pop(0))
                    if sum(player_cards_2) > 21:
                        for i in range(len(player_cards_2)):
                            if player_cards_2[i] == 11:
                                player_cards_2[i] = 1
                            if sum(player_cards_2) < 21: break
                    print("You now have a second total of " + str(sum(player_cards_2)) + " from these cards ", player_cards_2)
                else: break
            #count
            count+=cc(player_cards_1,count)
            count+=cc(player_cards_2,count)
            # player bust
            p_sum_1 = sum(player_cards_1)
            p_sum_2 = sum(player_cards_2)
            
# no split
    if split == False:
        # deal player 
        print("You have a total of " + str(sum(player_cards)) + " from these cards ", player_cards)
        action = str(input("Do you want to double? Type yes or press Enter for no. "))
        if action == "yes":
            bet = 2*bet      
            print("Player bet doubled to: $" + str(bet)) 
        while sum(player_cards) < 21:
            action_taken = str(input("Do you want to stand or hit?  "))
            if action_taken == "hit":
                player_cards.append(deck.pop(0))
                if sum(player_cards) > 21:
                    for i in range(len(player_cards)):
                        if player_cards[i] == 11:
                            player_cards[i] = 1
                        if sum(player_cards) < 21: break
                print("You now have a total  " + str(sum(player_cards)) + " from these cards ", player_cards)
            else: break
        count+=cc(player_cards, count)
        p_sum = sum(player_cards)
    
        # player bust
        if p_sum > 21: 
            print("Player BUST! \n")
            d_win+=1
            bank-=bet
            return p_win, d_win, tie, count, bank

    # deal dealer on soft 17
    while sum(dealer_cards) < 18:
        exit = False
        # check for soft 17
        if sum(dealer_cards) == 17:
            exit = True
            # check for an ace and convert to 1 if found
            for i, card in enumerate(dealer_cards):
                if card == 11:
                    exit = False
                    dealer_cards[i] = 1
        if exit: break
        dealer_cards.append(deck.pop(0))
        if sum(dealer_cards) > 21:
            for i in range(len(dealer_cards)):
                if dealer_cards[i] == 11:
                    dealer_cards[i] = 1
    print("The dealer now has: " + str(sum(dealer_cards)) + " from these cards ", dealer_cards)
    
    count+=cc(dealer_cards, count)
    d_sum = sum(dealer_cards)

    if split == False:
        # player bust
        if p_sum > 21:
            print("Player BUST!  \n")
            d_win+=1;
            bank-=bet
        #dealer bust
        elif d_sum > 21:
            print("Dealer BUST!  \n")
            p_win+=1;
            bank+=bet
        # dealer tie
        elif d_sum == p_sum:
            print("PUSH! \n")
            tie+=1
            bank = bank
        # dealer wins
        elif d_sum > p_sum:
            print("Dealer WINS!  \n")
            d_win+=1
            bank-=bet
        # dealer lose
        elif d_sum < p_sum:
            print("Player WINS!  \n")
            p_win+=1
            bank+=bet

    else: 
        for x in (p_sum_1, p_sum_2):
            # player bust
            if x > 21:
                print("Player BUST!  \n")
                d_win+=1
                bank-=bet
            #dealer bust
            elif d_sum > 21:
                print("Dealer BUST!  \n")
                p_win+=1
                bank+=bet
            # dealer tie
            elif d_sum == x:
                print("PUSH! \n")
                tie+=1
                bank = bank
            # dealer wins
            elif d_sum > x:
                print("Dealer WINS!  \n")
                d_win+=1
                bank-=bet
            # dealer lose
            elif d_sum < x:
                print("Player WINS!  \n")
                p_win+=1;
                bank+=bet
    return p_win,d_win,tie,count,bank

p_win_tot = d_win_tot = tie_tot = 0
count_setting = False
running_count = 0

print("\nBLACKJACK SIMULATOR")
print("Dealer stands on soft 17.")
print("Aces are 1 or 11; changing automatically.")
print("Decks used: " + str(num_decks))
print("Decks shuffled at: " + str(shuffle_perc) + "%")
print("Starting player bet: $" + str(bet))
print("Hi-Lo counting is turned OFF.\n")
action_count = str(input("Type ON to turn Hi-Lo count ON; otherwise press Enter. "))
if action_count == "ON":
    count_setting = True
    print("Hi-Lo counting is turned ON \n")
else: print("\n\n")

while infinite:
    deck = new_deck()
    while len(deck) > (100 - shuffle_perc)*len_decks/100:
        if count_setting == True:
            p,d,t,count,bank = play_hand(bank, bet) 
            running_count+=count
            print("Player Total Winnings: $" + str(bank) + "\n")
            print("Running count: " + str(running_count) + "\n")
        if count_setting == False:
            p,d,t,count,bank = play_hand(bank, bet) 
            running_count+=count
            print("Player Total Winnings: $" + str(bank) + "\n")
        p_win_tot+=p
        d_win_tot+=d
        tie_tot+=t
    print("\n SHUFFLING \n ")
    print("Player wins: " + str(p_win_tot))
    print("Dealer wins: " + str(d_win_tot))
    print("Ties: " + str(tie_tot))
    print("Player Cumulative Winnings: $" + str(bank) + "\n")
    
    running_count = 0


