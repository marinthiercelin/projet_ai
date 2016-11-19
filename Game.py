# game class
from Deck import Deck
from enum import Enum
from random import randrange
from player import player,action


class Stage(Enum):
	preflop = 1
	flop = 2
	turn = 3
	river = 4
	showdown = 5


class Game(object):
	# Init takes an array of players and the number of players set to 1
	# Blinds are the first chips to play the game
	def __init__(self, player1, player2, blind, bet_value):
		self.bet_value = bet_value
		self.dealer = player1
		self.small_blind = player2 
		self.opened_cards = []
		self.deck = Deck()
		self.blinds = blinds
		self.stage = Stage.preflop

	def collect_blinds(self):
		self.small_blind.collect_money(blind/2)
		self.dealer.collect_money(blind)

	def deal(self):
		self.deck.restart()
		self.small_blind.get_hand(deck.get(2))
		self.dealer.get_hand(deck.get(2))
	
	def start_game(self):
		while self.dealer.chips != 0 and self.small_blind.chips != 0:
			self.stage = Stage.preflop
			self.collect_blinds()
			self.deal()
			while not self.play_round()
			self.end_of_round()#to implement
			swap = self.dealer
			self.dealer = self.small_blind
			self.small_blind = swap
		

	#Collects bets and sends previous bets to current player
	def collect_bets(self):
		action1 = self.small_blind.play()#first small blind plays
		if action1 = action.fold:
			return False
		self.small_blind.collect_money(abs(self.small_blind.on_table - self.dealer.on_table))#call
		if action1 == action.bet:#then raise
			self.small_blind.collect_money(self.bet_value)
		
		action2 = self.dealer.play(action1 != action.bet)#then dealer plays, he can raise if small blind didnt raise
		if action2 = action.fold:
			return False
		self.d.collect_money(abs(self.small_blind.on_table - self.dealer.on_table))#call
		if action2 == action.bet:
			self.dealer.collect_money(self.bet_value)
			action1 = self.small_blind.play(False)#if dealer raised, small blind either calls or fold
			if action1 = action.fold:
				return False
			self.small_blind.collect_money(abs(self.small_blind.on_table - self.dealer.on_table))#call
		return True # indicates that no one folded
			
			

	def play_round(self):

		if not self.collect_bets() : return True #one of the player has folded

		if self.stage is Stage.river: #River has been played, time to decide who won the game
			self.stage = Stage.showdown
			return True #end of the turn

		elif self.stage is Stage.preflop: #Current Stage is Preflop so we open 3 cards
			self.opened_cards += self.deck.get(3)
			self.deck.burn()
			self.stage = Stage.flop

		elif self.stage is Stage.flop or self.stage is Stage.turn: #Opens 1 card if the current stage is the flop or turn
			self.opened_cards += self.deck.get()
			self.deck.burn()
			self.stage = Stage.turn if self.stage is Stage.flop else Stage.river
		return False # turn is not over


	def decide_winner(self):
		hands = []
		for i in xrange(self.num_players):
			hands.append(self.players[i].get_hand())

		winner = hand_comparator.best_hand(hands)
