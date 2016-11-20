from Game import Game
from player import player
from random_agent import random_agent
player1 = random_agent("noob", 10)
player2 = player("pro", 10)

game = Game(player1, player2, 1, 3)

game.start_game()
