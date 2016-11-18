import itertools
import random


values = ["Ace", "2", "3", "4", '5'," 6","7","8","9","10","Jack","Queen","King"]
suits = ["Spades", "Diamonds", "Hearts", "Clubs"]


#a deck of card
class Deck(object):

    def __init__(self):
        self.ordered_list = list(itertools.product(values, suits))
        self.deck = []
        self.restart()

    def restart(self):
        self.deck = list(self.ordered_list)
        random.shuffle(self.deck)

    def get(self, number=1):
        result = []
        for n in xrange(number):
            result.append(self.deck.pop())
        return result

    def burn(self, number=1):
        for n in xrange(number):
            self.deck.pop()


