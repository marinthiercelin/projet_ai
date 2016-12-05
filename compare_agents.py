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
from Deck import Deck,FakeDeck

def compare_agents(agent1,agent2,number_of_games,chips,blind,bet,file_name):
	f = open(file_name, "a")
	for i in xrange(number_of_games):
		agent1.new_game(chips)
		agent2.new_game(chips)
		deck = FakeDeck()
		game = Game(agent1,agent2,blind,bet,deck)
		stat = game.start_game()
		string = "Aller " + stat[0] + " " + str(stat[1]) + " "+ stat[2] + " " +  str(stat[3]) + " draw " + str(stat[4]) + " winner " + stat[5]+"\n"
		f.write(string)
		agent1.new_game(chips)
		agent2.new_game(chips)
		deck.restart_fake()
		game = Game(agent2,agent1,blind,bet,deck)
		stat = game.start_game()
		string = "Retour " + stat[0] + " " + str(stat[1]) + " "+ stat[2] + " " +  str(stat[3]) + " draw " + str(stat[4]) + " winner " + stat[5] + "\n-----------------\n"
		f.write(string)
	f.close()

def competition(agent1,agent2,number_of_games,chips,blind,bet):
	name1 = agent1.name
	name2 = agent2.name
	win1 = 0
	win2 = 0
	draw = 0
	for i in xrange(number_of_games):
		agent1.new_game(chips)
		agent2.new_game(chips)
		deck = FakeDeck()
		game = Game(agent1,agent2,blind,bet,deck)
		stat1 = game.start_game()
		agent1.new_game(chips)
		agent2.new_game(chips)
		deck.restart_fake()
		game = Game(agent2,agent1,blind,bet,deck)
		stat2 = game.start_game()
		if stat1[5] != stat2[5]:
			draw += 1
		elif stat1[5] == name1:
			win1 += 1
		elif  stat1[5] == name2:
			win2 += 1
		else:
			print "Errorrrrrrrr " 
			break;
	print name1 + " : " + str(win1) + ", " + name2 + " : " + str(win2) + ", Draw : " + str(draw)
		
chips = 100
bet_value = 10
blind_value = 5
learning = False
learning_round = 5
number_of_games = 20
player1 = Regret_Agent("regret",chips,bet_value)
player2 = LearningAgent("learning",chips,2)

if learning :
	for x in xrange(learning_round):
		player1.new_game(chips)
		player2.new_game(chips)
		game = Game(player1, player2, blind_value, bet_value)
		game.start_game()
	player2.learning(False)

competition(player1,player2,number_of_games,chips,blind_value,bet_value)
		
	
	
