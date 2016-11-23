from player import player, action
from Bucketing import Bucketing
from Game import Stage
import json
import math

Ne = 2
optimistic_reward = 10
preflop_filename = "preflop.json"
flop_filename = "flop.json"
turn_filename = "turn.json"
river_filename = "river.json"
class LearningAgent(player):

    #Plays only small blind for now
    def __init__(self, name, starting_chips):
        player.__init__(self, name, starting_chips)
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

        self.bucket_history = [-3]*4
        self.action_history = [-1]*4
        self.chips_before_round = starting_chips

    def initialize_map(self, map, stage):
        if stage is Stage.preflop: #Here we have 2 more buckets
            start = -2
        else:
            start = 0
        for i in xrange(start, 6):
            map[i] = [(0, 0)] * 3 #Because we have 3 actions

    #Introduces two new buckets for preflop stage (-1 for same suit and diff < 3 and -2 for same_suit or diff > 3
    def learning_bucket(self, cards, community_cards, stage):
        bucket = Bucketing().bucketing(cards, community_cards)
        if stage is Stage.preflop: #Preflop bucketing
            diff = abs(cards[0][0] - cards[1][0]) #Difference between the two cards
            if diff == 12: #Adjusts for case of having
                diff = 1
            same_suit = cards[0][1] == cards[1][1]
            if diff < 3 and same_suit:
                bucket = -1
            elif diff < 3 or same_suit:
                bucket = -2
        return bucket

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

    def new_hand(self):
        print self.action_history
        chips_diff = self.chips - self.chips_before_round  #Positive if won, negative if lost
        self.chips_before_round = self.chips #Update for next round
        player.new_hand(self) #Do the usual

        #Updating the q-values
        if self.bucket_history != [-3, -3, -3, -3]:
            for stage in Stage:
                if stage is not Stage.showdown:
                    map = self.map_getter(stage)
                    bucket = self.bucket_history[stage.value - 1] #Get corresponding bucket
                    act = self.action_history[stage.value - 1] #get corresponding action
                    if bucket == -3 or act == -1: #Folded or no more money for one of the players
                        break
                    pair = map[bucket][act] # returns the corresponding pair

                    new_q = pair[0] + self.learning_rate(pair[1]) * (chips_diff)

                    map[bucket][act] = (new_q, pair[1] + 1)

        self.bucket_history = [-3,-3,-3,-3]
        self.action_history = [-1,-1,-1,-1]

    #Returns the action based on the exploration function
    def get_action(self, bucket, stage, can_check, can_raise):
        values = self.map_getter(stage)[bucket] #Returns an array[(q1,f1), (q2,f2), (q3,f3)] (call/check, raise, fold)
        max_action = None
        maxq = -10000000

        for i in xrange(len(values)):
            tmp = self.exploration_function(values[i][0], values[i][1])
            if tmp > maxq:
                max_action = i
                maxq = tmp

        if max_action == 2 and can_check: #Case where he folds but can check
            max_action = 0
        elif max_action == 1 and not can_raise: #case where he choses to raise but can't
            max_action = 0

        return max_action

    def play(self, can_check=True, can_raise=True):
        stage = self.get_stage() #Returns current stage
        bucket = self.learning_bucket(self.cards, self.community_cards, stage)

        act = self.get_action(bucket, stage, can_check, can_raise)
        self.action_history[stage.value - 1] = act
        self.bucket_history[stage.value - 1] = bucket

        if act == 0:
            return action.call
        elif act == 1:
            return action.bet
        else:
            return action.fold

    def end_game(self):
        with open(preflop_filename,'w') as d:
            json.dump(self.preflop_values)
            d.close()
        with open(flop_filename,'w') as d:
            json.dump(self.flop_values)
            d.close()
        with open(turn_filename,'w') as d:
            json.dump(self.turn_values)
            d.close()
        with open(river_filename,'w') as d:
            json.dump(self.river_values)
            d.close()







