import Bucketing
import sys, os
from Game import Game
from player import player
from LearningAgent import LearningAgent
from All_In_Agent import All_In_Agent
from random_agent import random_agent
from Agent_Bucket import Agent_Bucket
from New_Agent import Utility_Agent
apprentice = 0
bucket = 0
weight = 0
#sys.stdout = open(os.devnull, "w")


for i in range(0,1):

    player1 = Agent_Bucket("bucket", 1000)
    player2 = Utility_Agent("utility", 1000,weight)

    game = Game(player1, player2, 10, 20)
    res = game.start_game()
    #weight = player1.prev_action_weight
    print res
    if res[5] == player1.name:
        apprentice += 1
    else:
        bucket += 1


sys.stdout = sys.__stdout__
#print weight, player1.prev_action_weight
print player1.name," won ", apprentice, " games and ",player2.name," won ", bucket, " Games out of 10"

'''print player1.preflop_values
print player1.flop_values
print player1.turn_values
print player1.river_values'''