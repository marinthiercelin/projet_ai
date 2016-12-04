from Game import Game 

class Information_Set(object): 
	def __init__(self): 
		self.player_bucket = 0
		self.history = []
		self.regrets = [0, 0, 0]
		self.probs = [1/3.0, 1/3.0, 1/3.0]
		self.expected_values = [0, 0, 0]
		
	def update_regrets(self, oprob): 
		average_expval = self.expected_value()
		for i in xrange(3): 
			self.regrets[i] += oprob*(self.expected_values[i] - average_expval)
		
	def update_probs(self): 
		totalreg = 0
		for i in xrange(3): 
			if self.regrets[i] > 0:
				totalreg += self.regrets[i]
		if totalreg > 0: 	
			for i in xrange(3): 
				if self.regrets[i] > 0: 
					self.probs[i] = self.regrets[i]/totalreg
				else : 
					self.probs[i] = 0
					
	def update_expected_values(self): 
			self.expected_values[0] = -1 * self.pot_from_history()
			
	def pot_from_history(self): 
		pot = 0 
		step = Game.bet_value
		for char in self.history:
			if char == "R": 
				pot += 2*step
			elif char == "C": 
				pot += step
		return pot
		
	def expected_value(self): 
		somme = 0
		for i in xrange(3): 
			somme += self.probs[i]*self.expected_values[i]
		return somme
			
info = Information_Set()
info.history = ["R", "R", "C"]
print info.pot_from_history()
		
		
