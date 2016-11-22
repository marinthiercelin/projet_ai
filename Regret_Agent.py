from player import player,action

class Regret_Agent(player):	
	def __init__(self, name, chips):
		player.__init__(self, name, chips)
	
	def play(self, check_or_call, can_raise = True):
		return action.call
