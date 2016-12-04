from Game import Game
from player import player
from random_agent import random_agent
from Agent_Bucket import Agent_Bucket
from All_In_Agent import All_In_Agent
from LearningAgent import LearningAgent
from Regret_Agent import Regret_Agent


player1 = Regret_Agent("Bot", 500, 10)
player2 = Agent_Bucket("You", 500)

game = Game(player1, player2, 5, 10 )

game.start_game()
