from Game import Game
from player import player
from random_agent import random_agent
from Regret_Agent import Regret_Agent
from Agent_Bucket import Agent_Bucket
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
		string = "Retour " + stat[0] + " " + str(stat[1]) + " "+ stat[2] + " " +  str(stat[3]) + " draw " + str(stat[4]) + " winner " + stat[5] + "\n"
		f.write(string)
	f.close()

chips = 100
bet_value = 10
blind_value = 5
number_of_games = 100
file_name = "test1.txt"
player1 = random_agent("Random",chips)
player2 = Agent_Bucket("Bucket",chips)	
compare_agents(player1,player2,number_of_games,chips,blind_value,bet_value,file_name)
		
	
	
