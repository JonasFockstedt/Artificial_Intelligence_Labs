from poker_game_example import PokerPlayer, GameState, get_next_states
import numpy as np


class RandomAgent(PokerPlayer):
    def __init__(self, current_hand=None, stack=300, action=None, action_value=None):
        super().__init__(current_hand_=current_hand, stack_=stack,
                         action_=action, action_value_=action_value)
        self.nodesExpanded = 0
        self.depthLimit = True

    def determineNextState(self, state_queue):
        # Picks random element from the state queue.
        randIndex = np.random.randint(0, len(state_queue))
        return get_next_states(state_queue.pop(randIndex))
