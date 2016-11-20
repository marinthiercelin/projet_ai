# game class
from Deck import Deck
from enum import Enum
import HandComparator
from random import randrange
from player import player,action


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
	def __init__(self, player1, player2, blind, bet_value):
		self.bet_value = bet_value
		self.dealer = player1  #Second to play
		self.small_blind = player2  #First to play
		self.community_cards = []
		self.deck = Deck()
		self.blind = blind
		self.pot = 0 #Sum of all bets for the game
		self.stage = Stage.preflop

	#Instructs players to put blind bets in their current bet
	def collect_blinds(self):
		self.small_blind.place_bet(self.blind/2.0)
		self.dealer.place_bet(self.blind)
		#self.pot += (3/2.0) * self.blind #Add sum to the pot

	#Shuffles the deck and gives two cards to each player
	def deal(self):
		self.deck.restart()
		self.small_blind.collect_cards(self.deck.get(2))
		self.dealer.collect_cards(self.deck.get(2))
	
	def start_game(self):
		while self.dealer.chips != 0 and self.small_blind.chips != 0: #Play until no player has money
			self.small_blind.new_hand()
			self.dealer.new_hand()
			print "Collecting blinds \n"
			self.collect_blinds()
			self.deal()

			while not self.play_round():
				print "\n Proceeding to ", self.stage.name , "\n"

			self.end_of_round()#to implement
		

	#Collects bets and sends previous bets to current player
	def collect_bets(self):
		action1 = self.small_blind.play(self.bet_value)# small blind plays

		if action1 == action.fold: #Small blind folded, end of round
			return False
		#We don't care if small blind calls or checks at this point, and if he raises, he adds it to his current bet
		if self.stage is Stage.preflop and action1 is action.call: #Makes the small blind cover the next half of blind
			print "\n Completed small blind \n"
			self.small_blind.place_bet(self.blind/2.0)
		#self.small_blind.collect_money(abs(self.small_blind.on_table - self.dealer.on_table))#call
		#elif action1 == action.bet:#then raise
			#self.small_blind.collect_money(self.bet_value)
		
		action2 = self.dealer.play(self.bet_value, action1 != action.bet)#then dealer plays, he can raise if small blind didnt raise
		if action2 == action.fold: #Player 2 folded
			return False

		#Here the dealer can re-raise, and thus we need the to pass the information to the small blind
		#elif action2 == action.call: #Player 2 checked or called the raise
		#self.dealer.collect_money(abs(self.small_blind.on_table - self.dealer.on_table))#call
		if action2 == action.bet:
			#self.dealer.collect_money(self.bet_value)

			action1 = self.small_blind.play(self.bet_value, False)#if dealer raised, small blind either calls or fold
			if action1 == action.fold:
				return False
			#If small blind didn't fold, then he called

			#self.small_blind.collect_money(abs(self.small_blind.on_table - self.dealer.on_table))#call
		small_blind_bet = self.small_blind.collect_bet()
		dealer_bet = self.dealer.collect_bet()

		self.pot += small_blind_bet + dealer_bet

		return True # indicates that no one folded

	#Plays one round until the end or until one player folds
	def play_round(self):

		print "\n pot is ", self.pot, "\n"

		if not self.collect_bets():
			return True  #one of the player has folded

		if self.stage is Stage.river: #River has been played, time to decide who won the game
			self.stage = Stage.showdown
			return True  #end of the turn

		elif self.stage is Stage.preflop: #Current Stage is Preflop so we open 3 cards
			self.community_cards += self.deck.get(3)

			self.deck.burn()
			self.stage = Stage.flop

		elif self.stage is Stage.flop or self.stage is Stage.turn: #Opens 1 card if the current stage is the flop or turn
			self.community_cards += self.deck.get()

			self.deck.burn()
			self.stage = Stage.turn if self.stage is Stage.flop else Stage.river

		#Tells players about new community cards
		self.small_blind.update_cards(self.community_cards)
		self.dealer.update_cards(self.community_cards)
		return False  # turn is not over

	def end_of_round(self):
		if self.small_blind.folded:
			print "Dealer won"
			self.dealer.win_money(self.pot)

		elif self.dealer.folded:
			print "Small blind won"
			self.small_blind.win_money(self.pot)

		else:
			small_blind_hand = comparator.get_hand(self.small_blind.show_cards() + self.community_cards) #Hand of small blind
			dealer_hand = comparator.get_hand(self.dealer.show_cards() + self.community_cards) #Hand of big blind

			winner = comparator.compare_hands(small_blind_hand, dealer_hand)
			if winner == small_blind_hand:
				self.small_blind.win_money(self.pot)  # dealer wins
				print "\n Small blind won ", self.pot, " chips with ", winner[0].name

			elif winner == dealer_hand:
				self.dealer.win_money(self.pot)
				print "\n Dealer won ", self.pot, " chips with ", winner[0].name
			else:
				self.small_blind.win_money(self.pot/2.0)
				self.dealer.win_money(self.pot/2.0)
				print "\n Pot split, same hand"

		self.pot = 0
		self.stage = Stage.preflop
		swap = self.dealer
		self.dealer = self.small_blind
		self.small_blind = swap
		self.community_cards = []

