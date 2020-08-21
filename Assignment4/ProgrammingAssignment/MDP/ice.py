# "MDPs on Ice - Assignment 5"
# Ported from Java

import random
import numpy as np
import copy
import sys

GOLD_REWARD = 100.0
PIT_REWARD = -150.0
DISCOUNT_FACTOR = 0.5
EXPLORE_PROB = 0.2  # for Q-learning
LEARNING_RATE = 0.1
ITERATIONS = 10000
MAX_MOVES = 1000
ACTIONS = 4
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
MOVES = ['U', 'R', 'D', 'L']

# Fixed random number generator seed for result reproducibility --
# don't use a random number generator besides this to match sol
random.seed(5100)


# Problem class:  represents the physical space, transition probabilities, reward locations,
# and approach to use (MDP or Q) - in short, the info in the text file
class Problem:
    # Fields:
    # approach - string, "MDP" or "Q"
    # move_probs - list of doubles, probability of going 1,2,3 spaces
    # map - list of list of strings: "-" (safe, empty space), "G" (gold), "P" (pit)

    # Format looks like
    # MDP    [approach to be used]
    # 0.7 0.2 0.1   [probability of going 1, 2, 3 spaces]
    # - - - - - - P - - - -   [space-delimited map rows]
    # - - G - - - - - P - -   [G is gold, P is pit]
    #
    # You can assume the maps are rectangular, although this isn't enforced
    # by this constructor.

    # __init__ consumes stdin; don't call it after stdin is consumed or outside that context
    def __init__(self):
        self.approach = input('Reading mode...')
        print(self.approach)
        probs_string = input("Reading transition probabilities...\n")
        self.move_probs = [float(s) for s in probs_string.split()]
        self.map = []
        for line in sys.stdin:
            self.map.append(line.split())

    def solve(self, iterations):
        if self.approach == "MDP":
            return mdp_solve(self, iterations)
        elif self.approach == "Q":
            return q_solve(self, iterations)
        return None


# Policy: Abstraction on the best action to perform in each state - just a 2D string list-of-lists
class Policy:
    def __init__(self, problem):  # problem is a Problem
        # Signal 'no policy' by just displaying the map there
        self.best_actions = copy.deepcopy(problem.map)

    def __str__(self):
        return '\n'.join([' '.join(row) for row in self.best_actions])


# roll_steps:  helper for try_policy and q_solve -- "rolls the dice" for the ice and returns
# the new location (r,c), taking map bounds into account
# note that move is expecting a string, not an integer constant
def roll_steps(move_probs, row, col, move, rows, cols):
    displacement = 1
    total_prob = 0
    move_sample = random.random()
    for p, prob in enumerate(problem.move_probs):
        total_prob += prob
        if move_sample <= total_prob:
            displacement = p + 1
            break
    # Handle "slipping" into edge of map
    new_row = row
    new_col = col
    if not isinstance(move, str):
        print("Warning: roll_steps wants str for move, got a different type")
    if move == "U":
        new_row -= displacement
        if new_row < 0:
            new_row = 0
    elif move == "R":
        new_col += displacement
        if new_col >= cols:
            new_col = cols - 1
    elif move == "D":
        new_row += displacement
        if new_row >= rows:
            new_row = rows - 1
    elif move == "L":
        new_col -= displacement
        if new_col < 0:
            new_col = 0
    return new_row, new_col

# try_policy:  returns avg utility per move of the policy, as measured by "iterations"
# random drops of an agent onto empty spaces, running until gold, pit, or time limit
# MAX_MOVES is reached
def try_policy(policy, problem, iterations):
    total_utility = 0
    total_moves = 0
    for i in range(iterations):
        # Resample until we have an empty starting square
        while True:
            row = random.randrange(0, len(problem.map))
            col = random.randrange(0, len(problem.map[0]))
            if problem.map[row][col] == "-":
                break
        for moves in range(MAX_MOVES):
            total_moves += 1
            policy_rec = policy.best_actions[row][col]
            # Take the move - roll to see how far we go, bump into map edges as necessary
            row, col = roll_steps(problem.move_probs, row, col, policy_rec, len(problem.map), len(problem.map[0]))
            if problem.map[row][col] == "G":
                total_utility += GOLD_REWARD
                break
            if problem.map[row][col] == "P":
                total_utility += PIT_REWARD
                break
    return total_utility / total_moves


