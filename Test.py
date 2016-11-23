import Bucketing
from Game import Game
from player import player
from LearningAgent import LearningAgent
from All_In_Agent import All_In_Agent
from random_agent import random_agent

player1 = LearningAgent("Bot", 1000)
player2 = random_agent("AllIn", 1000)

game = Game(player1, player2, 5,10)

print game.start_game()

print player1.preflop_values
print player1.flop_values
print player1.turn_values
print player1.river_values