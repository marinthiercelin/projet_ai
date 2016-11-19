from Game import Game
from player import player
player1 = player(1, 10)
player2 = player(2, 10)

game = Game(player1, player2, 1, 3)

game.start_game()