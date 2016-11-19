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
		self.money_on_table = 0
		self.folded = False
	
	def collect_money(amount):
		val =  max(0,self.chips-amount)
		self.chips = val
		self.money_on_table += val
	
	def win_money(amount):
		self.chips += amount
		
	def new_hand(self, cards):
		self.folded = False
		self.money_on_table = 0
		self.hand = cards
	
	def oponent_action(action):
			
	def play(self,can_call = True):
		if can_call :
			string = "What do you do ? : 1 = bet, 2 = fold, 3 = call/check \n"
		else:
			string = "What do you do ? : 1 = bet, 2 = fold\n"
		move = raw_input(string)
		if move == "1":
			return action.bet
		elif move == "2" :
			self.folded = True
			return action.fold
		elif move == "3":
			return action.call
		else:
			return self.play()
