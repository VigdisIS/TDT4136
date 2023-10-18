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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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

        # TODO
        "*** YOUR CODE HERE ***"
        # Initialize score with successor game state's score
        return successorGameState.getScore()

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

# $ python pacman.py --pacman=MinimaxAgent
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        # The max_value and min_value functions are implemented per the
        # pseudocode provided in the textbook. These functions will call each
        # other recursively, like two players playing a turn-based game, where
        # the max_value agents in this setting are the Pacman (agentIndex = 0), 
        # and the min_value agents are the ghosts (agentIndex >= 1).
        def max_value(gameState, depth):
            # Check if the game is over by checking if the game is won or lost,
            # or if the depth limit is reached. If so, return the evaluation
            # function value of the current game state.
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return self.evaluationFunction(gameState), ""
            # If not, initialize the value to negative infinity and the action
            # to an empty string. Then, for each legal action, generate the
            # successor game state and call min_value on it. If the returned
            # value is greater than the current value, update the value and
            # action.
            v = float("-inf")
            move = ""
            # For each legal action that Pacman can perform, generate the
            # successor game state and call min_value of it. If the returned
            # value is greater than the current value, update the value and
            # action.
            for a in gameState.getLegalActions(0):
                successor = gameState.generateSuccessor(0, a)
                temp_v, _ = min_value(successor, depth - 1, 1) # Start with the first ghost and increment by 1 for each ghost in the min_value function
                if temp_v > v:
                    v, move = temp_v, a
            # Finally, return the value and action.
            return v, move

        # The min_value function is similar to the max_value function, except
        # that it is called on the ghost agents. The only difference is that
        # the min_value function returns the minimum value and action.
        def min_value(gameState, depth, agentIndex):
            # Like in max_value, check if the game is over by checking if the
            # game is won or lost, or if the depth limit is reached. If so,
            # return the evaluation function value of the current game state.
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return self.evaluationFunction(gameState), ""
            # If not, initialize the value to positive infinity and the action
            # to an empty string. 
            v = float("inf")
            move = ""
            # Then, for each legal action, generate the successor game state and 
            # call max_value on it. If the returned value is less than the 
            # current value, update the value and action.
            for a in gameState.getLegalActions(agentIndex):
                successor = gameState.generateSuccessor(agentIndex, a)
                # If the current agentIndex is the last one, then the next 
                # agent's turn will be Pacman, so we call max_value on it.
                # TODO: Check if this is correct. Maybe use agentindex 1 and 2
                # instead, since pacman isn't moving when not close to ghosts.
                if agentIndex == gameState.getNumAgents() - 1:
                    temp_v, _ = max_value(successor, depth - 1)
                # Otherwise, we call min_value on the next (ghost) agent.
                else:
                    temp_v, _ = min_value(successor, depth, agentIndex + 1)
                if temp_v < v:
                    v, move = temp_v, a
            # Finally, return the value and action.
            return v, move

        # Call max_value on the current game state and return the action.
        _, move = max_value(gameState, self.depth)
        return move

        # util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

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
