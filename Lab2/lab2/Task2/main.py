from random_search import RandomAgent
from bfs import BreadthFirstAgent
from poker_game_example import PokerGame
from greedy_search import GreedyAgent

INIT_AGENT_STACK = 400

randomAgent = RandomAgent(
    current_hand=None, stack=INIT_AGENT_STACK, action=None, action_value=None)
bfsAgent = BreadthFirstAgent(
    current_hand=None, stack=INIT_AGENT_STACK, action=None, action_value=None)
greedyAgent = GreedyAgent(
    current_hand=None, stack=INIT_AGENT_STACK, action=None, action_value=None)

print('Result random agent')
random_game = PokerGame(randomAgent)
random_game.startGame()
random_game.printResultingState()

print('Result breadth first agent')
breadth_game = PokerGame(bfsAgent)
breadth_game.startGame()
breadth_game.printResultingState()

print('Result greedy agent')
greedy_game = PokerGame(greedyAgent)
greedy_game.startGame()
greedy_game.printResultingState()
