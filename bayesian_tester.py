from bayesian import bayesian
from bayesian_trainer import bayesian_trainer
from Game import Game
from player import player
from random_agent import random_agent
from Agent_Bucket import Agent_Bucket
from All_In_Agent import All_In_Agent
from LearningAgent import LearningAgent
from New_Agent import Utility_Agent


player2 = All_In_Agent("sparring_partner", 100)
player1 = bayesian("Bot_to_train", 100,player2)

for x in xrange(10):
	player1.new_game(100)
	player2.new_game(100)
	game = Game(player1, player2, 5, 10 )
	game.start_game()
	
dist = player1.teta_estimate()
for i in xrange(len(dist)):
	print "Bucket ", i, dist[i] 
