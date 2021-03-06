import poker_environment as pe_
from poker_environment import AGENT_ACTIONS, BETTING_ACTIONS
import copy


MAX_HANDS = 4
INIT_AGENT_STACK = 400
MAX_EXTENDED = 100000


class PokerGame():
    def __init__(self, agent):
        self.agent = agent
        self. opponent = PokerPlayer(
            current_hand_=None, stack_=INIT_AGENT_STACK, action_=None, action_value_=None)
        self.init_state = GameState(nn_current_hand_=0,
                                    nn_current_bidding_=0,
                                    phase_='INIT_DEALING',
                                    pot_=0,
                                    acting_agent_=None,
                                    agent_=agent,
                                    opponent_=self.opponent,
                                    )
        self.game_state_queue = []
        self.game_on = True
        self.round_init = True
        self.nodesExpanded = 0
        self.end_state = None

    def checkIfEndGame(self, _state_):
        # or _state_.MAX_HANDS >= 4):
        if _state_.phase == 'SHOWDOWN' and _state_.agent.stack >= 500 or self.agent.depthLimit and self.agent.nodesExpanded > MAX_EXTENDED:
            return True
        return False

    def startGame(self):
        while self.game_on:
            if self.round_init:
                self.round_init = False
                states_ = get_next_states(self.init_state)
                self.game_state_queue.extend(states_[:])
            else:
                # Pop next state from queue
                states_ = self.agent.determineNextState(self.game_state_queue)
                self.game_state_queue.extend(states_)
                self.agent.nodesExpanded += len(states_)

                # If the game should end
                for state in states_:
                    if self.checkIfEndGame(state):
                        self.end_state = state
                        self.game_on = False

    # Prints all states.

    def printResultingState(self):
        state = self.end_state
        if state != None:
            nn_level = 0

            print('------------ print game info ---------------')
            if state.agent.stack > state.opponent.stack:
                result = 'Win'
            elif state.opponent.stack > state.agent.stack:
                result = 'Loss'
            else:
                result = 'Draw'

            print(f'\
                  Result: {result} \
                  Agent stack: {state.agent.stack} \
                  Opponent stack: {state.opponent.stack} \
                  Nodes expanded: {self.agent.nodesExpanded} \
                  Amount of hands dealt: {state.nn_current_hand}')


"""
Player class
"""


class PokerPlayer(object):
    def __init__(self, current_hand_=None, stack_=300, action_=None, action_value_=None):
        self.current_hand = current_hand_
        self.current_hand_type = []
        self.current_hand_strength = []
        self.stack = stack_
        self.action = action_
        self.action_value = action_value_

    """
    identify agent hand and evaluate it's strength
    """

    def evaluate_hand(self):
        self.current_hand_type = pe_.identify_hand(self.current_hand)
        self.current_hand_strength = pe_.Types[self.current_hand_type[0]]*len(
            pe_.Ranks) + pe_.Ranks[self.current_hand_type[1]]

    """
    return possible actions, fold if there is not enough money...
    """

    def get_actions(self):
        actions_ = []
        for _action_ in AGENT_ACTIONS:
            if _action_[:3] == 'BET' and int(_action_[3:]) >= (self.stack):
                actions_.append('FOLD')
            else:
                actions_.append(_action_)
        return set(actions_)


"""
Game State class
"""


class GameState(object):
    def __init__(self,
                 nn_current_hand_=None,
                 nn_current_bidding_=None,
                 phase_=None,
                 pot_=None,
                 acting_agent_=None,
                 parent_state_=None,
                 children_state_=None,
                 agent_=None,
                 opponent_=None):

        self.nn_current_hand = nn_current_hand_
        self.nn_current_bidding = nn_current_bidding_
        self.phase = phase_
        self.pot = pot_
        self.acting_agent = acting_agent_
        self.parent_state = parent_state_
        self.children = children_state_
        self.agent = agent_
        self.opponent = opponent_
        self.showdown_info = None

    """
    draw 10 cards randomly from a deck
    """

    def dealing_cards(self):
        agent_hand, opponent_hand = pe_.generate_2hands()
        self.agent.current_hand = agent_hand
        self.agent.evaluate_hand()
        self.opponent.current_hand = opponent_hand
        self.opponent.evaluate_hand()
        #self.showdown_info = None

    """
    draw 10 cards from a fixed sequence of hands
    """

    def dealing_cards_fixed(self):
        self.agent.current_hand = pe_.fixed_hands[self.nn_current_hand][0]
        self.agent.evaluate_hand()
        self.opponent.current_hand = pe_.fixed_hands[self.nn_current_hand][1]
        self.opponent.evaluate_hand()

    """
    SHOWDOWN phase, assign pot to players
    """

    def showdown(self):

        if self.agent.current_hand_strength == self.opponent.current_hand_strength:
            self.showdown_info = 'draw'
            if self.acting_agent == 'agent':
                self.agent.stack += (self.pot - 5) / 2. + 5
                self.opponent.stack += (self.pot - 5) / 2.
            else:
                self.agent.stack += (self.pot - 5) / 2.
                self.opponent.stack += (self.pot - 5) / 2. + 5
        elif self.agent.current_hand_strength > self.opponent.current_hand_strength:
            self.showdown_info = 'agent win'
            self.agent.stack += self.pot
        else:
            self.showdown_info = 'opponent win'
            self.opponent.stack += self.pot

    # print out necessary information of this game state
    def print_state_info(self):

        print('************* state info **************')
        print('nn_current_hand', self.nn_current_hand)
        print('nn_current_bidding', self.nn_current_bidding)
        print('phase', self.phase)
        print('pot', self.pot)
        print('acting_agent', self.acting_agent)
        print('parent_state', self.parent_state)
        print('children', self.children)
        print('agent', self.agent)
        print('opponent', self.opponent)

        if self.phase == 'SHOWDOWN':
            print('---------- showdown ----------')
            print('agent.current_hand', self.agent.current_hand)
            print(self.agent.current_hand_type,
                  self.agent.current_hand_strength)
            print('opponent.current_hand', self.opponent.current_hand)
            print(self.opponent.current_hand_type,
                  self.opponent.current_hand_strength)
            print('showdown_info', self.showdown_info)

        print('----- agent -----')
        print('agent.current_hand', self.agent.current_hand)
        print('agent.current_hand_type', self.agent.current_hand_type)
        print('agent.current_hand_strength', self.agent.current_hand_strength)
        print('agent.stack', self.agent.stack)
        print('agent.action', self.agent.action)
        print('agent.action_value', self.agent.action_value)

        print('----- opponent -----')
        print('opponent.current_hand', self.opponent.current_hand)
        print('opponent.current_hand_type', self.opponent.current_hand_type)
        print('opponent.current_hand_strength',
              self.opponent.current_hand_strength)
        print('opponent.stack', self.opponent.stack)
        print('opponent.action', self.opponent.action)
        print('opponent.action_value', self.opponent.action_value)
        print('**************** end ******************')


