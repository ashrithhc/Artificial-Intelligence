# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """
    def __init__(self):
        self.nodes = 0

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        # Gets the manhattan distance between pacman and the ghost for every ghost - stores it in a list.
        ghostDistances = [manhattanDistance(ghostState.getPosition(), newPos) for ghostState in newGhostStates]
        
        # List of all coordinates where the food is present in the grid
        foodList = newFood.asList()
        # Gets the manhattan distance between pacman and the food for every food available in the grid - stores in a list
        foodDistances = [manhattanDistance(food, newPos) for food in foodList]

        # Calculating nodes expanded
        self.nodes += 1

        # If no food is present, goal is achieved, return current game state score
        if len(foodDistances) == 0:
            print self.nodes
            self.nodes = 0
            return successorGameState.getScore()

        # Multiply the current game state score by a factor of 'n' where n is a ratio of the distance to the nearest ghost to distance to nearest food.
        return ( min(ghostDistances) * (1.0/(min(foodDistances)))) + successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)
        self.node = 0

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """    
    def pacmanBestMove(self, state, agent, localDepth):
        # Returns the best score that can be achieved by the pacman - Max function in the minimax algorithm

        # Calculate nodes expanded for report purpose
        self.node += 1

        # If game is won or lost, OR if the depth limit is reached, return
        if localDepth == (self.depth * state.getNumAgents()) or state.isWin() or state.isLose():
            return self.evaluationFunction(state)

        # For each move possible at this state, get the best possible 'minimax' game state after Ghost makes the next move (Min function)
        maxValue = float("-inf")
        for move in state.getLegalActions(agent):
            maxValue = max(maxValue,self.ghostBestMove(state.generateSuccessor(agent,move), (agent+1)%(state.getNumAgents()), localDepth+1))          
        return maxValue
    
    def ghostBestMove(self, state, agent, localDepth):
        # Returns the best score that can be achieved by the pacman - Min function in the minimax algorithm

        # Calculate nodes expanded for report purpose
        self.node += 1

        # If game is won or lost, OR if the depth limit is reached, return
        if localDepth == (self.depth * state.getNumAgents()) or state.isWin() or state.isLose():
            return self.evaluationFunction(state)

        # For each move possible at this state, get the best possible 'minimax' game state after Pacman makes the next move (Max function)
        minValue = float("inf")
        for move in state.getLegalActions(agent):
            # If there are no more ghosts to make a move, go to pacman (Max function)
            if agent+1 == state.getNumAgents():
              minValue = min(minValue, self.pacmanBestMove(state.generateSuccessor(agent,move), (agent+1)%(state.getNumAgents()), localDepth+1))          
            # If there are more ghosts to make a move, go to the next ghost (Min function)
            else:
              minValue = min(minValue, self.ghostBestMove(state.generateSuccessor(agent,move), (agent+1)%(state.getNumAgents()), localDepth+1))          
        return minValue
      
    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        # localDepth stores the depth at which we are traversing, agent stores the agent index
        localDepth = 0
        agent = 0
        # Get all possible moves possible for pacman to make
        legalMoves = gameState.getLegalActions(agent)

        # for each legal move possible, calculate the best possible 'minimax' game state and return the score of that game state
        scores = [self.ghostBestMove(gameState.generateSuccessor(agent,move), agent+1, localDepth+1) for move in legalMoves]
        # choose the best score
        bestScore = max(scores)
        # Get the index of legalMoves which has the best score
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)

        # The best move according to minimax is returned
        return legalMoves[chosenIndex]
        
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    
    def pacmanBestMove(self, state, agent, localDepth, alpha, beta, action):
      # Returns the best score that can be achieved by the pacman - Max function in the minimax algorithm with Alpha-beta pruning

      # If game is won or lost, OR if the depth limit is reached, return
      if localDepth == (self.depth * state.getNumAgents()) or state.isWin() or state.isLose():
          return [self.evaluationFunction(state), action]

      # we set the default value of direction to stop, but it will eventually be changed
      maxValue = [float("-inf"), Directions.STOP]

      # for each legal move possible, calculate the best possible 'Alpha beta' game state after Ghost makes the next move (Min function)
      for move in state.getLegalActions(agent):
          tempValue = self.ghostBestMove(state.generateSuccessor(agent, move), (agent+1)%(state.getNumAgents()), localDepth+1, alpha, beta, move)
          tempValue[1] = move # Action stored in temp value
          if tempValue[0] > maxValue[0]: # If score returned on current action is greater than the best score for this game state, store this score as the best score for this game state
            maxValue = tempValue
          if maxValue[0] >= beta: # If Max score of this game state is greater than beta, no point continuing further, return MaxValue
              return maxValue
          alpha = max(alpha, maxValue[0]) # If all moves are explored, alpha will be the mximum of the them unless Alpha is greater than the best score
      return maxValue
    
    def ghostBestMove(self, state, agent, localDepth, alpha, beta, action):
      # Returns the best score that can be achieved by the ghost - Min function in the minimax algorithm with Alpha-beta pruning

      # If game is won or lost, OR if the depth limit is reached, return
      if localDepth == (self.depth * state.getNumAgents()) or state.isWin() or state.isLose():
          return [self.evaluationFunction(state), action]

      # we set the default value of direction to stop, but it will eventually be changed
      minValue = [float("inf"),Directions.STOP]

      # for each legal move possible, calculate the best possible 'Alpha beta' game state after Pacman makes the next move (Max function)
      for move in state.getLegalActions(agent):
          # If there are no more ghosts to make a move, go to pacman (Max function)
          if agent + 1 == state.getNumAgents():
            tempv = self.pacmanBestMove(state.generateSuccessor(agent, move), (agent+1)%(state.getNumAgents()), localDepth+1, alpha, beta, move)
          # If there are more ghosts to make a move, go to the next ghost (Min function)
          else:
            tempv = self.ghostBestMove(state.generateSuccessor(agent, move), (agent+1)%(state.getNumAgents()), localDepth+1, alpha, beta, move)
          tempv[1] = move # Action stored in temp value
          if tempv[0] < minValue[0]: # If score returned on current action is less than the best score for this game state, store this score as the best score for this game state
            minValue = tempv
          if minValue[0] < alpha: # If Max score of this game state is less than alpha, no point continuing further, return MinValue
            return minValue
          beta = min(beta, minValue[0]) # If all moves are explored, beta will be the minimum of the them unless beta is less than the best score
      return minValue

    def getAction(self, gameState):
      """
        Returns the minimax action using self.depth and self.evaluationFunction
      """
      "*** YOUR CODE HERE ***"
      # Default values for alpha, beta and action
      alpha = float("-inf")
      beta = float("inf")
      action = Directions.STOP
      v = self.pacmanBestMove(gameState, 0, 0, alpha, beta, action) # Get the best move out of all legal possible moves
      return v[1]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def pacmanBestMove(self, state, agent, localDepth):
        # If game is won or lost, OR if the depth limit is reached, return
        if localDepth == (self.depth * state.getNumAgents()) or state.isWin() or state.isLose():
            return self.evaluationFunction(state)

        # For each move possible at this state, get the best possible 'Alpha beta' game state after Ghost makes the next move (Min function)
        maxValue = float("-inf")
        for move in state.getLegalActions(agent):
            maxValue = max(maxValue,self.ghostBestMove(state.generateSuccessor(agent,move), (agent+1)%(state.getNumAgents()), localDepth+1))          
        return maxValue
    
    def ghostBestMove(self, state, agent, localDepth):
        # If game is won or lost, OR if the depth limit is reached, return
        if localDepth == (self.depth * state.getNumAgents()) or state.isWin() or state.isLose():
            return self.evaluationFunction(state)

        # For each move possible at this state, get the best possible 'Alpha beta' game state after Pacman makes the next move (Max function) and add it to the total score
        minValue = float("inf")
        sumOfAllMoves = 0
        for move in state.getLegalActions(agent):
            # If there are no more ghosts to make a move, go to pacman (Max function)
            if agent+1 == state.getNumAgents():
              sumOfAllMoves += self.pacmanBestMove(state.generateSuccessor(agent,move), (agent+1)%(state.getNumAgents()), localDepth+1) # Max function
            # If there are more ghosts to make a move, go to the next ghost (Min function)
            else:
              sumOfAllMoves += self.ghostBestMove(state.generateSuccessor(agent,move), (agent+1)%(state.getNumAgents()), localDepth+1) # Min function
        return sumOfAllMoves/len(state.getLegalActions(agent)) # Return the average of all the scores for each move possible (Expectimax)

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        # localDepth stores the depth at which we are traversing, agent stores the agent index
        localDepth = 0
        agent = 0
        # Get all possible moves possible for pacman to make
        legalMoves = gameState.getLegalActions(agent)

        # for each legal move possible, calculate the best possible 'Alpha beta pruning' game state and return the score of that game state
        scores = [self.ghostBestMove(gameState.generateSuccessor(agent,move), agent+1, localDepth+1) for move in legalMoves]
        # choose the best score
        bestScore = max(scores)
        # Get the index of legalMoves which has the best score
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)
        # The best move according to Alpha beta pruning is returned
        return legalMoves[chosenIndex]

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

