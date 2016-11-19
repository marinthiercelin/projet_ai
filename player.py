from enum import Enum
from copy import copy
import HandComparator

class action(Enum):
	call = 1
	bet = 2
	fold = 3

comparator = HandComparator.HandComparator()
#player class
class player(object):

	def __init__(self, number, chips):
		self.chips = chips
		self.number = number
		self.cards = []
		self.current_bet = 0 #Represents the bet for the current stage, bets are only collected before proceding to next stage
		self.folded = False
		self.community_cards = []

	#Reinitializes the hand to play next round
	def new_hand(self, cards):
		self.folded = False
		self.current_bet = 0
		self.cards = cards
		self.community_cards = []

	#Updates the community cards when changed
	def update_cards(self, community_cards):
		self.community_cards = community_cards

	#Instructs the player to put the required amount on his bet
	#Called to collect a blind or a bet
	def place_bet(self, amount):
		val = max(0, self.chips-amount)
		self.chips = val
		self.current_bet += amount

	#Returns the current bet to the game and resets it to 0, usually when proceding to next stage
	def collect_bet(self):
		tmp = copy(self.current_bet)
		self.current_bet = 0
		return tmp

	def win_money(self, amount):
		self.chips += amount

	def show_cards(self):
		return self.cards

	
	#def oponent_action(self, action):
			
	def play(self, bet_value, can_raise=True):
		print "Your cards are ", self.cards
		print "Community cards are ", self.community_cards
		print "You currently have a ", comparator.get_hand(self.cards + self.community_cards)

		if can_raise:
			string = "What do you do ? : 1 = bet, 2 = fold, 3 = call/check \n"
		else:
			string = "Opponent raised. What do you do ? : 2 = fold, 3 = call\n"
		move = raw_input(string)

		if move == "1":
			self.place_bet(bet_value)
			return action.bet
		elif move == "2" :
			self.folded = True
			return action.fold
		elif move == "3":
			if not can_raise: #If opponent raised, it's a call
				self.place_bet(bet_value)
			return action.call
		else:
			return self.play(bet_value)
