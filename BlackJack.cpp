#include <iostream>
#include <vector>
#include <algorithm>
#include <ctime>
#include <cstdlib>
#include <unistd.h>
#include <sys/wait.h>
#include <fcntl.h>

using namespace std;

struct Card {
    string suit;
    string rank;
    int value;
};

class Deck {
public:
    Deck() {
        for (const string& suit : {"Hearts", "Diamonds", "Clubs", "Spades"}) {
            for (const string& rank : {"2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"}) {
                int value = (rank == "A") ? 11 : (rank == "K" || rank == "Q" || rank == "J") ? 10 : stoi(rank);
                cards.push_back({suit, rank, value});
            }
        }
        srand(time(0));
        random_shuffle(cards.begin(), cards.end());
    }

    Card drawCard() {
        Card drawn = cards.back();
        cards.pop_back();
        return drawn;
    }

private:
    vector<Card> cards;
};

class Player {
public:
    void addCard(Card card) {
        hand.push_back(card);
        score += card.value;
    }

    int getScore() const {
        return score;
    }

    void showHand() const {
        for (const Card& card : hand) {
            cout << card.rank << " of " << card.suit << " ";
        }
        cout << endl;
    }

    string getHand() const {
        string hand_str;
        for (const Card& card : hand) {
            hand_str += card.rank + " of " + card.suit + " ";
        }
        return hand_str;
    }

private:
    vector<Card> hand;
    int score = 0;
};

void playBlackjack(int read_fd, int write_fd) {
    Deck deck;
    Player player, dealer;

    // start
    player.addCard(deck.drawCard());
    dealer.addCard(deck.drawCard());
   

    // kojeka gracza
    while (true) {
        string message = "Your hand: " + player.getHand() + "\nYour score: " + to_string(player.getScore()) + "\nDo you want to hit or stand? ";
        write(write_fd, message.c_str(), message.size());

        char buffer[1024] = {0};
        read(read_fd, buffer, 1024);
        string response(buffer);
        response.erase(remove(response.begin(), response.end(), '\n'), response.end()); 

        if (response == "stand") {
            break;
        } else if (response == "hit") {
            player.addCard(deck.drawCard());
            if (player.getScore() > 21) {
                write(write_fd, "You busted!\n", 12);
                return;
            }
        }
    }

    // kolej krupiera
    while (dealer.getScore() < 19) {
        dealer.addCard(deck.drawCard());
    }

    // wynik
    int player_score = player.getScore();
    int dealer_score = dealer.getScore();
    string result;
    if (dealer_score > 21 || player_score > dealer_score) {
        result = "You win!";
    } else if (player_score < dealer_score) {
        result = "Dealer wins!";
    } else {
        result = "It's a tie!";
    }

    string message = "Dealer's hand: " + dealer.getHand() + "\nDealer's score: " + to_string(dealer.getScore()) + "\n" + result + "\n";
    write(write_fd, message.c_str(), message.size());
}

int main() {
    int player_to_dealer[2];
    int dealer_to_player[2];

    if (pipe(player_to_dealer) == -1 || pipe(dealer_to_player) == -1) {
        cerr << "Pipe failed!" << endl;
        return 1;
    }

    pid_t pid = fork();
    if (pid < 0) {
        cerr << "Fork failed!" << endl;
        return 1;
    }

    if (pid == 0) { // Child - Gracz
        close(player_to_dealer[0]);
        close(dealer_to_player[1]);

        while (true) {
            char buffer[1024] = {0};
            int bytes_read = read(dealer_to_player[0], buffer, 1024);
            if (bytes_read > 0) {
                cout << buffer << flush;

                string response;
                getline(cin, response);
                response += "\n";
                write(player_to_dealer[1], response.c_str(), response.size());

                if (response == "stand\n") {
                    break;
                }
            }
            usleep(100000); 
        }

        // komunikat o wyinku
        char buffer[1024] = {0};
        read(dealer_to_player[0], buffer, 1024);
        cout << buffer << flush;

        close(player_to_dealer[1]);
        close(dealer_to_player[0]);

    } else { // Parent - krupier
        close(player_to_dealer[1]);
        close(dealer_to_player[0]);

        playBlackjack(player_to_dealer[0], dealer_to_player[1]);

        close(player_to_dealer[0]);
        close(dealer_to_player[1]);

        wait(NULL); // czeka aż child sie skończy
    }

    return 0;
}
