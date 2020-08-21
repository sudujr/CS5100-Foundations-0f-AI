import random
"""
    Class VaccumWorld is present to perform extraction of data from environ.txt
    after extraction it stores the details in an object variable
"""
class VaccumWorld:

    def __init__(self):
        self.row = 0
        self.column = 0
        self.grid = [[]]
        self.moves = 0
        self.x = 0
        self.y = 0

    # Function to extract the data from file and store it in the class variable
    def extraction(self, f):
        size = f.readline().split(" ")
        row = int(size[1])
        column = int(size[2])
        f.readline()
        self.row = row
        self.column = column
        d = row
        grid = []
        while d > 0:
            g = f.readline()
            g = " ".join(g.split())
            g = g.split(" ")
            x = [float(i) for i in g]
            grid.append(x)
            d -= 1
        self.grid = grid
        moves = int(f.readline().split(" ")[1])
        self.moves = moves
        initial_location = f.readline().split(" ")
        x = int(initial_location[1]) - 1
        y = int(initial_location[2]) - 1
        self.x = x
        self.y = y

# Function to display the grid along with the postion of agent after N moves
def display(count, N, grid, state):
    if count == N:
        for i in range(len(grid)):
            print("\n")
            for j in range(len(grid[0])):
                if [i,j] == state:
                    print("[",grid[i][j],"]", end = " ")
                else:
                    print(grid[i][j], end =" ")
        count = 0
        print("\n")
    return count

# Function to perform Left operation of an agent
def moveLeft(state, grid, pMeasure):
    state[1] -= 1
    print("L ","{:.2f}".format(pMeasure))
    return state, pMeasure

# Function to perform Right operation of an agent
def moveRight(state, grid, pMeasure):
    state[1] += 1
    print("R ","{:.2f}".format(pMeasure))
    return state, pMeasure

# Function to perform Up operation of an agent
def moveUp(state, grid, pMeasure):
    state[0] -= 1
    print("U ","{:.2f}".format(pMeasure))
    return state, pMeasure

# Function to perform Right operation of an agent
def moveDown(state,grid, pMeasure):
    state[0] += 1
    print("D ","{:.2f}".format(pMeasure))
    return state, pMeasure

# Function to Suck the dirt in agents current location
def suck(state, grid, pMeasure):
    pMeasure += grid[state[0]][state[1]]
    grid[state[0]][state[1]] = 0.0
    print("S ","{:.2f}".format(pMeasure))
    return grid, pMeasure

# Function to check if the agents current location is filled with dirt or not
def checkDirty(grid, state):
    if grid[state[0]][state[1]] > 0:
        return True
    return False

