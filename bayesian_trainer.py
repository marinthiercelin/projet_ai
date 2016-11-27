from player import player, action
from numpy import random

class bayesian_trainer(player):
	def __init__(self,name,chips,opponent):
		player.__init__(self,name,chips)
		self.opponent = opponent
	
	def play(self, can_check = False,can_raise=True):
		bucket = self.bucket()
		pr = []
		if bucket is 1:
			pr =[0.3,0.7]
		else:
			pr = [0.6,0.4]
			
		act = random.choice([action.call,action.bet],1,p=pr)
		self.opponent.add_action(act[0])
		return act if can_raise else action.call
		
	def collect_cards(self, cards):
		self.cards = cards
		self.opponent.get_opponnents_cards(self.bucket())
		
	def bucket(self):
		for c in self.cards:
			if c[0] > 9 :
				return 1
		return 0
			
