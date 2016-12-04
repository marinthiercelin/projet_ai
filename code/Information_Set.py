from Game import Game 
import json

class Information_Set(object): 
	def __init__(self, bv = 10): 
		self.player_bucket = 0
		self.history = []
		self.regrets = [0, 0, 0]
		self.probs = [1/3.0, 1/3.0, 1/3.0]
		self.expected_values = [0, 0, 0]
		self.betvalue = bv
		
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
					
	def update_expected_values(self, nextC, nextR): 
		currpot = self.pot_from_history()
		winpr = self.player_bucket/5.0 + 0.2
		self.expected_values[0] = -1 * currpot
		if nextC == None: 
			currpot += self.betvalue
			self.expected_values[1] = 2*winpr*currpot - currpot # p*a - (1-p)*a = 2*p*a - a 
		else : 
			self.expected_values[1] = nextC.expected_value()
		if nextR == None: 
			currpot += self.betvalue
			self.expected_values[2] = 2*winpr*currpot - currpot
		else: 
			self.expected_values[2] = nextR.expected_value()
		
	def pot_from_history(self): 
		pot = 0 
		step = self.betvalue
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


		
		
