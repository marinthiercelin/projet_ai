from Game import Game
from player import player
player1 = player("noob", 10)
player2 = player("pro", 10)

game = Game(player1, player2, 1, 3)

game.start_game()
