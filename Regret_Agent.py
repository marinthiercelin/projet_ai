from player import player,action
from Information_Tree import Information_Tree
from Game import Game

dealtreefile = "deal.json"
sbtreefile = "sb.json"

class Regret_Agent(player):	
	def __init__(self, name, chips):
		player.__init__(self, name, chips)
		self.dealer_tree = Information_Tree.__init__(dealtreefile)
		self.sb_tree = Information_Tree.__init__(sbtreefile)
		
		
	def play(self, can_check = False, can_raise = True):
		bucket = Bucketing.bucketing(self.cards, game.community_cards)
		if self.name == game.dealer.name : 
			return dealer_tree.get_action(can_check, can_raise, bucket, Game.bethistory)
		else: 
			return sb_tree.get_action(can_check, can_raise, bucket, Game.bethistory)
		
	def end_game(self): 
		self.dealer_tree.save_tree()
		self.sb_tree.save_tree()
