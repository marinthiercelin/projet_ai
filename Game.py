# game class
from Deck import Deck
from enum import Enum
import HandComparator
from random import randrange
from player import player, action


class Stage(Enum):
    preflop = 1
    flop = 2
    turn = 3
    river = 4
    showdown = 5


comparator = HandComparator.HandComparator()


class Game(object):
    # Init takes an array of players and the number of players set to 1
    # Blinds are the first chips to play the game
    def __init__(self, player1, player2, blind, bet_value, deck=None):
	self.bet_value = bet_value
        self.dealer = player1  # Second to play
        self.small_blind = player2  # First to play
        self.community_cards = []
        if deck is None:
            self.deck = Deck()
        else:
            self.deck = deck
        self.blind = blind
        self.pot = 0  # Sum of all bets for the game
        self.stage = Stage.preflop

    # Instructs players to put blind bets in their current bet
    def collect_blinds(self):
        self.small_blind.place_bet(self.blind / 2.0)
        self.dealer.place_bet(self.blind)

    # Shuffles the deck and gives two cards to each player
    def deal(self):
        self.deck.restart()
        self.small_blind.collect_cards(self.deck.get(2))
        self.dealer.collect_cards(self.deck.get(2))

    def start_game(self):
        name1 = self.dealer.name
        name2 = self.small_blind.name
        counter1 = 0  # number of round won by player1
        counter2 = 0  # number of round won by player2
        counterD = 0  # number of draw
        while self.dealer.chips != 0 and self.small_blind.chips != 0:  # Play until no player has money
            print "########################################\n"
            print self.dealer.name + " is the dealer\n"
            self.small_blind.new_hand()
            self.dealer.new_hand()
            print "Collecting blinds\n"
            self.collect_blinds()
            self.deal()

            while not self.play_round():
                print"----------------------------------\n"
                print "Proceeding to ", self.stage.name, "\n"

            winner_name = self.end_of_round()
            if winner_name is name1:
                counter1 += 1
            elif winner_name is name2:
                counter2 += 1
	    else:
                counterD += 1

        winner = None
        self.small_blind.end_game()
        self.dealer.end_game()
        if self.dealer.chips == 0:
            winner = self.small_blind
        else:
            winner = self.dealer
        print "-----> Winner : " + winner.name + " jackpot : " + str(winner.chips)
        return (name1, counter1, name2, counter2, counterD, winner.name)

    # Collects bets and sends previous bets to current player
    def collect_bets(self):
        if (self.small_blind.chips == 0 or self.dealer.chips == 0) and (
        not self.stage is Stage.preflop):  # Have to end the game
            return False

        small_blind_raise = 0
        dealer_raise = 0
        action1 = self.small_blind.play(can_check=not self.stage is Stage.preflop, pot=self.pot)  # small blind plays
        self.dealer.opponent_action(action1)

        if action1 is action.fold:  # Small blind folded, end of round
            print self.small_blind.name + " folds\n"
            self.small_blind.folded = True

            small_blind_bet = self.small_blind.collect_bet()
            dealer_bet = self.dealer.collect_bet()
	    self.pot += small_blind_bet + dealer_bet
            return False

        # We don't care if small blind calls or checks at this point, and if he raises, he adds it to his current bet
        elif action1 is action.call:  # Makes the small blind cover the next half of blind
            if self.stage is Stage.preflop:
                print "Completed small blind \n"
                self.small_blind.place_bet(self.blind / 2.0)
            else:
                print self.small_blind.name + " checks\n"

        elif action1 is action.bet:
            if self.stage is Stage.preflop:
                self.small_blind.place_bet(self.blind / 2.0)

            print self.small_blind.name + " raises\n"
            small_blind_raise = self.small_blind.place_bet(self.bet_value, self.dealer.chips)
        else:
            print "Error : " + str(action1)


        action2 = self.dealer.play(can_check=action1 is action.call, pot=self.pot)  # then dealer plays, he can raise if small blind didnt raise ! correction : can raise anyway
        self.small_blind.opponent_action(action2)
        
        if action2 is action.fold:  # dealer folded
            print self.dealer.name + " folds\n"
            self.dealer.folded = True

            small_blind_bet = self.small_blind.collect_bet()
            dealer_bet = self.dealer.collect_bet()
            self.pot += small_blind_bet + dealer_bet
            return False

        elif action2 is action.call:
            if action1 is action.call:
                print self.dealer.name + " checks\n"
            else:
                print self.dealer.name + " calls\n"
                self.dealer.place_bet(small_blind_raise)

        # Here the dealer can re-raise, and thus we need the to pass the information to the small blind
        elif action2 == action.bet:
            if action1 is action.call:
                print self.dealer.name + " raises\n"
                dealer_raise = self.dealer.place_bet(self.bet_value, self.small_blind.chips)
            else:
                print self.dealer.name + " calls and raises again\n"
                self.dealer.place_bet(small_blind_raise)  # Call
                dealer_raise = self.dealer.place_bet(self.bet_value, self.small_blind.chips)  # raise

            action3 = self.small_blind.play(can_check=False,
                                            can_raise=False, pot=self.pot)  # if dealer raised, small blind either calls or fold
	    self.dealer.opponent_action(action3)
            if action3 == action.fold:
                print self.small_blind.name + " folds\n"
                self.small_blind.folded = True
                small_blind_bet = self.small_blind.collect_bet()
                dealer_bet = self.dealer.collect_bet()
                self.pot += small_blind_bet + dealer_bet
                return False
            else:
                print self.small_blind.name + " calls\n"
                self.small_blind.place_bet(dealer_raise)
        else:
            print "Error : " + str(action2)

        small_blind_bet = self.small_blind.collect_bet()
        dealer_bet = self.dealer.collect_bet()

        self.pot += small_blind_bet + dealer_bet

        if self.small_blind.chips == 0 or self.dealer.chips == 0:
            return False

        return True  # indicates that no one folded

    # Plays one round until the end or until one player folds
    def play_round(self):

        print "pot is ", self.pot, "\n"

        if not self.collect_bets():
            return True  # one of the player has folded

        if self.stage is Stage.river:  # River has been played, time to decide who won the game
            self.stage = Stage.showdown
            return True  # end of the turn

        elif self.stage is Stage.preflop:  # Current Stage is Preflop so we open 3 cards
            self.community_cards += self.deck.get(3)

            self.deck.burn()
            self.stage = Stage.flop

        elif self.stage is Stage.flop or self.stage is Stage.turn:  # Opens 1 card if the current stage is the flop or turn
            self.community_cards += self.deck.get()

            self.deck.burn()
            self.stage = Stage.turn if self.stage is Stage.flop else Stage.river

        # Tells players about new community cards
        self.small_blind.update_cards(self.community_cards)
        self.dealer.update_cards(self.community_cards)
        return False  # turn is not over

    def end_of_round(self):
        winner_name = ""
        if self.small_blind.folded:
            print self.dealer.name, " won ", self.pot, " chips \n"
            self.dealer.win_money(self.pot)
            winner_name = self.dealer.name

        elif self.dealer.folded:
            print self.small_blind.name + " won ", self.pot, " chips \n"
            self.small_blind.win_money(self.pot)
            winner_name = self.small_blind.name

        else:
            if self.stage is not Stage.showdown:
                missing = 5 - len(self.community_cards)
                for i in range(0, missing):
                    self.community_cards += self.deck.get()

            small_blind_hand = comparator.get_hand(self.small_blind.show_cards() + self.community_cards)  # Hand of small blind
            dealer_hand = comparator.get_hand(self.dealer.show_cards() + self.community_cards)  # Hand of big blind
            winner = comparator.compare_hands(small_blind_hand, dealer_hand)
            if winner == small_blind_hand:
                self.small_blind.win_money(self.pot)  # small_blind wins
                print self.small_blind.name + " won ", self.pot, " chips with ", winner[0].name, winner[1], '\n'
                winner_name = self.small_blind.name

            elif winner == dealer_hand:
                self.dealer.win_money(self.pot)
                print self.dealer.name + " won ", self.pot, " chips with ", winner[0].name, winner[1], '\n'
                winner_name = self.dealer.name
            else:
                self.small_blind.win_money(self.pot / 2.0)
                self.dealer.win_money(self.pot / 2.0)
                print "Pot split, same hand\n"

        print "End of round : "
        print self.small_blind.name + " had : " + self.small_blind.card_string(self.small_blind.cards)
        print self.dealer.name + " had : " + self.dealer.card_string(self.dealer.cards)
        print "Table was : " + self.small_blind.card_string(self.community_cards)

        self.small_blind.end_round()
        self.dealer.end_round()
        self.pot = 0
        self.stage = Stage.preflop
        swap = self.dealer
        self.dealer = self.small_blind
        self.small_blind = swap
        self.community_cards = []
        return winner_name
