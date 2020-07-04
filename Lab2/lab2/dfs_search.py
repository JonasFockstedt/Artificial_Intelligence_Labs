from search_algorithm import PriorityQueue
from Node import Node
from operator import itemgetter
import numpy as np
import random


def search(_map, start, goal):
    # Finds the neighbors of the given node.
    def get_neighbors(node):
        actions = [[-1, 0],  # go up
                   [0, -1],  # go left
                   [1, 0],  # go down
                   [0, 1]]  # do right

        possible_actions = []
        visited_states = [element for element in came_from.values()]
        in_frontier = [node[1:] for node in frontier]

        # Find out the possible actions to take from the current node.
        for action in actions:
            neighbor_node = [node[1] + action[0], node[2] + action[1]]
            
            # -1 not in neighbor_node - if the neighbor node is outside the map.
            # neighbor_node[0] <= len(_map) - if the neighbor node is outside the map.
            # neighbor_node[1] <= len(_map[0]) - if the neighbor node is outside the map.
            if -1 not in neighbor_node and neighbor_node[0] < len(_map) and neighbor_node[1] < len(_map[0]):
                if neighbor_node not in visited_states and neighbor_node not in in_frontier and _map[neighbor_node[0]][neighbor_node[1]] != -1:
                    possible_actions.append(neighbor_node)

        return (possible_actions)

    # Computes the cost to reach the next cell.

    def cost_function(g):
        return g + 1

    # cost moving to another cell
    moving_cost = 1

    # open list
    frontier = []
    #frontier = PriorityQueue()

    start = start.tolist()
    goal = goal.tolist()

    
    # add starting cell to open list
    frontier.append([0] + start)      # [cost, x, y]
    #frontier.add(start, 0)

    # path taken
    came_from = {}

    # expanded list with cost value for each cell
    cost = {}
    visited_nodes = [[],[]]

    # init. starting node
    parent = None
    g = 0
    
    print('Searching...')

    # if there is still nodes to open
    while frontier:
        counter = 0
        # Pick node which has the biggest cost.
        current_node = frontier.pop()
        #print(current_node)
        visited_nodes[0].append(current_node[1])
        visited_nodes[1].append(current_node[2])

        # check if the goal is reached
        if current_node[1:] == goal:
            break

        # for each neighbor of the current cell
        # Implement get_neighbors function (return nodes to expand next)
        # (make sure you avoid repetitions!)
        for next in get_neighbors(current_node):
            # compute cost to reach next cell
            # Implement cost function
            cost = cost_function(g)

            # add next cell to open list
            frontier.append([cost, next[0], next[1]])
            frontier = sorted(frontier, key=itemgetter(0))
            # add to path
            came_from[tuple(next)] = current_node[1:]

        g += 1
        counter+=1
        if counter > 20:
            break

    return solve_path(came_from, start, goal)


# Returns the soled path.
def solve_path(came_from, start, goal):
    print('Calculating solved path...')
    solved_path = [[],[]]
    current_node = goal
    solved_path[0].append(current_node[1])    # Required to swap places between x and y coordinate.
    solved_path[1].append(current_node[0])    # Required to swap places between x and y coordinate.
    while current_node != start:
        current_node = came_from[tuple(current_node)]
        solved_path[0].append(current_node[1])
        solved_path[1].append(current_node[0])
    return solved_path
    