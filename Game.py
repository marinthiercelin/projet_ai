# game class
import Deck
from enum import Enum


class Stage(Enum):
	preflop = 1
	flop = 2
	turn = 3
	river = 4
	showdown = 5


class Game(object):
	# Init takes an array of players and the number of players set to 1
	# Blinds are the first chips to play the game
	def __init__(self, players, blinds, num_players=2):
		self.num_players = num_players
		self.players = players
		self.pot = 0
		self.opened_cards = []
		self.deck = Deck.Deck()
		self.blinds = blinds
		self.stage = Stage.preflop

	def collect_blinds(self):
		for i in xrange(self.num_players):
			self.pot += 0  # self.players[i].collect_blind() #Needs to be implemented

	def deal(self):
		self.deck.restart()

		for i in xrange(self.num_players):
			self.players[i].take_cards(self.deck.get(2))
			self.deck.burn()

	def play_round(self):
		for i in xrange(self.num_players):
			self.pot += self.players[i].decide # To be implemented (Maybe store each action and send to other players)

		if self.stage is Stage.river: #River has been played, time to decide who won the game
			self.stage = Stage.showdown

		elif self.stage is Stage.preflop: #Current Stage is Preflop so we open 3 cards
			self.opened_cards += self.deck.get(3)
			self.deck.burn()
			self.stage = Stage.flop

		elif self.stage is Stage.flop or self.stage is Stage.turn: #Opens 1 card if the current stage is the flop or turn
			self.opened_cards += self.deck.get()
			self.deck.burn()
			self.stage = Stage.turn if self.stage is Stage.flop else Stage.river

	def decide_winner(self):
		hands = []
		for i in xrange(self.num_players):
			hands.append(self.players[i].get_hand())

		winner = hand_comparator.best_hand(hands)
