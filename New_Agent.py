from Bucketing import Bucketing
from player import player, action
from Game import Stage
from enum import Enum
import numpy

class Strategy(Enum):
    agressive = 1
    defensive = 2
    bluff = 3


class Utility_Agent(player):

    def __init__(self, name, starting_chips, bluff = False):
        player.__init__(self, name, starting_chips)
        self.opp_strategy = Strategy.defensive #Will tend to check and call on smaller amounts and more folds
        self.strategy = Strategy.agressive #Will tend to raise and call on higher amounts
        self.bluff = bluff

        #These are the parameters, which are a certain number of votes for each heuristic function
        self.prev_action_votes = 5
        self.opp_strategy_votes = 5
        self.game_stage_votes = 5

        self.round_bet = 0
        self.chips_before_round = starting_chips
        self.opp_actions = [0] * 3 # [call,bet,fold] #Keeps track of number of folds, checks/calls, and raises to determine opp strategy
        self.opp_prevaction = None #Prev action of opponent
        self.num_hands = 0


    def new_hand(self):
        player.new_hand(self)
        self.round_bet = 0
        self.chips_before_round = self.chips
        self.opp_prevaction = None

    #Updates the number of checks/raise/fold #!!!Needs to be updated in GAME and PLAYER!!!#
    def opponent_action(self, act):
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
    def get_prevaction_votes(self, stage, win_prob, opp_action):
        votes = self.prev_action_votes
        if stage is Stage.preflop:
            if opp_action == action.bet:
                if self.strategy == Strategy.defensive: #Being defensive
                    return [0.5*win_prob*votes, 0.5*win_prob*votes, (1-win_prob)*votes]
                else: #bluffing
                    return [0.25*win_prob*votes, 0.75*win_prob*votes, (1-win_prob)*votes]
            else: #Checked/called or folded
                if self.strategy == Strategy.defensive:
                    return [0.8*votes, 0.2*votes, 0]
                else:
                    return [0.5*votes, 0.5*votes, 0]
        elif stage is Stage.flop:
            if self.opp_prevaction == action.bet:
                if self.strategy == Strategy.agressive or self.strategy == Strategy.bluff:
                    return [0.4 * win_prob * votes, 0.6 * win_prob * votes, (1 - win_prob) * votes]
                else:
                    return [0.7 * win_prob * votes, 0.1 * win_prob * votes, (1 - 0.8 * win_prob) * votes]
            else:
                if self.strategy == Strategy.defensive:
                    return [0.8*win_prob*votes, 0.2*win_prob*votes, (1-win_prob)*votes]
                elif self.strategy == Strategy.agressive:
                    return [0.5*win_prob*votes, 0.5*win_prob*votes, (1-win_prob)*votes]
                else: #Bluffing
                    return [0.2*(1-win_prob)*votes,0.8*(1-win_prob), 0]
        else:
            if self.opp_prevaction == action.bet:
                if self.strategy == Strategy.agressive:
                    return [0.35 * win_prob * votes, 0.65 * win_prob * votes, (1 - win_prob) * votes]
                elif self.strategy == Strategy.bluff:
                    return [0.1*(1-win_prob)*votes, 0.9*(1-win_prob), 0]
                else:
                    return [0.7 * win_prob * votes, 0.1 * win_prob * votes, (1 - 0.8 * win_prob) * votes]
            else:
                if self.strategy == Strategy.defensive:
                    return [0.8*win_prob*votes, 0.2*win_prob*votes, (1-win_prob)*votes]
                elif self.strategy == Strategy.agressive:
                    return [0.5*win_prob*votes, 0.5*win_prob*votes, (1-win_prob)*votes]
                else: #Bluffing
                    return [0.2*(1-win_prob)*votes,0.8*(1-win_prob), 0]

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

    def get_stage_votes(self, stage, win_prob, pot_size, bet_for_round):
        expected_wins = win_prob*pot_size - (1-win_prob)*bet_for_round
        print expected_wins
        votes = self.game_stage_votes
        if stage is Stage.preflop:
            if expected_wins >= 0:
                return [0.5*votes, 0.5*win_prob*votes, 0.5*(1-win_prob)*votes]
            else:
                return [0.3 * win_prob * votes, 0.3 * win_prob * votes, (1 - 0.6*win_prob) * votes]
        elif stage is Stage.flop:
            if expected_wins >= 0:
                return [0.5 * votes, 0.5 * win_prob * votes, 0.5*(1 - win_prob) * votes]
            else:
                return [0.1 * win_prob * votes, 0.1 * win_prob * votes, (1 - 0.2*win_prob) * votes]
        elif stage is Stage.turn:
            if expected_wins >= 0:
                return [0.6 * votes, 0.4 * win_prob * votes, 0.4*(1 - win_prob) * votes]
            else:
                return [0.2 * win_prob * votes, 0.1 * win_prob * votes, (1 - 0.3*win_prob) * votes]
        else:
            if expected_wins >= -pot_size/10:
                return [0.5*votes, 0.2 * win_prob * votes + 0.3*votes, 0.2*(1 - win_prob) * votes]
            else:
                return [0.2 * win_prob * votes, 0.1 * win_prob * votes, (1 - 0.3*win_prob) * votes]

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

    def get_votes(self, pot_size):
        stage = self.get_stage()
        win_prob = Bucketing().proba(self.cards, self.community_cards)
        self.round_bet = self.chips_before_round - self.chips
        #prev_action_votes = self.get_prevaction_votes(stage,win_prob,self.opp_prevaction)
        #opp_strategy_votes = self.get_oppstrategy_votes(stage, win_prob, pot_size, self.round_bet)
        stage_votes = self.get_stage_votes(stage, win_prob, pot_size, self.round_bet)

        votes = [0]*3
        for i in range(3):
            votes[i] = stage_votes[i] #+ prev_action_votes[i]  #+ opp_strategy_votes[i]

        s = sum(votes)

        print votes, s, win_prob
        return [vote/s for vote in votes] #Returns normalized votes corresponding to probabilities

    #def update_votes(self): #Upd3
    # ates the number of votes for each stage and each heuristic corresponding to the win or loss

    def play(self, can_check=False, can_raise = True, pot=None):
        votes = self.get_votes(pot)
        act = numpy.random.choice([action.call, action.bet, action.fold], p = votes)
        stage = self.get_stage()
        if act == action.fold and (can_check or (not can_check and stage == Stage.preflop and self.opp_prevaction != action.bet)):
            act = action.call
        return act

    def end_round(self):
        self.num_hands += 1

    #def end_game(self):