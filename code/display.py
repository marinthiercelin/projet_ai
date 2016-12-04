class display():
	def __init__(self,game,player1,player2):
		self.game = game
		self.player1 = player1
		self.player2 = player2
	
	def print_table(self):
		print "Table : "
		table = ""
		for card in self.game.table:
			table += "| " + card[0] + " of " + card[1] + " |"
		print table
		
	def print_bets(self):
		print "Bets : "
		print "Player 1 : " + self.player1.bets + " Player 2 : " + self.player2.bets
		
	def print_game(self):
		print "###############################"
		self.print_player(self.player1)
		print "------------"
		self.print_player(self.player1)
		print "------------"
		self.print_table()
		print "------------"
		self.print_bets()
		
		
	def print_player(self,player):
		print "Player " + str(player.number)
		if is_dealer(player): print "Dealer"
		print "Chips : " + str(player.chips)
		cards = ""
		print "Hand : "
		for card in player.hand:
			cards += "| " + card[0] + " of " + card[1] + " |"
		print cards
	
