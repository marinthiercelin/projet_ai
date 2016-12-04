from Information_Set import Information_Set
import json


class Information_Tree(object): 
	def __init__(self, filepath): 
		self.info_sets = dict()		
		self.load_tree(filepath)
		if len(self.info_sets) == 0:
			self.first_tree()
		
	def get_action(self, can_check, can_raise, bucket, bethistory): 
		proba = self.get_probs(bucket, bethistory, can_check, can_raise)
		
		act = random.choice([action.fold,action.call,action.bet],1,p=proba)
		return act[0]

	def get_probs(self, bucket, bethistory, can_check, can_raise):
		prob = self.info_sets.get(self.hashed(bucket, bethistory), [0, 1, 0])
		if can_check : 
			prob[0] = 0
		if not can_raise: 
			prob[2] = 0
		
		return self.normalize(prob)
		
	def first_tree(self):
		histories = self.generate_strings() 
		self.treenit(histories)
	
	def update_tree(self, n): 
		for i in xrange(n): 
			self.stepupdate()
			
	def stepupdate(self): 
		for iset in self.info_sets.values():
			iset.update_expected_values()
			n = len(iset.history)
			oppart = (iset.history[:n-1], iset.history[n-1:])
			if oppart[1] == "R": 
				oprob = self.info_sets.get(self.hashed(iset.bucket, oppart[0]), [1/3.0, 1/3.0, 1/3.0])[2]
			else : 
				oprob = self.info_sets.get(self.hashed(iset.bucket, oppart[0]), [1/3.0, 1/3.0, 1/3.0])[1]
			iset.update_regrets(opbrob)
			iset.update_probs()
	
	def normalize(self, prob): 
		s = sum(prob)
		if s != 0 :
			prob = [a / (s*1.0) for a in prob]
		else: 
			prob = [0, 1, 0]
		return prob
	
	def treenit(self, hist): 
		for buck in xrange(5): 			
			for elem in hist: 
				infset = Information_Set()
				infset.player_bucket = buck
				infset.history = elem
				self.info_sets[self.hashed(buck, str(elem))] = infset
				
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
	
	def listtostring(self, l): 
		word = ""
		for elem in l: 
			word = word + str(elem)
		return word
				
	def normalform(self, tonorm): 
		for i in xrange(len(tonorm)): 
			tonorm[i] = self.formalize(tonorm[i])
		return self.filtered(tonorm) 
		
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
		
	def filtered(self, tofilt): 
		newl = []
		for i in tofilt: 
			if i not in newl :
				newl.append(i)
		return newl		
	
	
	
	def hashed(buck, beth):
		if beth = None: 
			return str(buck)
		return str(buck) + str(beth)
	
	def load_tree(self, file1):
		file d = open(file1)
		self.info_sets = json.load(d)
		d.close()
	
	def save_tree(self, file1): 
		file d = open(file1, 'w')
		json.dump(self.info_sets, d)
		d.close() 
