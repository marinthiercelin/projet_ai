from Game import Game
from player import player
from random_agent import random_agent
from Agent_Bucket import Agent_Bucket
from All_In_Agent import All_In_Agent
from LearningAgent import LearningAgent


player1 = LearningAgent("Bot", 100)
player2 = player("You", 100)

game = Game(player1, player2, 5, 10 )

game.start_game()
