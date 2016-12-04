import sys
sys.path.insert(0, '../Game')
sys.path.insert(0, '../Naive_Agents')
sys.path.insert(0, '../Regret_Agent')
sys.path.insert(0, '../Learning_Agent')
from bayesian import bayesian
from bayesian_trainer import bayesian_trainer
from Game import Game
from player import player,action
from random_agent import random_agent
from Agent_Bucket import Agent_Bucket
from All_In_Agent import All_In_Agent
from LearningAgent import LearningAgent


player2 = bayesian_trainer("sparring_partner", 100)
player1 = bayesian("Bot_to_train", 100,player2)


for x in xrange(10):
	player1.new_game(100)
	player2.new_game(100)
	game = Game(player1, player2, 5, 10 )
	game.start_game()
	
player4 = All_In_Agent("sparring_partner", 100)
player3 = bayesian("Bot_to_train", 100,player4)


for x in xrange(10):
	player3.new_game(100)
	player4.new_game(100)
	game = Game(player3, player4, 5, 10 )
	game.start_game()
	
player1.learning(False)
player3.learning(False)
	
bucket1 = player1.bucket_estimation([action.bet,action.bet,action.bet])
bucket2 = player3.bucket_estimation([action.bet,action.bet,action.bet])

print "guess 1 : " + str(bucket1)
print "guess 2 : " + str(bucket2)
	
player1.learning(False)
dist = player1.teta_estimate()
for i in xrange(len(dist)):
	print "Bucket ", i, dist[i] 
	
