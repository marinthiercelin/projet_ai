import sys
sys.path.insert(0, '../Game')
sys.path.insert(0, '../Naive_Agents')
sys.path.insert(0, '../Regret_Agent')
sys.path.insert(0, '../Learning_Agent')
from player import player,action
from Agent_Bucket import Agent_Bucket
from numpy import random

#an Agent that use bayesian inferrence to guess the opponent's strategy
#and then use it to play a counter-strategy
class bayesian(Agent_Bucket):
	
	def __init__(self,name,chips,model = None):
		Agent_Bucket.__init__(self,name,chips)
		self.opp = None
		self.list_opp_action = []
		self.dist = []
		self.learning_model = True
		if model is None:
			self.model = []
			self.learning_model = True
		else :
			self.model = model
			self.learning_model = False
		for i in xrange(5):
			teta = [[5,5], [5,5]]
			self.dist.append(list(teta))
			
	
	def get_opponent(self,opponent):
		self.opp = opponent
        
	#if in learning mode the agent updates its model
	def end_round(self):
		if self.learning_model:
			opp_cards = self.opp.cards
			self.update_teta_dist(self.bucket(opp_cards),self.list_opp_action)
		self.list_opp_action = []

	#get the current bucket
	def bucket(self,cards):
		v = self.classifier.bucketing(cards, self.community_cards)
		return v if v < 5 else 4
        
	def get_opp_cards(self,bucket):
		self.opp_bucket = bucket
		
	def opponent_action(self,action):
		if not action is None:
			self.list_opp_action.append(action)
			
			
	#based on the actions and the bucket of the opponent, we update the distribution
	def update_teta_dist(self,bucket,action_history):
		number_of_raise = 0
		number_of_call = 0
		number_of_fold = 0
		for act in action_history:
			if act is action.bet:
				number_of_raise += 1
			elif act is action.call:
				number_of_call += 1
			elif act is action.fold:
				number_of_fold += 1
			else:
				None
		
		self.dist[bucket][0][0] += number_of_raise
		self.dist[bucket][0][1] += number_of_call + number_of_fold
		self.dist[bucket][1][0] += number_of_call
		self.dist[bucket][1][1] += number_of_fold
		
	#based on the distribution, we compute the MAP estimates for each parameter	
	def teta_estimate(self):
		dist = []
		for bucket_dist in self.dist:
			a = bucket_dist[0][0]
			b = bucket_dist[0][1]
			teta1 = ((a -1)*1.0/(a + b-2))
			a = bucket_dist[1][0]
			b = bucket_dist[1][1]
			teta2 = ((a -1)*1.0/(a + b-2))
			dist.append([(1-teta1)*(1-teta2),(1-teta1)*teta2,teta1])
		return dist
	
	#get in or out of the learning mode	
	def learning(self,start_stop):
		if start_stop is False :
			self.model = list(self.teta_estimate())
		self.learning_model = start_stop
		
	#return the action chosen	
	def play(self,can_check = False,can_raise = True, pot=None):
		if self.learning_model:
			return Agent_Bucket.play(self,can_check,can_raise,pot)
		else:
			#implement a counter-strategy : we try to guess the cards of the opponent based on its actions
			#and then take decision with that information.
			my_bucket = self.classifier.bucketing(self.cards, self.community_cards)
			guess = self.bucket_estimation(self.list_opp_action)
			his_bucket = guess[0]
			evidence = guess[1]
			return self.choose_action(my_bucket, his_bucket, evidence, can_check, can_raise)
	
	#counter strategy : take decision based on all the information we have		
	def choose_action(self, my_bucket, his_bucket, evidence, can_check, can_raise):
		proba = [1,1,1]
		if evidence < 1.5:
			if my_bucket is 0:
				proba = [0.5,0.45,0.05]
			elif my_bucket is 1:
				proba = [0.4,0.5,0.1]
			elif my_bucket is 2:
				proba = [0.1,0.6,0.3]
			elif my_bucket is 3:
				proba = [0.05,0.5,0.45]
			elif my_bucket >= 4:
				proba = [0,0.4,0.6]
				
		elif evidence >= 1.5:
			diff = my_bucket - his_bucket
			if my_bucket <= -4:
				proba = [0.6,0.4,0]
			elif my_bucket is -3:
				proba = [0.45,0.5,0.05]
			elif my_bucket is -2:
				proba = [0.35,0.55,0.1]
			elif my_bucket is -1:
				proba = [0.25,0.6,0.15]
			elif my_bucket is 0:
				proba = [0.15,0.65,0.2]
			elif my_bucket is 1:
				proba = [0.1,0.7,0.2]
			elif my_bucket is 2:
				proba = [0.1,0.6,0.3]
			elif my_bucket is 3:
				proba = [0.05,0.6,0.35]
			elif my_bucket >= 4:
				proba = [0.02,0.5,0.48]
				
		if not can_raise:
			proba[1] += proba[2]
			proba[2] = 0
		if can_check:
			proba[1] += proba[0]
			proba[0] = 0
			
		s = sum(proba)
		if s != 0 :
			proba = [a / (s*1.0) for a in proba]
		act = random.choice([action.fold,action.call,action.bet],p=proba)
		if act is None:
			raise ImportError
		return act
					
	#makes a guess of the cards of the opponent based on the learned model and the list of actions
	def bucket_estimation(self,list_action):
		proba = [1,1,1,1,1]
		for bucket in xrange(5):
			for act in list_action:
				if act is action.call:
					proba_act = self.model[bucket][1]
					proba[bucket] *= proba_act
				elif act is action.bet:
					proba_act = self.model[bucket][2]
					proba[bucket] *= proba_act
				else:
					None
		max_prob = max(proba)
		idx = proba.index(max_prob)
		del proba[idx]
		second = max(proba)
		ev = max_prob/second if second != 0 else 10000
		return (idx, ev) 
