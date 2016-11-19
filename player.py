from enum import Enum

class action(Enum):
	call = 1
	bet = 2
	fold = 3
	
#player class
class player(object):
	def __init__(self,number,chips):
		self.chips = chips
		self.number = number
		self.cards = []
		
	def new_hand(self, cards):
		self.hand = cards
		
	def play(self):
		move = raw_input("What do you do ? : 1 = call/check, 2 = bet, 3 = fold \n")
		if move == "1":
			return action.call
		elif move == "2" :
			return action.bet
		elif move == "3":
			return action.fold
		else:
			return self.play()
