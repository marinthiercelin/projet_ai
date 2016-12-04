from player import player, action
from Bucketing import Bucketing
from Game import Stage
import json
import math
from Agent_Bucket import Agent_Bucket
import numpy
from HandComparator import HandComparator

Ne = -1
optimistic_reward = 10
preflop_filename = "preflop2.json"
flop_filename = "flop2.json"
turn_filename = "turn2.json"
river_filename = "river2.json"

preflop_filename1 = "preflop.json"
flop_filename1 = "flop.json"
turn_filename1 = "turn.json"
river_filename1 = "river.json"


class LearningAgent(Agent_Bucket):

    #Plays only small blind for now
    def __init__(self, name, starting_chips, num):
        if num == 1:
            self.preflop = preflop_filename1
            self.flop = flop_filename1
            self.turn = turn_filename1
            self.river= river_filename1
        elif num == 2:
            self.preflop = preflop_filename
            self.flop = flop_filename
            self.turn = turn_filename
            self.river = river_filename
        Agent_Bucket.__init__(self, name, starting_chips)
        try:
            with open(self.preflop) as d:
                self.preflop_values = json.load(d)
                d.close()
            with open(self.flop) as d:
                self.flop_values = json.load(d)
                d.close()
            with open(self.turn) as d:
                self.turn_values = json.load(d)
                d.close()
            with open(self.river) as d:
                self.river_values = json.load(d)
                d.close()
            #raise IOError
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
        self.action_history = [[],[],[],[]] #one for each stage
        self.opp_prev_action = None
        self.starting_chips = starting_chips
        self.opp_action_history = [[], [], [], []]
        self.dealer = False
        self.opponent_hand = None
        self.comp = HandComparator()
        self.bad_folds = 0


    def initialize_map(self, map, stage):
        if stage is Stage.preflop: #Here we have 2 more buckets
            start = -2
        elif stage is Stage.flop:
            start = -3 #3 new buckets for flop stage (-3:open ended straight draw, -2:middle card straight draw, -1 flush draw)
        else:
            start = 0

        for i in xrange(start, 6):
            map[str(i)] = [[1, 1, 1], [1,1,1]] #2 actions for opponent and 3 actions for player

    #Introduces two new buckets for preflop stage (-1 for same suit and diff < 3 and -2 for same_suit or diff > 3
    @staticmethod
    def learning_bucket(cards, community_cards, stage, comp=None):
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
        elif stage is Stage.flop and comp is not None:
            straight_draw = comp.straight_draw(cards + community_cards)
            flush_draw = comp.flush_draw(cards + community_cards)
            if flush_draw:
                bucket = -1
            elif straight_draw == 1:
                bucket = -2
            elif straight_draw == 2: #open ended straight draw
                bucket = -3
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

    #Learns new values when student has not folded
    def learn(self, actions, opponent_actions, buckets, amount, dealer, fold=False):
        for i in reversed(range(1, 5)):
            if len(buckets) >= i:
                map = self.map_getter(Stage(i))
                bucket = buckets[i - 1]  # Get corresponding bucket
                acts = actions[i - 1]  # get corresponding actions list
                opp_acts = opponent_actions[i - 1] #list for
                location = map[bucket]

                if dealer: #Can have only one decision based on action of opponent
                    opp_act = opp_acts[0] #action
                    act = acts[0] #reaction
                    #q_value = location[opp_act][act]
                else: #can have two decisions
                    if len(acts) == 2: #have to update two values
                        if not fold:
                            opp_act1 = 0 #Consider it as nothing
                            act1 = acts[0]
                            self.update_list(location, opp_act1, act1, math.fabs(amount)/amount)
                        opp_act = opp_acts[0] #Reaction of opponent to act1
                        act = acts[1]  # reaction of player to opp_act2

                    else: #update one value here opponent
                        opp_act = 0 #player is small blind to opponent doesnt play before it
                        act = acts[0]

                        print acts, opp_acts

                self.update_list(location, opp_act, act, math.fabs(amount)/amount )
                if fold:
                    break

    #Updates the values according to the outcome
    def update_list(self, location, opp_action, act, win):
        if opp_action == 0 and act == 0 and win < 0:
            location[opp_action][act] += win/2.0
        else:
            location[opp_action][act] += win

    def opponent_cards(self, cards):
        self.opponent_hand = cards

    def learn_from_fold(self):
        opp_hand = self.comp.get_hand(self.opponent_hand + self.community_cards)
        my_hand = self.comp.get_hand(self.cards + self.community_cards)
        winner = self.comp.compare_hands(opp_hand, my_hand)

        if winner is my_hand:  # bad fold
            self.learn(self.action_history, self.opp_action_history
                               , self.bucket_history, -1, self.dealer, fold=True)
            self.bad_folds += 1

        elif winner is opp_hand:
            self.learn(self.action_history, self.opp_action_history
                               , self.bucket_history, 1, self.dealer, fold=True)

    def end_round(self):
        chips_diff = self.chips - self.chips_before_round  # Positive if won, negative if lost

        if not self.folded and chips_diff != 0:  # Case where we fold to be treated separately
            self.learn(self.action_history, self.opp_action_history, self.bucket_history, chips_diff, self.dealer)
        elif self.folded and self.get_stage() is not Stage.preflop:
            self.learn_from_fold()

    def new_hand(self):
        self.chips_before_round = self.chips
        self.dealer = not self.dealer
        self.bucket_history = []
        self.action_history = [[], [], [], []]
        self.opp_action_history = [[], [], [], []]
        self.opponent_hand = None
        player.new_hand(self) #Do the usual

    #Returns the action based on the exploration function
    def get_action(self, bucket, stage, opp_action, can_check, can_raise):
        values = self.map_getter(stage)[bucket][opp_action]

        max_action = None
        maxq = -10000000

        '''for i in xrange(len(values)):
            tmp = values[i]
            if tmp > maxq:
                max_action = i
                maxq = tmp

        if self.learning:
            randomize = numpy.random.choice(5)
            if randomize == 1:
                max_action = numpy.random.choice(3)'''

        max_action = numpy.random.choice([0, 1, 2], p=self.normalize(values))

        if max_action == 2 and can_check: #or stage is Stage.preflop and not can_check and can_raise:
            max_action = 0

        if max_action == 1 and not can_raise: #case where he choses to raise but can't
            max_action = 0

        return max_action

    @staticmethod
    def normalize(list):
        if list is not None:
            min_elem = min(list)
            if min_elem <= 0:
                l = [e - min_elem + 1 for e in list]
            else:
                l = list
            s = sum(l)
            if s == 0:

                raise ImportError(l)

            return [e*1.0 / s for e in l]
        else:
            raise ImportError




    def play(self, can_check=True, can_raise=True, pot=None):
        stage = self.get_stage() #Returns current stage
        bucket = self.learning_bucket(self.cards, self.community_cards, stage, self.comp)

        act = self.get_action(bucket, stage, self.opp_prev_action, can_check, can_raise)

        if stage.value != len(self.bucket_history):
            self.bucket_history.append(bucket)

        self.action_history[stage.value - 1].append(act)

        if act == 0:
            return action.call
        elif act == 1:
            return action.bet
        else:
            return action.fold

    def end_game(self):
        with open(self.preflop,'w') as d:
            json.dump(self.preflop_values, d)
            d.close()
        with open(self.flop,'w') as d:
            json.dump(self.flop_values, d)
            d.close()
        with open(self.turn,'w') as d:
            json.dump(self.turn_values,d)
            d.close()
        with open(self.river,'w') as d:
            json.dump(self.river_values,d)
            d.close()

    def opponent_action(self, act):
        stage = self.get_stage()
        if act is action.bet or act is action.call:
            self.opp_action_history[stage.value - 1].append(act.value-1)
            self.opp_prev_action = act.value - 1
        elif act is None: #If he receives none then he plays first
            self.dealer = False
            self.opp_prev_action = 0


