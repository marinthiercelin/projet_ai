from player import player,action
from Agent_Bucket import Agent_Bucket
#try to infer the strategy
class bayesian(Agent_Bucket):
	def __init__(self,name,chips,opponent):
		Agent_Bucket.__init__(self,name,chips)
		self.opp = opponent
		self.opp_actions = []
		self.dist = 5*[2*[5,5]]
		self.number_of_call = 0
		self.number_of_raise = 0
		self.evolution_of_teta = []
		self.opp_bucket = 0
		
	def new_hand(self):
		player.new_hand(self)
		
		
	def end_of_round(self):
		opp_cards = self.opp.cards
		self.update_teta_dist(self.bucket(cards),self.list_opp_action)
		self.list_opp_action = []
		
	def bucket(self,cards):#technique of bucketing opponent_cards from 0 to 4
		return 0
		
	def get_opp_cards(self,bucket):
		self.opp_bucket = bucket
		
	def opp_action(self,action):
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
			a = self.bucket_dist[0][0]
			b = self.bucket_dist[0][1]
			teta1 = ((a -1)*1.0/(a + b-2))
			a = self.bucket_dist[1][0]
			b = self.bucket_dist[1][1]
			teta2 = ((a -1)*1.0/(a + b-2))
			dist.append([(1-teta1)*(1-teta2),(1-teta1)*teta2,teta1])
		return dist
		
		
