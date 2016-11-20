from player import player,action
from random import randrange

class random_agent(player):
	def play(player,can_raise = True):
		move = randrange(3) if can_raise else randrange(2)
		if move == 0:
			return action.call
		elif move == 1 :
			return action.fold
		else :
			return action.bet
			


	
