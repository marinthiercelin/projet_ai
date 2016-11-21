import itertools
import random
import json

values = range(1, 14)
suits = ["Spades", "Diamonds", "Hearts", "Clubs"]
ordered_list = list(itertools.product(values, suits))

#a deck of card
class Deck(object):

    def __init__(self):
        self.deck = []
        self.restart()

    def restart(self):
        self.deck = list(ordered_list)
        random.shuffle(self.deck)

    def get(self, number=1):
        result = []
        for n in xrange(number):
            result.append(self.deck.pop())
        return result

    def burn(self, number=1):
        for n in xrange(number):
            self.deck.pop()

class FakeDeck(Deck):
	def __init__(self):
		self.list_of_decks = []
		self.index_of_deck = -1 # current_deck
		Deck.__init__(self)
		
	def restart(self):
		self.index_of_deck += 1
		if self.index_of_deck >= len(self.list_of_decks):
			new = list(ordered_list)
			random.shuffle(new)
			self.list_of_decks.append(new)
		self.deck = self.list_of_decks[self.index_of_deck]
	
	def restart_fake(self):
		self.index_of_deck = -1
		self.restart()
		
	def store(self,name):
		f = open(name,"w")
		json.dump(self.list_of_decks,f)
		f.close()
		
	def load(self,name):
		f = open(name)
		self.list_of_decks = json.load(f)
		f.close()
		new = []
		for deck in self.list_of_decks:
			new_d = []
			for card in deck:
				new_d.append((card[0],str(card[1])))
			new.append(new_d)
		self.list_of_decks = list(new)
		
		
		

