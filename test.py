import tkinter as tk
import random

def deal_card(deck, hand, frame):
    card = deck.pop()
    hand.append(card)
    tk.Label(frame, text=card, font=("Arial", 14)).pack(side=tk.LEFT)

def calculate_score(hand):
    score = 0
    aces = 0
    for card in hand:
        rank = card[:-1]
        if rank in ["J", "Q", "K"]:
            score += 10
        elif rank == "A":
            aces += 1
            score += 11
        else:
            score += int(rank)
    while score > 21 and aces:
        score -= 10
        aces -= 1
    return score

def hit(deck, player_hand, player_frame, info_label, hit_button, stand_button):
    deal_card(deck, player_hand, player_frame)
    player_score = calculate_score(player_hand)
    if player_score > 21:
        info_label.config(text="You busted! Dealer wins.")
        end_game(hit_button, stand_button)

def stand(deck, dealer_hand, player_hand, dealer_frame, info_label, hit_button, stand_button):
    dealer_score = calculate_score(dealer_hand)
    while dealer_score < 17:
        deal_card(deck, dealer_hand, dealer_frame)
        dealer_score = calculate_score(dealer_hand)

    player_score = calculate_score(player_hand)
    if dealer_score > 21 or player_score > dealer_score:
        info_label.config(text="You win!")
    elif dealer_score == player_score:
        info_label.config(text="It's a tie!")
    else:
        info_label.config(text="Dealer wins.")
    end_game(hit_button, stand_button)

def end_game(hit_button, stand_button):
    hit_button.config(state="disabled")
    stand_button.config(state="disabled")





root = tk.Tk()
root.title("Blackjack")

deck = [str(rank) + suit for rank in list(range(2, 11)) + ["J", "Q", "K", "A"] for suit in "♠♥♦♣"]
random.shuffle(deck)

player_hand = []
dealer_hand = []


info_label = tk.Label(root, text="Welcome to Blackjack!")

buttons_frame = tk.Frame(root)
buttons_frame.pack()
hit_button = tk.Button(buttons_frame, text="Hit", command=lambda: hit(deck, player_hand, player_frame, info_label, hit_button, stand_button))
hit_button.grid(row=0, column=0, padx=10)
stand_button = tk.Button(buttons_frame, text="Stand", command=lambda: stand(deck, dealer_hand, player_hand, dealer_frame, info_label, hit_button, stand_button))
stand_button.grid(row=0, column=1, padx=10)
reset_button = tk.Button(buttons_frame, text="Reset", command=lambda: reset_game(deck, player_hand, dealer_hand, player_frame, dealer_frame, info_label, hit_button, stand_button))
reset_button.grid(row=0, column=2, padx=10)

reset_game(deck, player_hand, dealer_hand, player_frame, dealer_frame, info_label, hit_button, stand_button)

root.mainloop()
