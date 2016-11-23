from player import player,action

class Regret_Agent(player):	
	def __init__(self, name, chips):
		player.__init__(self, name, chips)
	
	def play(self, can_check = False, can_raise = True):
		return action.call
