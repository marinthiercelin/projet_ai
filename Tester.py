from Game import Game
from player import player
from random_agent import random_agent
from Agent_Bucket import Agent_Bucket
from All_In_Agent import All_In_Agent


player1 = Agent_Bucket("Bot", 1000)
player2 = All_In_Agent("AllIn", 1000)

game = Game(player1, player2, 5, 10 )

game.start_game()
