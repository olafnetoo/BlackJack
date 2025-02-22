
import tkinter as tk
import random

def deal_card(deck, hand, frame):
    card = deck.pop()
    hand.append(card)
    tk.Label(frame, text=card, font=("Arial Black", 14)).pack(side=tk.LEFT)

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

def hit(deck, player_hand, player_frame, info_label, hit_button, stand_button, player_score_label, dealer_score_label, scores):
    deal_card(deck, player_hand, player_frame)
    player_score = calculate_score(player_hand)
    if player_score > 21:
        info_label.config(text="Za dużo! Kasyno wygrywa")
        scores["Kasyno"] += 1
        update_scores(player_score_label, dealer_score_label, scores, info_label)
        end_game(hit_button, stand_button)

def stand(deck, dealer_hand, player_hand, dealer_frame, info_label, hit_button, stand_button, player_score_label, dealer_score_label, scores):
    dealer_score = calculate_score(dealer_hand)
    while dealer_score < 16:
        deal_card(deck, dealer_hand, dealer_frame)
        dealer_score = calculate_score(dealer_hand)

    player_score = calculate_score(player_hand)
    if dealer_score > 21 or player_score > dealer_score:
        info_label.config(text="Wygrałeś!")
        scores["Gracz"] += 1
    elif dealer_score == player_score:
        info_label.config(text="Remis")
    else:
        info_label.config(text="Kasyno wygrywa")
        scores["Kasyno"] += 1

    update_scores(player_score_label, dealer_score_label, scores, info_label)
    end_game(hit_button, stand_button)

def end_game(hit_button, stand_button):
    hit_button.config(state="disabled")
    stand_button.config(state="disabled")

def reset_game(deck, player_hand, dealer_hand, player_frame, dealer_frame, info_label, hit_button, stand_button, player_score_label, dealer_score_label, scores):
    if scores["Gracz"] >= 5:
        info_label.config(text="Gratulacje , ograłeś kasyno , jesteś bogaty")
        disable_buttons(hit_button, stand_button)
        return
    elif scores["Kasyno"] >= 5:
        info_label.config(text="Kasyno tym razem wygrało ")
        disable_buttons(hit_button, stand_button)
        return

    deck.clear()
    deck.extend([str(rank) + suit for rank in list(range(2, 11)) + ["J", "Q", "K", "A"] for suit in "♠♥♦♣"])
    random.shuffle(deck)

    player_hand.clear()
    dealer_hand.clear()

    for widget in player_frame.winfo_children():
        widget.destroy()
    for widget in dealer_frame.winfo_children():
        widget.destroy()

    deal_card(deck, player_hand, player_frame)
    deal_card(deck, player_hand, player_frame)
    deal_card(deck, dealer_hand, dealer_frame)

    info_label.config(text="Hit or Stand?")
    hit_button.config(state="normal")
    stand_button.config(state="normal")

def update_scores(player_score_label, dealer_score_label, scores, info_label):
    player_score_label.config(text=f"Wygrane Gracza: {scores['Gracz']}")
    dealer_score_label.config(text=f"Wygrane Kasyna: {scores['Kasyno']}")

def disable_buttons(hit_button, stand_button):
    hit_button.config(state="disabled")
    stand_button.config(state="disabled")

window = tk.Tk()
window.title("Blackjack")

deck = [str(rank) + suit for rank in list(range(2, 11)) + ["J", "Q", "K", "A"] for suit in "♠♥♦♣"]
random.shuffle(deck)

player_hand = []
dealer_hand = []
scores = {"Gracz": 0, "Kasyno": 0}

player_frame = tk.Frame()
player_frame.pack(pady=10)
dealer_frame = tk.Frame()
dealer_frame.pack(pady=10)

info_label = tk.Label( text="Zagrajmy w Blackjack! Pierwsza runda w ciemno")
info_label.pack(pady=10)

score_frame = tk.Frame()
score_frame.pack(pady=10)
player_score_label = tk.Label(score_frame, text="Wygrane Gracza: 0")
player_score_label.pack(side=tk.LEFT, padx=10)
dealer_score_label = tk.Label(score_frame, text="Wygrane Kasyna: 0")
dealer_score_label.pack(side=tk.RIGHT, padx=10)

buttons_frame = tk.Frame()
buttons_frame.pack()
hit_button = tk.Button(buttons_frame, text="Hit", command=lambda: hit(deck, player_hand, player_frame, info_label, hit_button, stand_button, player_score_label, dealer_score_label, scores))
hit_button.grid(row=0, column=0, padx=10)
stand_button = tk.Button(buttons_frame, text="Stand", command=lambda: stand(deck, dealer_hand, player_hand, dealer_frame, info_label, hit_button, stand_button, player_score_label, dealer_score_label, scores))
stand_button.grid(row=0, column=1, padx=10)
reset_button = tk.Button(buttons_frame, text="Reset", command=lambda: reset_game(deck, player_hand, dealer_hand, player_frame, dealer_frame, info_label, hit_button, stand_button, player_score_label, dealer_score_label, scores))
reset_button.grid(row=0, column=2, padx=10)

#reset_game(deck, player_hand, dealer_hand, player_frame, dealer_frame, info_label, hit_button, stand_button, player_score_label, dealer_score_label, scores)

window.mainloop()
