from player import player,action
from Agent_Bucket import Agent_Bucket
#try to infer the strategy
class bayesian(Agent_Bucket):
	def __init__(self,name,chips,opponent):
		Agent_Bucket.__init__(self,name,chips)
		self.opp = opponent
		self.list_opp_action = []
		self.dist = []
		self.learning_model = True
		self.model = []
		for i in xrange(5):
			teta = [[5,5], [5,5]]
			self.dist.append(list(teta))
	
		
	def new_hand(self):
		player.new_hand(self)
        
	def end_round(self):
		if self.learning_model:
			opp_cards = self.opp.cards
			self.update_teta_dist(self.bucket(opp_cards),self.list_opp_action)
		self.list_opp_action = []

	def bucket(self,cards):#technique of bucketing opponent_cards from 0 to 4
		v = self.classifier.bucketing(cards, self.community_cards)
		return v if v < 5 else 4
        
	def get_opp_cards(self,bucket):
		self.opp_bucket = bucket
		
	def opponent_action(self,action):
		self.list_opp_action.append(action)
	
	def update_teta_dist(self,bucket,action_history):
		number_of_raise = 0
		number_of_call = 0
		number_of_fold = 0
		for act in action_history:
			if act is action.bet:
				number_of_raise += 1
			elif act is action.call:
				number_of_call += 1
			else:
				number_of_fold += 1
		
		self.dist[bucket][0][0] += number_of_raise
		self.dist[bucket][0][1] += number_of_call + number_of_fold
		self.dist[bucket][1][0] += number_of_call
		self.dist[bucket][1][1] += number_of_fold
		
		
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
		
	def learning(self,start_stop):
		if start_stop is False :
			self.model = list(self.teta_estimate())
		self.learning_model = start_stop
		
	def play(self,can_check = False,can_raise = True, pot=None):
		if self.learning_model:
			return Agent_Bucket.play(self,can_check,can_raise,pot)
		else:
			#implement a counter_strategy
			my_bucket = self.classifier.bucketing(self.cards, self.community_cards)
			guess = self.bucket_estimation(self.list_opp_action)
			his_bucket = guess[0]
			evidence = guess[1]
			print "\n Based on " + str(self.list_opp_action) + " we guess : " + str(bucket) +"\n"
			self.choose_action(my_bucket, his_bucket, evidence, can_check, can_raise)
				
	def choose_action(self, my_bucket, his_bucket, evidence, can_check, can_raise):
		proba = [1,1,1]
		if evidence < 1.5:
			print " not enough info "
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
		act = random.choice([action.fold,action.call,action.bet],1,p=proba)
		return act
					
	def bucket_estimation(self,list_action):
		proba = [1,1,1,1,1]
		for bucket in xrange(5):
			for action in list_action:
				if action is action.call:
					proba_act = self.model[bucket][1]
					proba[bucket] *= proba_act
				elif action is action.bet:
					proba_act = self.model[bucket][2]
					proba[bucket] *= proba_act
				else:
					print "error estimation bucket"
					return 0 # fold ? not supposed to happen
		max_prob = max(proba)
		idx = proba.index(max_prob)
		del proba[idx]
		second = max(proba)
		ev = max_prob/second if second != 0 else 10000
		print "proba of all : " + str(proba)
		return (idx, ev) 