# Generates legal moves available for the agent to move from a state
def legalMoves(row,column):
    moves = []
    if column - 1 >= 0:
        moves.append('L')
    if row + 1 < len(problem.map):
        moves.append('D')
    if row - 1 >= 0:
        moves.append('U')
    if column + 1 < len(problem.map[0]):
        moves.append('R')

    return moves


# Generates the maximum utility value of a state from all the possible utility values allowed based onpossible legal moves
# returns value and the direction
def Q_max(moves, R,V_copy,i, j,problem):
    A = {a: 0 for a in moves}
    for m in moves:
        if m == 'U':
            x = i
            for p in problem.move_probs:
                x = x - 1
                if x >= 0:
                    A[m] += p * (R[x][j] + (DISCOUNT_FACTOR * V_copy[x][j]))
                else:
                    z = x + 1 if x + 1 >= 0 else x + 2
                    A[m] += p * (R[z][j] + (DISCOUNT_FACTOR * V_copy[z][j]))
        elif m == 'D':
            x = i
            for p in problem.move_probs:
                x = x + 1
                if x < len(problem.map):
                    A[m] += p * (R[x][j] + (DISCOUNT_FACTOR * V_copy[x][j]))
                else:
                    z = x - 1 if x - 1 < len(problem.map) else x - 2
                    A[m] += p * (R[z][j] + (DISCOUNT_FACTOR * V_copy[z][j]))
        elif m == 'R':
            y = j
            for p in problem.move_probs:
                y = y + 1
                if y < len(problem.map[0]):
                    A[m] += p * (R[i][y] + (DISCOUNT_FACTOR * V_copy[i][y]))
                else:
                    z = y - 1 if y - 1 < len(problem.map[0]) else y - 2
                    A[m] += p * (R[i][z] + (DISCOUNT_FACTOR * V_copy[i][z]))
        elif m == 'L':
            y = j
            for p in problem.move_probs:
                y = y - 1
                if y >= 0:
                    A[m] += p * (R[i][y] + (DISCOUNT_FACTOR * V_copy[i][y]))
                else:
                    z = y + 1 if y + 1 >= 0 else y + 2
                    A[m] += p * (R[i][z] + (DISCOUNT_FACTOR * V_copy[i][z]))
    max_key = max(A, key=A.get)
    return max_key, A[max_key]


# Function to calculate the reward for moving from one state to another state in the durection of m
def rewardCalc(i, j, m, R, problem):
    reward = 0
    if m == 'U':
        x = i
        for p in problem.move_probs:
            x = x - 1
            if x >= 0:
                reward += p * R[x][j]
            else:
                z = x + 1 if x + 1 >= 0 else x + 2
                reward += p * R[z][j]
    elif m == 'D':
        x = i
        for p in problem.move_probs:
            x = x + 1
            if x < len(problem.map):
                reward += p * R[x][j]
            else:
                z = x - 1 if x - 1 < len(problem.map) else x - 2
                reward += p * R[z][j]
    elif m == 'R':
        y = j
        for p in problem.move_probs:
            y = y + 1
            if y < len(problem.map[0]):
                reward += p * R[i][y]
            else:
                z = y - 1 if y - 1 < len(problem.map[0]) else y - 2
                reward += p * R[i][z]
    elif m == 'L':
        y = j
        for p in problem.move_probs:
            y = y - 1
            if y >= 0:
                reward += p * R[i][y]
            else:
                z = y + 1 if y + 1 >= 0 else y + 2
                reward += p * R[i][z]
    return reward


# Function to generate the coordinates of the next move
def nextMove(m,i,j):
    if m == 'U':
        i -= 1
    elif m == 'D':
        i += 1
    elif m == 'L':
        j -= 1
    elif m == 'R':
        j += 1
    return i,j

