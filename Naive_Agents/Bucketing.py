import sys
sys.path.insert(0, '../Game')
sys.path.insert(0, '../Regret_Agent')
sys.path.insert(0, '../Learning_Agent')
sys.path.insert(0, '../Bayesian_Agent')
from Deck import ordered_list
from HandComparator import HandComparator
import math


comp = HandComparator()

class Bucketing(object):

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
	
	def bucketing(self, cards, table_cards, number=5):
		return int(math.floor(number*self.proba(cards,table_cards)))
		
		
