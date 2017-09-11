# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def dfsFinalSolution(problem, currentState, direction, finalList, visited):
    """
    The function takes in 5 parameters :
    problem - Object from the parent function, used mainly to get successor List for every node and to verify if Goal is reached
    curentState - Current node which is being examined in this function
    direction - The direction taken to come to the cuurent node. This will be part of the final solution if the goal is reached through this node
    finalList - Path taken by the Pacman. Passed and returned during all recursive calls
    visited - Dictionary to track all nodes that are visited by the algorithm to avoid going through them again
    """
    # Direction is "None" only for the starting node, for the rest, "direction" is the direction taken to reach the node
    if direction != "None":
        finalList.append(direction)

    # If Goal is reached, return with the final result
    if problem.isGoalState(currentState) == True:
        return finalList, visited, 1

    # Obtain successor List for the current node, mark current node as visited.
    successorsList = problem.getSuccessors(currentState)
    visited[currentState] = 1

    # If there are no successors and the goal state is not achieved, return with fail status to previous node and abandon this path by popping out this path from the final path.
    if len(successorsList) == 0:
        finalList.pop()
        return finalList, visited, 0

    # Go to the first successor, if the goal isn't found, move on to the second successor until the successor List is exhausted.
    for x in successorsList:
        if visited.has_key(x[0]) == False:
            finalList, visited, flag = dfsFinalSolution(problem, x[0], x[1], finalList, visited)
            # flag = 1 implies Goal found, hence return bac with the final path.
            if flag == 1:
                return finalList, visited, 1

    # If none of the nodes in the successor List lead to the goal, return back with failed status
    finalList.pop()
    return finalList, visited, 0

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    # Creating a recursive function so that the currentState can be sent as a parameter.
    finalList, visited, flag = dfsFinalSolution(problem, problem.getStartState(), "None", [], {})
    print "Total Path cost", problem.getCostOfActions(finalList)
    return finalList

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    currentPath, visited = [], {}
    successorsQueue = util.Queue()
    direction = "None"
    successorsQueue.push((problem.getStartState(), direction, []))

    while successorsQueue.isEmpty() == False:
        node = successorsQueue.pop()
        currentState = node[0]
        direction = node[1]
        currentPath = node[2]

        visited[currentState] = 1
        if problem.isGoalState(currentState):
            print "Total Path cost", problem.getCostOfActions(currentPath)
            return currentPath

        successorsList = problem.getSuccessors(currentState)
        for x in successorsList:
            if (visited.has_key(x[0]) == False):
                tempPath = list(currentPath)
                tempPath.append(x[1])
                successorsQueue.push((x[0], x[1], tempPath))

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    expanded = {}
    priorityQueue = util.PriorityQueue()
    priorityQueue.push((problem.getStartState(), "None", []), 0)

    while priorityQueue.isEmpty() == False:
        node = priorityQueue.pop()
        currentState = node[0]
        direction = node[1]
        currentPath = node[2]

        if expanded.has_key(currentState):
            continue

        expanded[currentState] = 1
        if problem.isGoalState(currentState) == True:
            print "Total Path cost", problem.getCostOfActions(currentPath)
            return currentPath

        successorsList = problem.getSuccessors(currentState)
        for x in successorsList:
            tempPath = list(currentPath)
            tempPath.append(x[1])
            priorityQueue.push((x[0], x[1], tempPath), problem.getCostOfActions(tempPath))

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    expanded = {}
    priorityQueue = util.PriorityQueue()
    priorityQueue.push((problem.getStartState(), "None", []), 0)

    while priorityQueue.isEmpty() == False:
        node = priorityQueue.pop()
        currentState = node[0]
        direction = node[1]
        currentPath = node[2]

        if expanded.has_key(currentState):
            continue

        expanded[currentState] = 1
        if problem.isGoalState(currentState) == True:
            print "Total Path cost", problem.getCostOfActions(currentPath)
            return currentPath

        successorsList = problem.getSuccessors(currentState)
        for x in successorsList:
            tempPath = list(currentPath)
            tempPath.append(x[1])
            priorityQueue.push((x[0], x[1], tempPath), (len(tempPath)+heuristic(currentState, problem)))


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