"""
    Class representing the solution for First Agent
    A simple reflex Agent that sucks if the dirt is present at its current location
    else moves within the grid to its neighbours
"""
class AgentOne:
    def __init__(self, vaccumworld):
        self.grid = vaccumworld.grid
        self.moves = vaccumworld.moves
        self.state = [vaccumworld.x, vaccumworld.y]
        self.pMeasure = 0
        self.count = 0

    # Function to perform the reflex operation of Agent One
    def operation(self, N):
        while self.moves > 0:
            if checkDirty(self.grid,self.state):
                self.grid, self.pMeasure = suck(self.state, self.grid, self.pMeasure)
                self.moves -= 1
                self.count += 1
                self.count = display(self.count, N, self.grid, self.state)
            else:
                if self.state[0] == 0 and self.state[1] == len(self.grid[0]) - 1:
                    self.state, self.pMeasure = moveRight(self.state, self.grid, self.pMeasure)
                    self.moves -= 1
                    self.count += 1
                    self.count = display(self.count, N, self.grid, self.state)
                elif self.state[0] == 0:
                    self.state, self.pMeasure = moveDown(self.state, self.grid, self.pMeasure)
                    self.moves -= 1
                    self.count += 1
                    self.count = display(self.count, N, self.grid, self.state)
                elif self.state[0] == len(self.grid) - 1 and self.state[1] == len(self.grid[0]) - 1:
                    self.state, self.pMeasure = moveUp(self.state, self.grid, self.pMeasure)
                    self.moves -= 1
                    self.count += 1
                    self.count = display(self.count, N, self.grid, self.state)
                elif self.state[1] == len(self.grid[0]) - 1:
                    self.state, self.pMeasure = moveLeft(self.state, self.grid, self.pMeasure)
                    self.moves -= 1
                    self.count += 1
                    self.count = display(self.count, N, self.grid, self.state)
                elif self.state[0] == len(self.grid) - 1 and self.state[1] == 0:
                    self.state, self.pMeasure = moveRight(self.state, self.grid, self.pMeasure)
                    self.moves -= 1
                    self.count += 1
                    self.count = display(self.count, N, self.grid, self.state)
                elif self.state[0] == len(self.grid) - 1:
                    self.state, self.pMeasure = moveUp(self.state, self.grid, self.pMeasure)
                    self.moves -= 1
                    self.count += 1
                    self.count = display(self.count, N, self.grid, self.state)
                elif self.state[1] == 0 and self.state[0] == 0:
                    self.state, self.pMeasure = moveDown(self.state, self.grid, self.pMeasure)
                    self.moves -= 1
                    self.count += 1
                    self.count = display(self.count, N, self.grid, self.state)
                elif self.state[1] == 0:
                    self.state, self.pMeasure = moveRight(self.state, self.grid, self.pMeasure)
                    self.moves -= 1
                    self.count += 1
                    self.count = display(self.count, N, self.grid, self.state)
                else:
                    L = random.choice(["U","D","L","R"])
                    if L == "U":
                        self.state, self.pMeasure = moveUp(self.state, self.grid, self.pMeasure)
                        self.moves -= 1
                        self.count += 1
                        self.count = display(self.count, N, self.grid, self.state)
                    if L == "D":
                        self.state, self.pMeasure = moveDown(self.state, self.grid, self.pMeasure)
                        self.moves -= 1
                        self.count += 1
                        self.count = display(self.count, N, self.grid, self.state)
                    if L == "L":
                        self.state, self.pMeasure = moveLeft(self.state, self.grid, self.pMeasure)
                        self.moves -= 1
                        self.count += 1
                        self.count = display(self.count, N, self.grid, self.state)
                    if L == "R":
                        self.state, self.pMeasure = moveRight(self.state, self.grid, self.pMeasure)
                        self.moves -= 1
                        self.count += 1
                        self.count = display(self.count, N, self.grid, self.state)

"""
    Class representing  solution for 2nd agent
    agent uses greedy algorithm to visit the the neighbour with maximum dirt
"""
class AgentTwo:

    def __init__(self,vaccumworld):
        self.grid = vaccumworld.grid
        self.moves = vaccumworld.moves
        self.state = [vaccumworld.x, vaccumworld.y]
        self.pMeasure = 0
        self.count = 0

    # Function to get valid and the best successor to visit next
    # selects a successor randomly if neighbours have a same value of dirt
    def getBestSuccessor(self):
        successor_list = {}
        up = [self.state[0]-1, self.state[1]]
        down = [self.state[0] + 1, self.state[1]]
        left = [self.state[0], self.state[1] - 1]
        right = [self.state[0], self.state[1] + 1]
        if 0 <= up[0] < len(self.grid) and 0 <= up[1] < len(self.grid[0]):
            successor_list[tuple(up)] = self.grid[up[0]][up[1]]
        if 0 <= down[0] < len(self.grid) and 0 <= down[1] < len(self.grid[0]):
            successor_list[tuple(down)] = self.grid[down[0]][down[1]]
        if 0 <= left[0] < len(self.grid) and 0 <= left[1] < len(self.grid[0]):
            successor_list[tuple(left)] = self.grid[left[0]][left[1]]
        if 0 <= right[0] < len(self.grid) and 0 <= right[1] < len(self.grid[0]):
            successor_list[tuple(right)] = self.grid[right[0]][right[1]]
        itemMaxValue = max(successor_list.items(), key=lambda x: x[1])

        listOfKeys = list()
        # Iterate over all the items in dictionary to find keys with max value
        for key, value in successor_list.items():
            if value == itemMaxValue[1]:
                listOfKeys.append(list(key))

        l = random.choice(listOfKeys)
        if [l[0],l[1]] == up:
            print("U ","{:.2f}".format(self.pMeasure))
        elif [l[0],l[1]] == down:
            print("D ","{:.2f}".format(self.pMeasure))
        elif [l[0],l[1]] == left:
            print("L ","{:.2f}".format(self.pMeasure))
        elif [l[0],l[1]]  == right:
            print("R ","{:.2f}".format(self.pMeasure))
        return [l[0],l[1]]

    # Function to perform the operation of Greedy Agent that moves based on
    # the results from the getBestSuccesor function
    def operation(self,N):
        while self.moves > 0:
            if checkDirty(self.grid,self.state):
                self.grid, self.pMeasure = suck(self.state, self.grid, self.pMeasure)
                self.moves -= 1
                self.count += 1
                self.count = display(self.count, N, self.grid, self.state)
            else:
                self.state = self.getBestSuccessor()
                self.moves -= 1
                self.count += 1
                self.count = display(self.count, N, self.grid, self.state)

