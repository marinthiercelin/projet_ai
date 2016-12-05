import sys
sys.path.insert(0, '../Game')
sys.path.insert(0, '../Regret_Agent')
sys.path.insert(0, '../Learning_Agent')
sys.path.insert(0, '../Bayesian_Agent')
from Deck import ordered_list
from HandComparator import HandComparator
import math


comp = HandComparator()

# Computes the bucket, for each hand
class Bucketing(object):

	# Computes the expected value of a hand by comparing it to all the possible enemy hands and computing its win probability
	def proba(self, cards, table_cards):
		compteur = 0
		diviseur = 0

		dealt = cards + table_cards
		remaining = list(ordered_list)
		for card in dealt:
			remaining.remove(card)

		hand = comp.get_hand(cards + table_cards)
		for i in xrange(len(remaining)):
			card1 = ordered_list[i]
			for card2 in remaining[i+1:] :
				diviseur += 1
				l = [card1, card2]
				h1 = comp.get_hand(l + table_cards)
				if hand == comp.compare_hands(h1, hand):
					compteur += 1
						
		proba = compteur / (diviseur*1.0)
		return proba
	
	# Splits the probabilities computed by the above function in the 5 different buckets (0 - 0.2 : 0; 0.2 - 0.4 : 1 ... 0.8 - 1 : 4) 
	def bucketing(self, cards, table_cards, number=5):
		return int(math.floor(number*self.proba(cards,table_cards)))
		
		