# copy given state in the argument
def copy_state(game_state):
    _state = copy.copy(game_state)
    _state.agent = copy.copy(game_state.agent)
    _state.opponent = copy.copy(game_state.opponent)
    return _state


"""
successor function for generating next state(s)
"""


def get_next_states(last_state):

    if last_state.phase == 'SHOWDOWN' or last_state.acting_agent == 'opponent' or last_state.phase == 'INIT_DEALING':

        # NEW BETTING ROUND, AGENT ACT FIRST

        states = []

        for _action_ in last_state.agent.get_actions():

            _state_ = copy_state(last_state)
            _state_.acting_agent = 'agent'

            if last_state.phase == 'SHOWDOWN' or last_state.phase == 'INIT_DEALING':
                _state_.dealing_cards()

            if _action_ == 'CALL':

                _state_.phase = 'SHOWDOWN'
                _state_.agent.action = _action_
                _state_.agent.action_value = 5
                _state_.agent.stack -= 5
                _state_.pot += 5

                _state_.showdown()

                _state_.nn_current_hand += 1
                _state_.nn_current_bidding = 0
                _state_.pot = 0
                _state_.parent_state = last_state
                states.append(_state_)

            elif _action_ == 'FOLD':

                _state_.phase = 'SHOWDOWN'
                _state_.agent.action = _action_
                _state_.opponent.stack += _state_.pot

                _state_.nn_current_hand += 1
                _state_.nn_current_bidding = 0
                _state_.pot = 0
                _state_.parent_state = last_state
                states.append(_state_)

            elif _action_ in BETTING_ACTIONS:

                _state_.phase = 'BIDDING'
                _state_.agent.action = _action_
                _state_.agent.action_value = int(_action_[3:])
                _state_.agent.stack -= int(_action_[3:])
                _state_.pot += int(_action_[3:])

                _state_.nn_current_bidding += 1
                _state_.parent_state = last_state
                states.append(_state_)

            else:

                print('...unknown action...')
                exit()

        return states

    elif last_state.phase == 'BIDDING' and last_state.acting_agent == 'agent':

        states = []
        _state_ = copy_state(last_state)
        _state_.acting_agent = 'opponent'

        opponent_action, opponent_action_value = pe_.poker_strategy_example(last_state.opponent.current_hand_type[0],
                                                                            last_state.opponent.current_hand_type[1],
                                                                            last_state.opponent.stack,
                                                                            last_state.agent.action,
                                                                            last_state.agent.action_value,
                                                                            last_state.agent.stack,
                                                                            last_state.pot,
                                                                            last_state.nn_current_bidding)

        if opponent_action == 'CALL':

            _state_.phase = 'SHOWDOWN'
            _state_.opponent.action = opponent_action
            _state_.opponent.action_value = 5
            _state_.opponent.stack -= 5
            _state_.pot += 5

            _state_.showdown()

            _state_.nn_current_hand += 1
            _state_.nn_current_bidding = 0
            _state_.pot = 0
            _state_.parent_state = last_state
            states.append(_state_)

        elif opponent_action == 'FOLD':

            _state_.phase = 'SHOWDOWN'

            _state_.opponent.action = opponent_action
            _state_.agent.stack += _state_.pot

            _state_.nn_current_hand += 1
            _state_.nn_current_bidding = 0
            _state_.pot = 0
            _state_.parent_state = last_state
            states.append(_state_)

        elif opponent_action + str(opponent_action_value) in BETTING_ACTIONS:

            _state_.phase = 'BIDDING'

            _state_.opponent.action = opponent_action
            _state_.opponent.action_value = opponent_action_value
            _state_.opponent.stack -= opponent_action_value
            _state_.pot += opponent_action_value

            _state_.nn_current_bidding += 1
            _state_.parent_state = last_state
            states.append(_state_)

        else:
            print('unknown_action')
            exit()
        return states
