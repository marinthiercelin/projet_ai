from Game import Game
from player import player
from random_agent import random_agent
from Agent_Bucket import Agent_Bucket
player1 = Agent_Bucket("Bot", 100)
player2 = player("YOU", 100)

game = Game(player1, player2, 5, 10 )

game.start_game()
