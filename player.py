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

	def __init__(self, name, chips):
		self.chips = chips
		self.name = name
		self.cards = []
		self.current_bet = 0 #Represents the bet for the current stage, bets are only collected before proceding to next stage
		self.folded = False
		self.community_cards = []
		
	def new_game(self,chips):
		self.chips = chips
		self.cards = []
		self.current_bet = 0 #Represents the bet for the current stage, bets are only collected before proceding to next stage
		self.folded = False
		self.community_cards = []
		

	#Reinitializes the hand to play next round
	def new_hand(self):
		self.folded = False
		self.current_bet = 0
		self.cards = []
		self.community_cards = []

	#Collects the cards
	def collect_cards(self, cards):
		self.cards = cards

	#Updates the community cards when changed
	def update_cards(self, community_cards):
		self.community_cards = community_cards

	#Instructs the player to put the required amount on his bet
	#Called to collect a blind or a bet
	def place_bet(self, amount, opponent_chips=100000000):
		val = min(amount, opponent_chips, self.chips)
		self.current_bet += val
		self.chips -= val
		return val

	#Returns the current bet to the game and resets it to 0, usually when proceding to next stage
	def collect_bet(self):
		tmp = copy(self.current_bet)
		self.current_bet = 0
		return tmp

	def win_money(self, amount):
		self.chips += amount

	def show_cards(self):
		return self.cards

	def end_game(self):
		return None

	def end_round(self):
		return None

	def opponent_action(self, act):
		return None

	def opponent_cards(self, cards):
		return None

	def play(self, can_check = False,can_raise=True, pot=None):
		print "Player : " + self.name
		print "Your statement is " , self.chips
		print "Your cards are " + self.card_string(self.cards)
		print "Community cards are " + self.card_string(self.community_cards)
		print "You currently have a ", comparator.get_hand(self.cards + self.community_cards)[0].name 
		
		check_or_call = "check" if can_check else "call"

		if can_raise:
			string = "What do you do ? : 1 = bet, 2 = fold, 3 = "+check_or_call+"\n"
		else:
			string = "Opponent raised. What do you do ? : 2 = fold, 3 = "+check_or_call+"\n"
		move = raw_input(string)

		if move == "1" and can_raise:
			return action.bet
		elif move == "2" :
			return action.fold
		elif move == "3":
			return action.call
		else:
			return self.play(can_raise)
		
		print #retour a la ligne du bled
			
	def card_string(self,cards):
		string = ""
		for card in cards :
			string += "\n| "
			if card[0] is 1:
				string += "Ace"
			elif card[0] is 11:
				string += "Jack"
			elif card[0] is 12:
				string += "Queen"
			elif card[0] is 13:
				string += "King"
			else :
				string += str(card[0])
			string += " of " + card[1] + " |"
		return "No cards" if string == "" else string