"""
    Class representing the solution for Agent Three
    Agent Three uses an Optimised greedy Agent 
    The greedy agent keeps track of visited nodes 
    by keeping track of visited nodes it will not visit the same node again if it has a valid unvisted neighbor
    Agent Makes a random movement if only all its neighbours are visited 
"""
class AgentThree:

    def __init__(self,vaccumworld):
        self.grid = vaccumworld.grid
        self.moves = vaccumworld.moves
        self.state = [vaccumworld.x, vaccumworld.y]
        self.pMeasure = 0
        self.count = 0
        self.visited = []

    # Function to get Valid Successors, it returns a list of valid successors
    def getSuccessors(self):
        successor_list = {}
        up = [self.state[0]-1, self.state[1]]
        down = [self.state[0] + 1, self.state[1]]
        left = [self.state[0], self.state[1] - 1]
        right = [self.state[0], self.state[1] + 1]
        successor_list = []
        if 0 <= up[0] < len(self.grid) and 0 <= up[1] < len(self.grid[0]):
            successor_list.append(up)
        if 0 <= down[0] < len(self.grid) and 0 <= down[1] < len(self.grid[0]):
            successor_list.append(down)
        if 0 <= left[0] < len(self.grid) and 0 <= left[1] < len(self.grid[0]):
            successor_list.append(left)
        if 0 <= right[0] < len(self.grid) and 0 <= right[1] < len(self.grid[0]):
            successor_list.append(right)

        return successor_list
    # Function to select the best successor out of the available successors
    def bestSuccessor(self):
        states = self.getSuccessors()
        dictionary = {}
        result = [i for i in states if i not in self.visited]
        for key in result:
            dictionary[tuple(key)] = self.grid[key[0]][key[1]]

        if len(dictionary) != 0:
            itemMaxValue = max(dictionary.items(), key=lambda x: x[1])
            listOfKeys = list()
            for key, value in dictionary.items():
                if value == itemMaxValue[1]:
                    listOfKeys.append(list(key))
            l = random.choice(listOfKeys)
        else:
            l = random.choice(states)
        up = [self.state[0]-1, self.state[1]]
        down = [self.state[0] + 1, self.state[1]]
        left = [self.state[0], self.state[1] - 1]
        right = [self.state[0], self.state[1] + 1]
        if [l[0],l[1]] == up:
            print("U ","{:.2f}".format(self.pMeasure))
        elif [l[0],l[1]] == down:
            print("D ","{:.2f}".format(self.pMeasure))
        elif [l[0],l[1]] == left:
            print("L ","{:.2f}".format(self.pMeasure))
        elif [l[0],l[1]]  == right:
            print("R ","{:.2f}".format(self.pMeasure))
        self.visited += [[l[0],l[1]]]

        return l

    # Function to perform operation for the agent based on the greedy algorithm
    def operation(self,N):
        while self.moves > 0:
            if checkDirty(self.grid,self.state):
                self.grid, self.pMeasure = suck(self.state, self.grid, self.pMeasure)
                self.moves -= 1
                self.count += 1
                self.count = display(self.count, N, self.grid, self.state)
            else:
                self.state = self.bestSuccessor()
                self.moves -= 1
                self.count += 1
                self.count = display(self.count, N, self.grid, self.state)




def main():
    file = open("environ.txt","r")
    N = 5
    # if you want to custom input N uncomment below portion of code
    #N = int(input("Enter less than no of moves\n"))
    v1 = VaccumWorld()
    v1.extraction(file)
    print("\n REFLEX AGENT \n")
    r = AgentOne(v1)
    r.operation(N)
    file.close()
    file = open("environ.txt","r")
    v2 = VaccumWorld()
    v2.extraction(file)
    print("\n GREEDY AGENT \n")
    a = AgentTwo(v2)
    a.operation(N)
    file.close()
    file = open("environ.txt","r")
    v3 = VaccumWorld()
    v3.extraction(file)
    print("\n OPTIMIZED GREEDY AGENT \n")
    m = AgentThree(v3)
    m.operation(N)
    file.close()

if __name__ == "__main__":
        main()