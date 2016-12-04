import sys
sys.path.insert(0, '../Game')
sys.path.insert(0, '../Regret_Agent')
sys.path.insert(0, '../Learning_Agent')
sys.path.insert(0, '../Bayesian_Agent')
from player import player,action
from random import randrange

from numpy import random
class random_agent(player):
	def __init__(self,name,chips):
		player.__init__(self,name,chips)
	
	def play(player,can_check = False,can_raise = True, pot = None):
		move = random.choice(3, p=[0.7,0.1,0.2])
		if move == 0:
			return action.call
		elif move == 1:
			return action.fold
		else :
			return action.bet
			


	
