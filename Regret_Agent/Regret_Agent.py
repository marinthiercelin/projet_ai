# Counterfactual Regret Minimization Agent
import sys
sys.path.insert(0, '../Game')
sys.path.insert(0, '../Naive_Agents')
sys.path.insert(0, '../Learning_Agent')
sys.path.insert(0, '../Bayesian_Agent')
from player import player,action
from Information_Tree import Information_Tree
from Game import Game
from Bucketing import Bucketing

# Path to the json files containing the precomputed trees
dealtreefile = "./Regret_Agent/deal.json"
sbtreefile = "./Regret_Agent/sb.json"

class Regret_Agent(player):	
	# Apart from the usual player attributes, this agent also need two half trees for its strategy, the betting history and needs to know whether it is the dealer or not.
	def __init__(self, name, chips, bv):
		player.__init__(self, name, chips)
		self.dealer_tree = Information_Tree(dealtreefile, bv)
		self.sb_tree = Information_Tree(sbtreefile, bv)
		self.bet_hist = []
		self.dealer = False
				
	# Asks the appropriate half strategy what to do in the given bucket with such a betting history
	def play(self, can_check = False, can_raise = True, pot = None):
		bucket = Bucketing().bucketing(self.cards, self.community_cards)
		if self.dealer : 
			return self.dealer_tree.get_action(can_check, can_raise, bucket, self.bet_hist)
		else: 
			return self.sb_tree.get_action(can_check, can_raise, bucket, self.bet_hist)
		
	# Resets the betting history at the end of each hand and change the dealer
	def new_hand(self): 
		self.bet_hist = []
		self.dealer = not self.dealer
		player.new_hand(self)	
		
	# Getter method to access the betting history from Game
	def betting_history(self, bh):
		self.bet_hist = bh 
		
	
		
