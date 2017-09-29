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

        if successorGameState.isWin():
          return 9999
        if successorGameState.isLose():
          return 0

        ghostPos = [successorGameState.getGhostPosition(agentIndex) for agentIndex in range(1, len(newGhostStates)+1)]
        scaryNum = 0
        for pos in ghostPos:
          distToGhost = util.manhattanDistance(successorGameState.getPacmanPosition(), pos)
          if distToGhost < 5:
            scaryNum += (5 - distToGhost) * 5

        return (successorGameState.getScore() - scaryNum)

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

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

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
        legalMoves = gameState.getLegalActions()

        scores = [self.getAllPossibleStates(gameState.generateSuccessor(0, move), 1, self.depth) for move in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)

        return legalMoves[chosenIndex]

    def getAllPossibleStates(self, gameState, agentIndex, localdepth):
        legalMoves = gameState.getLegalActions(agentIndex)
        scores = []

        if len(legalMoves) == 0 and agentIndex == gameState.getNumAgents()-1:
          if localdepth == 1:
            return self.evaluationFunction(gameState)
          else:
            scores.append(self.bestPacmanResponse(gameState, localdepth-1))
        elif len(legalMoves) == 0 and agentIndex != gameState.getNumAgents()-1:
          return self.getAllPossibleStates(gameState, agentIndex+1, localdepth)

        if len(legalMoves) != 0:
          for move in legalMoves:
            if agentIndex == gameState.getNumAgents()-1:
              if localdepth == 1:
                return self.evaluationFunction(gameState)
              else:
                scores.append(self.bestPacmanResponse(gameState.generateSuccessor(agentIndex, move), localdepth-1))
            else:
              return self.getAllPossibleStates(gameState.generateSuccessor(agentIndex, move), agentIndex+1, localdepth)

        bestScore = min(scores)
        return bestScore

    def bestPacmanResponse(self, gameState, localdepth):
        legalMoves = gameState.getLegalActions()
        if len(legalMoves) == 0:
          return self.getAllPossibleStates(gameState, 1, localdepth)

        scores = []
        for move in legalMoves:
          scores.append(self.getAllPossibleStates(gameState.generateSuccessor(0, move), 1, localdepth))

        bestScore = max(scores)
        return bestScore

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        legalMoves = gameState.getLegalActions()
        alpha = -999999
        beta = 999999

        # scores = [self.getAllPossibleStates(gameState.generateSuccessor(0, move), 1, alpha, beta, self.depth) for move in legalMoves]
        scores = []
        for move in legalMoves:
          tempAlpha = self.getAllPossibleStates(gameState.generateSuccessor(0, move), 1, alpha, beta, self.depth)
          if tempAlpha > alpha:
            alpha = tempAlpha
          scores.append(tempAlpha)
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)

        return legalMoves[chosenIndex]

    def getAllPossibleStates(self, gameState, agentIndex, alpha, beta, localdepth):

        if alpha > beta:
          return beta

        legalMoves = gameState.getLegalActions(agentIndex)
        scores = []

        if len(legalMoves) == 0 and agentIndex == gameState.getNumAgents()-1:
          if localdepth == 1:
            tempBeta = self.evaluationFunction(gameState)
            if tempBeta < beta:
              beta = tempBeta
            return beta
          else:
            tempBeta = self.bestPacmanResponse(gameState, alpha, beta, localdepth-1)
            if tempBeta < beta:
              beta = tempBeta
        elif len(legalMoves) == 0 and agentIndex != gameState.getNumAgents()-1:
          return self.getAllPossibleStates(gameState, agentIndex+1, alpha, beta, localdepth)

        if len(legalMoves) != 0:
          for move in legalMoves:
            if agentIndex == gameState.getNumAgents()-1:
              if localdepth == 1:
                tempBeta = self.evaluationFunction(gameState)
                if tempBeta < beta:
                  beta = tempBeta
                return beta
              else:
                if alpha > beta:
                  return beta
                tempBeta = self.bestPacmanResponse(gameState.generateSuccessor(agentIndex, move), alpha, beta, localdepth-1)
                if tempBeta < beta:
                  beta = tempBeta
            else:
              return self.getAllPossibleStates(gameState.generateSuccessor(agentIndex, move), agentIndex+1, alpha, beta, localdepth)

        return beta

    def bestPacmanResponse(self, gameState, alpha, beta, localdepth):
        if alpha > beta:
          return alpha

        legalMoves = gameState.getLegalActions()
        if len(legalMoves) == 0:
          tempAlpha = self.getAllPossibleStates(gameState, 1, alpha, beta, localdepth)
          if tempAlpha > alpha:
            alpha = tempAlpha
          return alpha

        scores = []
        for move in legalMoves:
          if alpha > beta:
            return alpha
          tempAlpha = self.getAllPossibleStates(gameState.generateSuccessor(0, move), 1, alpha, beta, localdepth)
          if tempAlpha > alpha:
            alpha = tempAlpha

        return alpha

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

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

