import Bucketing
import sys, os
from Game import Game
from player import player
from LearningAgent import LearningAgent, Teacher
from All_In_Agent import All_In_Agent
from random_agent import random_agent
from Agent_Bucket import Agent_Bucket
from New_Agent import Utility_Agent

sys.stdout = open(os.devnull, "w")

apprentice = 0
opponent = 0

for i in range(0,10):


    student = LearningAgent("Student", 100)
    teacher = Agent_Bucket("Bucket", 100)

    game = Game(teacher, student, 5, 10)

    res = game.start_game()

    sys.stdout = sys.__stdout__
    print res
    sys.stdout = open(os.devnull, "w")
    #weight = player1.prev_action_weight


    if res[5] == teacher.name: #teacher won
        opponent += 1
    else:
        apprentice += 1



sys.stdout = sys.__stdout__
#print weight, player1.prev_action_weight
print teacher.name," won ", opponent, " games and ", student.name ," won ", apprentice, " Games out of 10"


print student.preflop_values
print student.flop_values
print student.turn_values
print student.river_values
