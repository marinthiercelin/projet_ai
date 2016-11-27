from player import player, action
from Bucketing import Bucketing
from Game import Stage
import json
import math
from Agent_Bucket import Agent_Bucket
import numpy

Ne = 2
optimistic_reward = 10
preflop_filename = "preflop.json"
flop_filename = "flop.json"
turn_filename = "turn.json"
river_filename = "river.json"
class LearningAgent(Agent_Bucket):

    #Plays only small blind for now
    def __init__(self, name, starting_chips):
        Agent_Bucket.__init__(self, name, starting_chips)
        try:
            with open(preflop_filename) as d:
                self.preflop_values = json.load(d)
                d.close()
            with open(flop_filename) as d:
                self.flop_values = json.load(d)
                d.close()
            with open(turn_filename) as d:
                self.turn_values = json.load(d)
                d.close()
            with open(river_filename) as d:
                self.river_values = json.load(d)
                d.close()
        except IOError:
            self.preflop_values = dict()
            self.initialize_map(self.preflop_values, Stage.preflop)
            self.flop_values = dict()
            self.initialize_map(self.flop_values, Stage.flop)
            self.turn_values = dict()
            self.initialize_map(self.turn_values, Stage.turn)
            self.river_values = dict()
            self.initialize_map(self.river_values, Stage.turn)

        self.bucket_history = []
        self.action_history = []

    def initialize_map(self, map, stage):
        if stage is Stage.preflop: #Here we have 2 more buckets
            start = -2
        else:
            start = 0
        for i in xrange(start, 6):
            map[str(i)] = [(0, 0)] * 3 #Because we have 3 actions

    #Introduces two new buckets for preflop stage (-1 for same suit and diff < 3 and -2 for same_suit or diff > 3
    def learning_bucket(self, cards, community_cards, stage):
        bucket = Bucketing().bucketing(cards, community_cards)
        if stage is Stage.preflop: #Preflop bucketing
            diff = abs(cards[0][0] - cards[1][0]) #Difference between the two cards
            if diff == 12: #Adjusts for case of having
                diff = 1
            same_suit = cards[0][1] == cards[1][1]
            if diff < 3 and same_suit and diff != 0:
                bucket = -1
            elif (diff != 0 and diff < 3) or same_suit:
                bucket = -2
        return str(bucket)

    def get_stage(self):
        if len(self.community_cards) == 0:
            return Stage.preflop
        elif len(self.community_cards) == 3:
            return Stage.flop
        elif len(self.community_cards) == 4:
            return Stage.turn
        elif len(self.community_cards) == 5:
            return Stage.river

    def map_getter(self, stage):
        if stage is Stage.preflop:
            return self.preflop_values
        elif stage is Stage.flop:
            return self.flop_values
        elif stage is Stage.turn:
            return self.turn_values
        elif stage is Stage.river:
            return self.river_values

    def exploration_function(self, q, freq):
        if freq < Ne:
            return optimistic_reward
        else:
            return q

    def learning_rate(self, n):
        return math.log(n+1) / (n+1)

    def end_round(self):
        print self.action_history
        print self.bucket_history

        chips_diff = self.chips - self.chips_before_round  # Positive if won, negative if lost

        #Updating the q-values
        for stage in Stage:
            if stage is not Stage.showdown and len(self.bucket_history) >= stage.value:
                map = self.map_getter(stage)
                bucket = self.bucket_history[stage.value - 1]  # Get corresponding bucket
                act = self.action_history[stage.value - 1]  # get corresponding action
                pair = map[bucket][act]  # returns the corresponding pair

                new_q = pair[0] + self.learning_rate(pair[1]) * (chips_diff)

                map[bucket][act] = (new_q, pair[1] + 1)

    def new_hand(self):
        self.chips_before_round = self.chips
        self.bucket_history = []
        self.action_history = []
        player.new_hand(self) #Do the usual

    #Returns the action based on the exploration function
    def get_action(self, bucket, stage, can_check, can_raise):
        values = self.map_getter(stage)[bucket] #Returns an array[(q1,f1), (q2,f2), (q3,f3)] (call/check, raise, fold)
        max_action = None
        maxq = -10000000

        for i in xrange(len(values)):
            tmp = values[i][0]#self.exploration_function(values[i][0], values[i][1])
            if tmp > maxq:
                max_action = i
                maxq = tmp

        recommended_action = Agent_Bucket.play(self).value - 1
        '''if not (can_check and stage is Stage.preflop): #Opponent raised
            if bucket < 4 and self.chips_before_round-self.chips < 70: #Fold indication and limit for bet
                return 2
        if len(self.bucket_history) > 0 and self.bucket_history[-1] == bucket and bucket < 2 and not can_check:
            max_action = 2'''
        '''if max_action == 2 and can_check and can_raise: #Case where he folds but can check
            max_action = 0

        if max_action == 1 and not can_raise: #case where he choses to raise but can't
            max_action = 0'''

        #act = numpy.random.choice([recommended_action, max_action], 1)
        return max_action


    def play(self, can_check=True, can_raise=True, pot=None):
        stage = self.get_stage() #Returns current stage
        bucket = self.learning_bucket(self.cards, self.community_cards, stage)
        act = self.get_action(bucket, stage, can_check, can_raise)

        if stage.value == len(self.action_history):
            self.action_history[stage.value - 1] = act
            self.bucket_history[stage.value - 1] = bucket
        else:
            self.action_history.append(act)
            self.bucket_history.append(bucket)

        if act == 0:
            return action.call
        elif act == 1:
            return action.bet
        else:
            return action.fold

    def end_game(self):
        with open(preflop_filename,'w') as d:
            json.dump(self.preflop_values, d)
            d.close()
        with open(flop_filename,'w') as d:
            json.dump(self.flop_values, d)
            d.close()
        with open(turn_filename,'w') as d:
            json.dump(self.turn_values,d)
            d.close()
        with open(river_filename,'w') as d:
            json.dump(self.river_values,d)
            d.close()







