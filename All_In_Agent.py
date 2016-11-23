from player import player,action

class All_In_Agent(player):	
	def __init__(self, name, chips):
		player.__init__(self, name, chips)
	
	def play(self, can_check = False, can_raise = True):
		if can_raise: 
			return action.bet
		else :
			return action.call