# mdp_solve:  use [iterations] iterations of the Bellman equations over the whole map in [problem]
# and return the policy of what action to take in each square
def mdp_solve(problem, iterations):
    # makes the copy of a map
    grid = copy.deepcopy(problem.map)
    # Initial Utility Matrix
    V = [[0 for j in range(len(problem.map[0]))] for i in range(len(problem.map))]
    # Reward Matrix
    R = [[0 if problem.map[i][j] == '-' else GOLD_REWARD if problem.map[i][j] == 'G' else PIT_REWARD for j in range(len(problem.map[0]))] for i in range(len(problem.map))]
    while iterations > 0:
        # Creates a copy of utility matrix for every new iteration
        V_copy = copy.deepcopy(V)
        for i in range(len(problem.map)):
            for j in range(len(problem.map[0])):
                # if the goal is met skip the state and go onto next state
                if problem.map[i][j] == 'G' or problem.map[i][j] == 'P':
                    continue
                # compute the maximum possible utility value for that state along with the direction
                key, value = Q_max(legalMoves(i,j),R,V_copy, i,j,problem)
                # update the utility matrix
                V[i][j] = value
                # update the map with direction
                problem.map[i][j] = key
        iterations -= 1
    # Generate the Policy based on above computation
    policy = Policy(problem)
    # reset the map to original value
    problem.map = grid
    return policy


def q_solve(problem, iterations):
    # makes the copy of a map
    grid = copy.deepcopy(problem.map)
    # Reward Matrix
    R = [[0 if problem.map[i][j] == '-' else GOLD_REWARD if problem.map[i][j] == 'G' else PIT_REWARD for j in range(len(problem.map[0]))] for i in range(len(problem.map))]
    # Initial Q matrix
    Q = [[{m: 0 for m in legalMoves(i,j)} if problem.map[i][j] == '-' else {m: GOLD_REWARD for m in legalMoves(i, j)} if problem.map[i][j] =='G' else {m: PIT_REWARD for m in legalMoves(i, j)} for j in range(len(problem.map[0]))] for i in range(len(problem.map))]
    while iterations > 0:
        # Generates Random starting state
        while True:
            i = random.randrange(0, len(problem.map))
            j = random.randrange(0, len(problem.map[0]))
            if problem.map[i][j] == "-":
                break
        while True:
            # goes to next iteration of goal is met
            if problem.map[i][j] == 'G' or problem.map[i][j] == 'P':
                break
            # EXPLORE_PROB is used to determine whether a random action or maximum qvalue diection based action is taken or not
            choice = random.choices([1,2], weights=[EXPLORE_PROB,1 - EXPLORE_PROB], k=1)
            # direction m is chosen from the available moves based on the choice
            if choice[0] == 1:
                m = random.choice(legalMoves(i,j))
            else:
                m = max(Q[i][j], key=Q[i][j].get)
            #Stores the root location
            x, y = i, j
            # moves to next location based on m
            i, j = nextMove(m,i,j)
            # computes possible rewards for moving from root location to next location based on m
            reward = rewardCalc(x,y,m,R,problem)
            #key, value = Q_max(legalMoves(i, j),R, V_copy, i, j, problem)
            #V[i][j] = value
            # computes the direction of the maximum Q value
            key = max(Q[i][j], key=Q[i][j].get)
            # Q[i][j][key] is same as  value

            # Q learning eqution which updates the Q values for every movement made
            Q[x][y][m] += LEARNING_RATE * (reward + (DISCOUNT_FACTOR * Q[i][j][key]) - Q[x][y][m])
        iterations -= 1
    # Update the policy based on the best Q value for each state
    for i in range(len(problem.map)):
        for j in range(len((problem.map[0]))):
            if problem.map[i][j] == 'G' or problem.map[i][j] == 'P':
                continue
            problem.map[i][j] = max(Q[i][j], key=Q[i][j].get)
    # Generate policy based on above computation
    policy = Policy(problem)
    # reset the map to original grid
    problem.map = grid
    return policy


# Main:  read the problem from stdin, print the policy and the utility over a test run
if __name__ == "__main__":
    problem = Problem()
    policy = problem.solve(ITERATIONS)
    print(policy)
    print("Calculating average utility...")
    print("Average utility per move: {utility:.2f}".format(utility=try_policy(policy, problem, ITERATIONS)))

