from Bucketing import Bucketing
from player import player, action
from Game import Stage
from enum import Enum
import numpy
from Deck import ordered_list

step = 0.25

class Strategy(Enum):
    agressive = 1
    defensive = 2
    bluff = 3


class Utility_Agent(player):

    def __init__(self, name, starting_chips, weight, bluff = False):
        player.__init__(self, name, starting_chips)
        self.opp_strategy = Strategy.agressive #Will tend to check and call on smaller amounts and more folds
        self.strategy = Strategy.defensive #Will tend to raise and call on higher amounts
        self.bluff = bluff
        self.step = step
        self.prev_op = '-'

        #These are the parameters, which are a certain number of votes for each heuristic function
        self.prev_action_weight = weight
        self.opp_strategy_votes = 5
        self.game_stage_votes = 5

        self.chips_before_round = starting_chips
        self.opp_actions = [0] * 3 # [call,bet,fold] #Keeps track of number of folds, checks/calls, and raises to determine opp strategy
        self.opp_prevaction = None #Prev action of opponent
        self.num_hands = 0
        self.prev_action = None


    def new_hand(self):
        player.new_hand(self)
        self.chips_before_round = self.chips
        self.opp_prevaction = None

    #Updates the number of checks/raise/fold #!!!Needs to be updated in GAME and PLAYER!!!#
    def opponent_action(self, act):
        if act is not None:
            self.opp_prevaction = act
            self.opp_actions[act.value - 1] += 1

    #Updates both the opponent's strategy and the agent's strategy
    def update_strategy(self, wins):
        if self.opp_actions[0] > (3.0/2) * self.opp_actions[1]: #more checks than raise
            if self.opp_actions[2] > (1.0/4) * self.num_hands:
                self.opp_strategy = Strategy.defensive
            else:
                self.opp_strategy = numpy.random.choice([Strategy.defensive, Strategy.bluff], 1)
        else:
            self.opp_strategy = Strategy.agressive

        if self.opp_strategy == Strategy.defensive or self.opp_strategy == Strategy.bluff:
            if wins > 0:
                self.strategy = Strategy.agressive
            else:
                self.strategy = Strategy.defensive
        else :
            self.strategy = numpy.random.choice([Strategy.bluff, Strategy.defensive], 1) if self.bluff else Strategy.defensive

    #Returns an array of votes [call, raise, fold]
    def get_prevaction_votes(self, expected_wins, round_bet,  win_prob, opp_action, can_check, can_raise):
        if not can_check and opp_action is not action.bet: #Small blind
            return [1,0,0] #Calls anyway

        elif opp_action is action.bet: #opponent raised

            if can_raise: #Can raise again
                if expected_wins > -round_bet/2.0:
                    if win_prob > 0.7:
                        return [5*win_prob, 4*win_prob, (1-win_prob)]
                    else:
                        return [4*win_prob, 2*win_prob, 4*(1-win_prob)]
                else:
                    return [3*win_prob, 0, 6*(1-win_prob)]
            else: #Cannot raise again
                if self.prev_action is action.bet:
                    if expected_wins > 0:
                        if win_prob > 0.75:
                            return [9*win_prob, 0, 1-win_prob]
                        else:
                            return [8*win_prob, 0, 2*(1-win_prob)]
                    else:
                        return [6*win_prob, 0, 3*(1-win_prob)]
                else: #playing small blind and dealer raised
                    if expected_wins > 0 and win_prob > 0.7:
                        return [7*win_prob, 0, 3*(1-win_prob)]
                    else:
                        return [2*win_prob, 0, 5*(1-win_prob)]
        else: #free to do
            if expected_wins > round_bet/2.0:
                if win_prob > 0.8:
                    return [4*win_prob, 5*win_prob, (1-win_prob)]
                else:
                    return [7*win_prob, 2*win_prob, (1-win_prob)]
            else:
                if win_prob > 0.7:
                    return [7*win_prob, win_prob, 2*(1-win_prob)]
                else:
                    return [9*win_prob, 0, (1-win_prob)]



    #Returns an array of votes [call, raise, fold]
    def get_oppstrategy_votes(self, stage, win_prob, pot_size, bet_for_round):
        votes = self.opp_strategy_votes
        expected_wins = win_prob*pot_size - (1-win_prob) * bet_for_round
        if stage is Stage.preflop:
            if self.opp_strategy == Strategy.agressive:
                if expected_wins > 0:
                    return [0.7*win_prob*votes, 0.3*win_prob*votes, (1-win_prob)*votes]
                else:
                    return [0.5 * win_prob * votes, 0.2 * win_prob * votes, (1 - 0.7*win_prob) * votes]

            elif self.opp_strategy == Strategy.defensive:
                if expected_wins > 0:
                    return [0.3 * win_prob * votes, 0.7 * win_prob * votes, (1 - win_prob) * votes]
                else:
                    return [0.25 * win_prob * votes, 0.25 * win_prob * votes, (1 - 0.5*win_prob) * votes]
            else:
                if expected_wins > 0:
                    return [0.7 * win_prob * votes, 0.3 * win_prob * votes, (1 - win_prob) * votes]
                else:
                    return [0.2 * win_prob * votes, 0.2 * win_prob * votes, (1 - 0.4*win_prob) * votes]

        elif stage is Stage.river:
            if self.opp_strategy == Strategy.agressive:
                if expected_wins > 0:
                    return [0.3 * win_prob * votes, 0.7 * win_prob * votes, (1 - win_prob) * votes]
                else:
                    return [0.6 * win_prob * votes, 0.1 * win_prob * votes, (1 - 0.7*win_prob) * votes]
            elif self.opp_strategy == Strategy.defensive:
                if expected_wins > 0:
                    return [0.3 * win_prob * votes, 0.7 * win_prob * votes, (1 - win_prob) * votes]
                else:
                    return [0.4 * win_prob * votes, 0.3 * win_prob * votes, (1 - 0.7*win_prob) * votes]
            else:
                if expected_wins > 0:
                    return [0.7 * win_prob * votes, 0.3 * win_prob * votes, (1 - win_prob) * votes]
                else:
                    return [0.3 * win_prob * votes, 0.3 * win_prob * votes, (1 - 0.6*win_prob) * votes]
        else:
            if self.opp_strategy == Strategy.agressive:
                if expected_wins > 0:
                    return [0.7 * win_prob * votes, 0.3 * win_prob * votes, (1 - win_prob) * votes]
                else:
                    return [0.2 * win_prob * votes, 0.2 * win_prob * votes, (1 - 0.4*win_prob) * votes]
            elif self.opp_strategy == Strategy.defensive:
                if expected_wins > 0:
                    return [0.5 * win_prob * votes, 0.5 * win_prob * votes, (1 - win_prob) * votes]
                else:
                    return [0.3 * win_prob * votes, 0.3 * win_prob * votes, (1 - 0.6*win_prob) * votes]
            else:
                if expected_wins > 0:
                    return [0.7 * win_prob * votes, 0.3 * win_prob * votes, (1 - win_prob) * votes]
                else:
                    return [0.3 * win_prob * votes, 0.3 * win_prob * votes, (1 - 0.6*win_prob) * votes]

    def get_stage_votes(self, stage, win_prob, expected_wins, bet_for_round, can_raise, can_check):

        if stage is Stage.preflop:
            if not can_check and can_raise: #small blind
                if win_prob > 0.85:
                    return [7*win_prob, 2*win_prob, 1-win_prob]
                else:
                    return [9*win_prob, 0, 1-win_prob]
            elif can_check: #Dealer
                if win_prob > 0.9:
                    return [7*win_prob, 2*win_prob, 1-win_prob]
                else:
                    return [10*win_prob, win_prob, 1-win_prob]
            else:#Opponent raised at preflop, call or fold
                if win_prob > 0.9:
                    return [5*win_prob, 0, 1-win_prob]
                else:
                    return [win_prob, 0, 4*(1-win_prob)]

        elif stage is Stage.flop:
            if can_check and can_raise:
                if expected_wins > 0:
                    if win_prob > 0.9:
                        return [4*win_prob, 6*win_prob, 1-win_prob]
                    elif win_prob > 0.7:
                        return [7*win_prob, 2*win_prob, 1-win_prob]
                    else:
                        return [8*win_prob, win_prob, 1-win_prob]
                else:
                    return [7*win_prob, 0, 2*(1-win_prob)]
            elif can_raise: #Opponent raised and we can raise again
                if expected_wins > bet_for_round:
                    if win_prob > 0.9:
                        return [3*win_prob, 7*win_prob, 1-win_prob]
                    elif win_prob > 0.7:
                        return [5*win_prob, 4*win_prob, 1-win_prob]
                    else:
                        return [8*win_prob, 0, 2*(1-win_prob)]
                else:
                    return [4*win_prob, 0, 3*(1-win_prob)]
            else: #call or fold
                if expected_wins > bet_for_round:
                    if win_prob > 0.9:
                        return [9*win_prob, 0, 1-win_prob]
                    elif win_prob > 0.7:
                        return [7*win_prob, 0, 1-win_prob]
                    else:
                        return [6*win_prob, 0, 2*(1-win_prob)]
                else:
                    return [3*win_prob, 0, 4*(1-win_prob)]

        elif stage is Stage.turn:
            if can_check and can_raise:
                if expected_wins > 0:
                    if win_prob > 0.9:
                        return [3*win_prob, 7*win_prob, 1-win_prob]
                    elif win_prob > 0.7:
                        return [5*win_prob, 5*win_prob, 1-win_prob]
                    else:
                        return [8*win_prob, 0, 2*(1-win_prob)]
                else:
                    return [7*win_prob, 0, 2*(1-win_prob)]
            elif can_raise: #Opponent raised and we can raise again
                if expected_wins > bet_for_round:
                    if win_prob > 0.9:
                        return [2*win_prob, 8*win_prob, 1-win_prob]
                    elif win_prob > 0.7:
                        return [5*win_prob, 4*win_prob, 1-win_prob]
                    else:
                        return [2*win_prob, 0, 2*(1-win_prob)]
                else:
                    return [4*win_prob, 0, 3*(1-win_prob)]
            else: #call or fold
                if expected_wins > bet_for_round:
                    if win_prob > 0.9:
                        return [9*win_prob, 0, 1-win_prob]
                    elif win_prob > 0.7:
                        return [7*win_prob, 0, 2*(1-win_prob)]
                    else:
                        return [4*win_prob, 0, 6*(1-win_prob)]
                else:
                    return [3*win_prob, 0, 4*(1-win_prob)]

        else:
            if can_check and can_raise:
                if expected_wins > 0:
                    if win_prob > 0.9:
                        return [2*win_prob, 8*win_prob, 1-win_prob]
                    elif win_prob > 0.7:
                        return [5*win_prob, 4*win_prob, 1-win_prob]
                    else:
                        return [3*win_prob, 0, 2*(1-win_prob)]
                else:
                    return [8*win_prob,0, 1-win_prob]
            elif can_raise: #Opponent raised and we can raise again
                if expected_wins > bet_for_round:
                    if win_prob > 0.9:
                        return [3*win_prob, 7*win_prob, 1-win_prob]
                    elif win_prob > 0.7:
                        return [6*win_prob, 3*win_prob, 1-win_prob]
                    else:
                        return [4*win_prob, 0, 5*(1-win_prob)]
                else:
                    return [2*win_prob, 0, 3*(1-win_prob)]
            else: #call or fold
                if expected_wins > bet_for_round:
                    if win_prob > 0.9:
                        return [9*win_prob, 0, 1-win_prob]
                    elif win_prob > 0.7:
                        return [6*win_prob, 0, 2*(1-win_prob)]
                    else:
                        return [3*win_prob,0, 4*(1-win_prob)]
                else:
                    return [2*win_prob, 0, 4*(1-win_prob)]

    #Returns the current stage
    def get_stage(self):
        if len(self.community_cards) == 0:
            return Stage.preflop
        elif len(self.community_cards) == 3:
            return Stage.flop
        elif len(self.community_cards) == 4:
            return Stage.turn
        else:
            return Stage.river

    def get_votes(self, pot_size, can_check, can_raise):
        stage = self.get_stage()
        win_prob = Bucketing().proba(self.cards, self.community_cards)
        round_bet = self.chips_before_round - self.chips

        expected_wins = win_prob * pot_size - (1 - win_prob) * round_bet

        prev_action_votes = self.get_prevaction_votes(expected_wins, round_bet,win_prob, self.opp_prevaction, can_check, can_raise)
        #opp_strategy_votes = self.get_oppstrategy_votes(stage, win_prob, pot_size, self.round_bet)
        stage_votes = self.get_stage_votes(stage, win_prob, expected_wins, round_bet,can_raise, can_check)

        votes = [0]*3
        for i in range(3):
            votes[i] = stage_votes[i] + prev_action_votes[i] #* self.prev_action_weight  #+ opp_strategy_votes[i]

        s = sum(votes)

        print win_prob
        return [vote/s for vote in votes] #Returns normalized votes corresponding to probabilities

    def update_weights(self, wins): #Upd3
        if wins < 0:
            if self.prev_op == '+':
                if self.prev_action_weight > self.step:
                    self.prev_action_weight -= self.step
                self.prev_op = '-'
            elif self.prev_op == '-':
                self.prev_action_weight += self.step
                self.prev_op = '+'
        else:
            if self.prev_op == '+':
                self.prev_action_weight += self.step
            else:
                if self.prev_action_weight > self.step:
                    self.prev_action_weight -= self.step

        self.prev_action_weight /= 2
        #self.step = self.step/1.3


    def play(self, can_check=False, can_raise=True, pot=None):
        votes = self.get_votes(pot, can_check, can_raise)

        print votes

        act = numpy.random.choice([action.call, action.bet, action.fold],1, p = votes)[0]
        stage = self.get_stage()

        if act == action.fold and (can_check or (not can_check and stage == Stage.preflop and self.opp_prevaction != action.bet)):
            print "not sure"
            act = action.call

        '''if act is action.bet and not can_raise:
            act = action.call'''
        self.opp_prevaction = None
        self.prev_action = act
        return act

    def end_round(self):
        self.num_hands += 1
        #self.update_weights(self.chips - self.chips_before_round)
        #print self.prev_action_weight


    #def end_game(self):