import sys
sys.path.insert(0, '../Game')
sys.path.insert(0, '../Regret_Agent')
sys.path.insert(0, '../Learning_Agent')
sys.path.insert(0, '../Bayesian_Agent')
from numpy import random
from player import player,action
from Bucketing import Bucketing

# A naive agent, that maps from card observation to actions
class Agent_Bucket(player):
	def __init__(self, name, chips):
		player.__init__(self, name, chips)
		self.classifier = Bucketing()
	
	def play(self,can_check = False,can_raise = True, pot=None):
		bucket = self.classifier.bucketing(self.cards, self.community_cards)
		proba = [0,0,0]
		if bucket == 0:
			proba = [1,1,0]
		elif bucket == 1:
			proba = [4,7,1]  if can_raise else [5,7,0]
		elif bucket == 2:
			proba = [1,8,3]  if can_raise else [1,11,0]
		elif bucket == 3:
			proba = [1,25,24]  if can_raise else [1,49,0]
		elif bucket == 4:
			proba = [0,2,3]  if can_raise else [0,1,0] 
		else : 
			proba = [0,0,1] if can_raise else [0,1,0]
			
		if can_check : 
			proba[1] += proba[0]
			proba[0] = 0
				
		s = sum(proba)
		if s != 0 :
			proba = [a / (s*1.0) for a in proba]
		act = random.choice([action.fold,action.call,action.bet],1,p=proba)
		return act[0]