class Teacher(Agent_Bucket):

    def __init__(self, name, chips, student):
        Agent_Bucket.__init__(self, name, chips)
        self.action_history = [[], [], [], []]
        self.bucket_history = []
        self.wins = 0
        self.student = student
        self.chips_before_round = 0
        self.dealer = False
        self.comp = HandComparator()

    def get_stage(self):
        if len(self.community_cards) == 0:
            return Stage.preflop
        elif len(self.community_cards) == 3:
            return Stage.flop
        elif len(self.community_cards) == 4:
            return Stage.turn
        else:
            return Stage.river

    def play(self, can_check=False, can_raise=True, pot=None):
        act = Agent_Bucket.play(self, can_check, can_raise)
        stage = self.get_stage()
        bucket = LearningAgent.learning_bucket(self.cards, self.community_cards, stage, self.comp)

        if stage.value != len(self.bucket_history):
            self.bucket_history.append(bucket)

        self.action_history[stage.value - 1].append(act.value - 1)
        return act


    def end_round(self):
        diff = self.chips - self.chips_before_round #pos if won negative if lost
        if diff > 0 and self.student.learning:
            self.student.learn(self.action_history, self.student.action_history, self.bucket_history, diff, self.dealer)

    def new_hand(self):
        player.new_hand(self)
        self.wins = 0
        self.action_history = [[], [], [], []]
        self.bucket_history = []
        self.chips_before_round = self.chips
        self.dealer = not self.dealer

    def win_money(self, amount):
        player.win_money(self, amount)
        self.wins = amount

    def opponent_action(self, act):
        if act is None:  # If he receives none then he plays first
            self.dealer = False










