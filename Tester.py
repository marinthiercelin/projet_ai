from Game import Game
from player import player
from random_agent import random_agent
from Agent_Bucket import Agent_Bucket
player1 = Agent_Bucket("noob", 10)
player2 = player("pro", 10)

game = Game(player1, player2, 1, 3)

game.start_game()
