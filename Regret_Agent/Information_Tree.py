# Information Tree class, that the agent built and iterated over to get the optimal actions
import sys
sys.path.insert(0, '../Game')
sys.path.insert(0, '../Naive_Agents')
sys.path.insert(0, '../Learning_Agent')
sys.path.insert(0, '../Bayesian_Agent')
sys.path.insert(0, '../Regret_Agent')
from Information_Set import Information_Set
from numpy import random
from player import player, action
import json


class Information_Tree(object): 
	# Keeps a map of the bucket + history key associated with the different information sets as values, along with the bet value 
	def __init__(self, filepath, bv, learn = False): 
		self.info_sets = dict()		
		self.betvalue = bv
		self.filepath = filepath
		self.load_tree(filepath)
		
		# If there was no precomputed tree generate a new one and save it in json format
		if len(self.info_sets) == 0:
			self.first_tree()
			self.save_tree()
		
		# If we want to keep on towards the convergence of the algorithm, update the tree and save it.
		elif learn: 
			self.update_tree(1000)
			self.save_tree()
	
	# Returns the action suggested by the strategy stocked in this tree
	def get_action(self, can_check, can_raise, bucket, bethistory): 
		proba = self.get_probs(bucket, bethistory, can_check, can_raise)
		act = random.choice([action.fold,action.call,action.bet],1,p=proba)
		return act[0]

	# Returns the probabilities associated with each action, and prevents the agent from folding when it can check and from raising when it is not allowed to.
	def get_probs(self, bucket, bethistory, can_check, can_raise):
		iset = self.info_sets.get(self.hashed(bucket, self.listtostring(bethistory)), None)
		if iset == None : 
			prob = [0, 1, 0]
		else : 
			prob = iset.probs
		if can_check or bucket >= 3 : 
			prob[0] = 0
		if not can_raise: 
			prob[2] = 0
		
		return self.normalize(prob)
	
	# Method used to generaate the tree at first
	def first_tree(self):
		histories = self.generate_strings() 
		self.treenit(histories, self.betvalue)
		self.update_tree(1000)
	
	# Repeats n times the algorithm used by this technique
	def update_tree(self, n): 
		for i in xrange(n): 
			self.stepupdate()
			
	# Performs one whole step of the algorithm
	def stepupdate(self): 
		for iset in self.info_sets.values():
			histC = iset.history + "C"
			histR = iset.history + "R"
			nextC = self.info_sets.get(self.hashed(iset.player_bucket, histC), None) 
			nextR = self.info_sets.get(self.hashed(iset.player_bucket, histR), None) 		
			iset.update_expected_values(nextC, nextR)
			n = len(iset.history)
			oppart = (iset.history[:n-1], iset.history[n-1:])
			if oppart[1] == "R": 
				oprob = self.info_sets.get(self.hashed(iset.player_bucket, oppart[0]), [1/3.0, 1/3.0, 1/3.0]).probs[2]
			else : 
				oprob = self.info_sets.get(self.hashed(iset.player_bucket, oppart[0]), [1/3.0, 1/3.0, 1/3.0]).probs[1]
			iset.update_regrets(oprob)
			iset.update_probs()
	
	# Normalizes the probabilities to make sure the random selecter doesn't complain
	def normalize(self, prob): 
		s = sum(prob)
		if s != 0 :
			prob = [a / (s*1.0) for a in prob]
		else: 
			prob = [0, 1, 0]
		return prob
	
	# Initializes the tree by creating all the necessary information sets
	def treenit(self, hist, bv): 
		for buck in xrange(5): 			
			for elem in hist: 
				infset = Information_Set(bv)
				infset.player_bucket = buck
				infset.history = elem
				self.info_sets[self.hashed(buck, str(elem))] = infset
	
	# Generates all the possible Check and Raise combination 			
	def generate_strings(self) :
		hlist = []
		hlist.append('')
		templist = ['']
		for i in xrange(11): 
			newlist = []
			for elem in templist:
				newlist.append(str(elem) + "C")
				newlist.append(str(elem) + "R") 
			newlist = self.normalform(newlist)
			hlist = hlist + newlist 
			templist = newlist
		return hlist
	
	# Given a list of chars, returns a string
	def listtostring(self, l): 
		word = ""
		for elem in l: 
			word = word + str(elem)
		return word
				
	# Removes the unwanted betting sequences
	def normalform(self, tonorm): 
		for i in xrange(len(tonorm)): 
			tonorm[i] = self.formalize(tonorm[i])
		return self.filtered(tonorm) 
	
	# Removes the unwanted betting sequences (for instance RRR is not possible, as only two raises per stage are allowed)	
	def formalize(self, elem):
		tomod = list(elem)	
		if len(elem)%3 == 0:			
			maxind = len(elem)/3
			for i in xrange(maxind): 
				a = tomod[3*i]
				b = tomod[3*i + 1]
				if a == "C" and b == "C" : 
					tomod[3*i + 2] = "Z"
				elif a == "C" and b == "R": 
					tomod[3*i + 2] = "C"
				elif a == "R" and b == "C": 
					tomod[3*i + 2] = "Z"
				elif a == "R" and b == "R": 
					tomod[3*i + 2] = "C"
		return self.listtostring(tomod)
		
	# Removes the duplicates in the list 	
	def filtered(self, tofilt): 
		newl = []
		for i in tofilt: 
			if i not in newl :
				newl.append(i)
		return newl		
	
	# Concatenates the bucket number and the betting history to form the keys of the dictionnary
	def hashed(self, buck, beth):
		if beth == None: 
			return str(buck)
		return str(buck) + str(beth)
	
	# Loads a precomputed tree from a json file whose path is specified as argument 
	def load_tree(self, file1):
		d = open(file1)
		self.jsontodict(json.load(d))
		d.close()
	
	# Saves the current tree in a json file whose path is specified as argument
	def save_tree(self): 
		d = open(self.filepath, 'w')
		stored_dict = self.dicttojson()
		json.dump(stored_dict, d)
		d.close() 
	
	# Helper function to go from a dictionnary (containing Information_Set values) to a json-compatible form
	def dicttojson(self): 
		stored_dict = {}
		for elem in self.info_sets.items():
			templist = []
			bucklist = [0]
			bucklist[0] = elem[1].player_bucket
			templist.append(bucklist)
			templist.append(list(elem[1].history))
			templist.append(elem[1].regrets) 
			templist.append(elem[1].probs)
			templist.append(elem[1].expected_values)
			stored_dict[elem[0]] = templist
		return stored_dict
	
	# Helper function to recover the dictionnary from the json-compatible form
	def jsontodict(self, jsonlist): 
		for elem in jsonlist.items(): 
			iset = Information_Set()
			iset.player_bucket = elem[1][0]
			iset.history = elem[1][1]
			iset.regrets = elem[1][2]
			iset.probs = elem[1][3]
			iset.expected_values = elem[1][4]
			self.info_sets[elem[0]] = iset
			

