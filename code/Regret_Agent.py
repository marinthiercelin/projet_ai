from player import player,action
from Information_Tree import Information_Tree
from Game import Game
from Bucketing import Bucketing

dealtreefile = "deal.json"
sbtreefile = "sb.json"

class Regret_Agent(player):	
	def __init__(self, name, chips, bv):
		player.__init__(self, name, chips)
		self.dealer_tree = Information_Tree(dealtreefile, bv)
		self.sb_tree = Information_Tree(sbtreefile, bv)
		self.bet_hist = []
		self.dealer = False
				
	def play(self, can_check = False, can_raise = True, pot = None):
		bucket = Bucketing().bucketing(self.cards, self.community_cards)
		if self.dealer : 
			return self.dealer_tree.get_action(can_check, can_raise, bucket, self.bet_hist)
		else: 
			return self.sb_tree.get_action(can_check, can_raise, bucket, self.bet_hist)
		
	def end_game(self): 
		self.dealer_tree.save_tree()
		self.sb_tree.save_tree()
		
	def new_hand(self): 
		self.bet_hist = []
		self.dealer = not self.dealer
		player.new_hand(self)	
		
	def betting_history(self, bh):
		self.bet_hist = bh 
		
	
		
