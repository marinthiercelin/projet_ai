import Bucketing
import sys, os
from Game import Game
from player import player
from LearningAgent import LearningAgent, Teacher
from All_In_Agent import All_In_Agent
from random_agent import random_agent
from Agent_Bucket import Agent_Bucket
from New_Agent import Utility_Agent

training_episodes = 2000
games_to_play = 10


sys.stdout = open(os.devnull, "w") #No prints

for i in range(0, training_episodes + 1): #1000 learning episodes

    if i % 20 == 0:
        sys.stdout = sys.__stdout__
        print i
        sys.stdout = open(os.devnull, "w")

    if i % 50 == 0: #Every 50 episodes, play 10 games against bucket agent to track progress
        apprentice = 0
        hands_played = 0
        hands_won = 0
        draws = 0
        bad_folds = 0
        for j in range(10):
            player = LearningAgent("Student1", 100,2)
            opponent = LearningAgent("Student2", 100,1)
            game = Game(player, opponent, 5, 10)
            results = game.start_game()

            hands_played += results[1] + results[3] + results[4]
            draws += results[4]
            bad_folds += player.bad_folds

            if results[5] == player.name:
                apprentice += 1 #Games won

            if results[0] == player.name: #Hands won
                hands_won += results[1]
            else:
                hands_won += results[3]

        sys.stdout = sys.__stdout__
        print player.preflop_values
        print player.flop_values
        print player.turn_values
        print player.river_values
        print "After ", i, " learning epsiodes : \n Num Games won :", apprentice, \
            "\n Num hands won :", hands_won, "\n Num hands played :", hands_played, \
            "\n Draws :", draws, "\n Bad folds : ", bad_folds
        sys.stdout = open(os.devnull, "w")

    if i != training_episodes:
        student = LearningAgent("Student1", 100,2)
        teacher = LearningAgent("Student2", 100,1)
        game = Game(teacher, student, 5, 10)
        game.start_game()


sys.stdout = sys.__stdout__


