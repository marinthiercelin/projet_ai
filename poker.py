import sys
sys.path.insert(0, './Game')
sys.path.insert(0, './Naive_Agents')
sys.path.insert(0, './Regret_Agent')
sys.path.insert(0, './Learning_Agent')
sys.path.insert(0, './Bayesian_Agent')
from Game import Game
from bayesian import bayesian
from player import player
from All_In_Agent import All_In_Agent
from Agent_Bucket import Agent_Bucket
from random_agent import random_agent
from LearningAgent import LearningAgent
from Regret_Agent import Regret_Agent

# Main program. Allows you to compete with one of the 6 agents, or to watch two of them compete. More detailed instructions can be found in the README file.

def ask_player_mode(number,chips,bet_value,model):	
	print "Player"+ str(number) +" Mode : "
	print " 1 : Manual player (You play)"
	print " 2 : Random Agent"
	print " 3 : All-In Agent"
	print " 4 : Bucket_Agent"
	print " 5 : Bayesian Agent ( with pre-computed model )"
	print " 6 : Learning Agent "
	print " 7 : Regret-Minimization Agent"
	x = raw_input(" What mode ? [1-7] : ")
	gamer = None
	if x == "1":
		gamer = player("player" + str(number),chips)
	elif x == "2":
		gamer = random_agent("player" + str(number),chips)
	elif x == "3":
		gamer = All_In_Agent("player" + str(number),chips)
	elif x == "4":
		gamer = Agent_Bucket("player" + str(number),chips)
	elif x == "5":
		gamer = bayesian("player" + str(number),chips, list(model))
	elif x == "6":
		gamer = LearningAgent("player" + str(number),chips,2)
	elif x == "7":
		gamer = Regret_Agent("player" + str(number),chips,bet_value)
	else:
		return False
	return gamer

# Precomputed model used by Bayesian agent	
model = [[0.0839300839300839, 0.8476938476938477, 0.06837606837606838], [0.06048166392993976, 0.7490421455938697, 0.19047619047619047], [0.03334283271587343, 0.6390709603875748, 0.3275862068965517], [0.019170204025742845, 0.5032178556757496, 0.47761194029850745], [0.01857323765301814, 0.40861122836639935, 0.5728155339805825]]

# Game constants :
chips = 100 # Amount of starting chips (default 100)
bet_value = 10 # Value of a single bet  (default 10) 
blind_value = 5 # Value of the blind, should be half the bet_value (default 5) 
number_of_game = 1 # Number of games to be played (default 1) 

player1 = False
while not player1:
	player1 = ask_player_mode(1,chips,bet_value,model)
player2 = False
while not player2:
	player2 = ask_player_mode(2,chips,bet_value,model)
player1.get_opponent(player2)
player2.get_opponent(player1)

for i in xrange(number_of_game):
	player1.new_game(chips)
	player2.new_game(chips)
	game = Game(player1,player2,blind_value,bet_value)
	game.start_game()
