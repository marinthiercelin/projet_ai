import Bucketing
import sys, os
from Game import Game
from player import player
from LearningAgent import LearningAgent
from All_In_Agent import All_In_Agent
from random_agent import random_agent
from Agent_Bucket import Agent_Bucket

apprentice = 0
bucket = 0

#sys.stdout = open(os.devnull, "w")

#for i in range(0,10):

player1 = LearningAgent("Apprentice Bot", 1000)
player2 = Agent_Bucket("Bucket", 1000)

game = Game(player1, player2, 10, 20)
if game.start_game()[5] == player1.name:
    apprentice += 1
else:
    bucket += 1

#sys.stdout = sys.__stdout__

print "Apprentice won ", apprentice, " games and Bucket Agent won ", bucket, " Games out of 10"

'''print player1.preflop_values
print player1.flop_values
print player1.turn_values
print player1.river_values'''