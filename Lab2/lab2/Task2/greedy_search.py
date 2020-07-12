from poker_game_example import PokerPlayer, GameState, get_next_states
import numpy as np


class GreedyAgent(PokerPlayer):
    def __init__(self, current_hand=None, stack=300, action=None, action_value=None):
        super().__init__(current_hand_=current_hand, stack_=stack,
                         action_=action, action_value_=action_value)
        self.nodesExpanded = 0
        self.depthLimit = False

    def determineNextState(self, state_queue):
        state_queue.sort(key=lambda childState: childState.nn_current_hand)
        return get_next_states(state_queue.pop(0))
