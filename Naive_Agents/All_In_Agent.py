import sys
sys.path.insert(0, '../Game')
sys.path.insert(0, '../Regret_Agent')
sys.path.insert(0, '../Learning_Agent')
sys.path.insert(0, '../Bayesian_Agent')
from player import player,action

# An agent that always bet when possible, calls otherwise. You can't play more aggressively. It is not as weak as it might appear to be and is a good benchmark agent. 
class All_In_Agent(player):	
	def __init__(self, name, chips):
		player.__init__(self, name, chips)
	
	def play(self, can_check = False, can_raise = True, pot = None):
		if can_raise: 
			return action.bet
		else :
			return action.call
