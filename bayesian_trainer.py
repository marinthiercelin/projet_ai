from player import player, action
from numpy import random
from Agent_Bucket import Agent_Bucket

class bayesian_trainer(Agent_Bucket):
	def __init__(self,name,chips):
		Agent_Bucket.__init__(self,name,chips)
	
	def play(self,can_check = False,can_raise = True, pot=None):
		bucket = self.classifier.bucketing(self.cards, self.community_cards)
		proba = [0,0,0]
		if bucket == 0:
			proba = [0.4,0.4,0.2]  if can_raise else [0.5,0.5,0]
		elif bucket == 1:
			proba = [0.25,0.5,0.25]  if can_raise else [0.35,0.65,0]
		elif bucket == 2:
			proba = [0.1,0.5,0.4]  if can_raise else [0.1,0.9,0]
		elif bucket == 3:
			proba = [0.02,0.4,0.58]  if can_raise else [0.05,0.95,0]
		elif bucket == 4:
			proba = [0,0.2,0.8]  if can_raise else [0,1,0] 
		else : 
			print "Cards with proba of winning 1 ? " + str(self.cards)
			proba = [0,0,1] if can_raise else [0,1,0]
			
		if can_check : 
			proba[1] += proba[0]
			proba[0] = 0
				
		s = sum(proba)
		if s != 0 :
			proba = [a / (s*1.0) for a in proba]
		#print sum(proba)
		#print bucket
		act = random.choice([action.fold,action.call,action.bet],1,p=proba)
		return act[0]
			
