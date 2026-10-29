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
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
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

    def evaluationFunction(self, currentGameState: GameState, action):
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

        # find the closest food
        food_dist = -100
        for (x,y) in newFood.asList():
            dist = util.manhattanDistance(newPos,(x,y))
            if food_dist < 0 or dist < food_dist:
                food_dist = dist


        # find the closest ghost
        active_ghost_dist = -100
        scared_ghost_dist = -100
        for ghostState in newGhostStates:
            pos = ghostState.getPosition()
            dist = util.manhattanDistance(newPos,pos)
            
            scared_time = ghostState.scaredTimer
            scared = scared_time > dist # don't get close to it if you won't be able to reach it in time
           

            if scared and (scared_ghost_dist < 0 or dist < scared_ghost_dist):
                scared_ghost_dist = dist
                            
            elif active_ghost_dist < 0 or dist < active_ghost_dist:
                active_ghost_dist = dist


        # ensure our scores aren't negative and we never divide by zero
        # add multipliers to the ghost scores since they are more important
        food_score = max(1/(food_dist+1),0)
        scared_ghost_score = max(5/(scared_ghost_dist+1),0)

        # if a ghost is sufficiently far away, just ignore it
        if active_ghost_dist > 3:
            active_ghost_score = 0
        else:
            active_ghost_score = max(5/(active_ghost_dist+1),0)
        

        total_score = food_score + scared_ghost_score - active_ghost_score

        return (successorGameState.getScore() + total_score)

def scoreEvaluationFunction(currentGameState: GameState):
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

    def getAction(self, gameState: GameState):
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
        n = gameState.getNumAgents()

        # define the recurrsion within the function 
        # so we can pass our depth and next agent
        def minimax(g:GameState, d, a):
            # if we hit depth, or win, or lose, stop
            if d == 0 or g.isLose() or g.isWin(): 
                return self.evaluationFunction(g)

            # find our next action, mod n since we want to loop through each agent
            # our depth should only decrease if we restarted at pacman (0)
            next_a = (a+1) % n
            next_d = (d-1) if next_a==0 else d

            # the MAX case
            if a == 0:
                # initialize the value to arbitrarily large negative
                # update value (utility) as we traverse the tree looking for the maximum
                v = -float('inf')
                for action in g.getLegalActions(a):
                    succ = g.generateSuccessor(a,action)
                    v = max(v,minimax(succ, next_d, next_a)) 
                return v

            # the MIN case
            else:
                # initialize the value to arbitrarily large positive
                # update value (utility) as we traverse the tree looking for the minimum
                v = float('inf')
                for action in g.getLegalActions(a):
                    succ = g.generateSuccessor(a,action)
                    v = min(v,minimax(succ, next_d, next_a)) 
                return v
            

        d = self.depth
        a = 0
        next_a = (a+1) % n

        # keep tract of the best move to return
        best_move = None
        best_score = -float('inf')

        # start the loop on all actions pacman can take, so we can return a next step
        for action in gameState.getLegalActions(a):
            succ = gameState.generateSuccessor(a,action)

            # recurse through minimax for each subtree
            score = minimax(succ, d, next_a)

            # update our best found score as we go
            if score>best_score:
                best_score = score
                best_move = action

        return best_move
            

        

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        n = gameState.getNumAgents()

        # define the recurrsion within the function 
        # so we can pass our depth and next agent
        def minimax(g:GameState, d, agent, a, b):
            # if we hit depth, or win, or lose, stop
            if d == 0 or g.isLose() or g.isWin(): 
                return self.evaluationFunction(g)

            # find our next action, mod n since we want to loop through each agent
            # our depth should only decrease if we restarted at pacman (0)
            next_agent = (agent+1) % n
            next_d = (d-1) if next_agent==0 else d

            # the MAX case
            if agent == 0:
                # initialize the value to arbitrarily large negative
                # update value (utility) as we traverse the tree looking for the maximum
                v = -float('inf')
                for action in g.getLegalActions(agent):
                    succ = g.generateSuccessor(agent,action)
                    v = max(v,minimax(succ, next_d, next_agent, a, b))
                    if v > b: return v
                    a = max(a,v)
                return v

            # the MIN case
            else:
                # initialize the value to arbitrarily large positive
                # update value (utility) as we traverse the tree looking for the minimum
                v = float('inf')
                for action in g.getLegalActions(agent):
                    succ = g.generateSuccessor(agent,action)
                    v = min(v,minimax(succ, next_d, next_agent, a, b))
                    if v < a: return v
                    b = min(b,v)
                return v
            

        d = self.depth
        agent = 0
        next_agent = (agent+1) % n

        # keep tract of the best move to return
        best_move = None
        best_score = -float('inf')

        alpha = -float('inf')
        beta = float('inf')

        # start the loop on all actions pacman can take, so we can return a next step
        for action in gameState.getLegalActions(agent):
            succ = gameState.generateSuccessor(agent,action)
            
            # recurse through minimax for each subtree
            score = minimax(succ, d, next_agent, alpha, beta)

            # max like function
            # update our best found score as we go
            if score>best_score:
                best_score = score
                best_move = action

            # pruning steps
            if score > beta:
                best_move = action
                break
            alpha = max(alpha,score)

        return best_move

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
