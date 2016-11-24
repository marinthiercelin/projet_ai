import Bucketing
from Game import Game
from player import player
from LearningAgent import LearningAgent
from All_In_Agent import All_In_Agent
from random_agent import random_agent
from Agent_Bucket import Agent_Bucket
player1 = LearningAgent("Apprentice Bot", 1000)
player2 = random_agent("Random Bot", 1000)

game = Game(player1, player2, 10,20)


print game.start_game()

print player1.preflop_values
print player1.flop_values
print player1.turn_values
print player1.river_values