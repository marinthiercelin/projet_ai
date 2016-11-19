from player import player,action
from random import randrange

class random_agent(player):
	def play(player):
		move = randrange(3)
		if move == 0:
			return action.call
		elif move == 1 :
			return action.bet
		else :
			return action.fold
			


	
