from numpy import random
from player import player,action
from Bucketing import Bucketing

class Agent_Bucket(player):
	def __init__(self,name,chips):
		player.__init__(self,name,chips)
		self.classifier = Bucketing()
	
	def play(self,can_raise = True):
		bucket = self.classifier.bucketing(self.cards, self.community_cards)
		print bucket
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
				
		s = sum(proba)
		if s != 0 :
			proba = [a / (s*1.0) for a in proba]
		print proba , sum(proba)
			
		act = random.choice([action.fold,action.call,action.bet],1,p=proba)
		print "agent acts : " + str(act)
		return act[0]
