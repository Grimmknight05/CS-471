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

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    """
    Initialize the fringe to track what we need to visit (potentially).
    Fringe will hold tuples (state, path).
    Use a Stack for DFS becuase we want the most recently explored (deepest) 
        node to be explored further before exploring other nodes.
    """
    fringe = util.Stack()

    # add the starting point to the fringe
    currPos = problem.getStartState()
    currPath = []
    currNode = (currPos, currPath)

    fringe.push(currNode)

    # keep track of the set of visited notes to not enter infinite loops
    visited = set()

    # while there are new nodes to visit
    while not fringe.isEmpty():
        """
        Grab the node off the top of the fringe and check if it is the goal state.
        The top of the fringe (most recently added) will always be deeper 
            than the previously visited node since the most recent nodes added to the fringe
            were the previous node's children.
        """
        currNode = fringe.pop()
        currPos = currNode[0]
        currPath = currNode[1]

        if (problem.isGoalState(currPos)):
            return currPath

        # we only want to keep exploring a node's children if we have never visited the node before
        if currPos not in visited:
            visited.add(currPos)

            # getting the successor states of the current state will help expand the graph and our DFS tree
            neighbors = problem.getSuccessors(currPos)
            for node in neighbors:
                # add all the children (successor states) to the fringe
                # a node looks like the 3-tuple (<pos (x,y)>, <action (NSEW)>, <cost>)
                newPath = currPath + [node[1]]
                fringe.push((node[0], newPath))


    # if there is no valid path return no path
    return []



def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    """
    Initialize the fringe to track what we need to visit (potentially).
    Fringe will hold tuples (state, path).
    Use a Queue for BFS becuase we want the least recently explored (shallowest) 
        node to be explored further before exploring deeper nodes.
    """
    fringe = util.Queue()

    # add the starting point to the fringe
    currPos = problem.getStartState()
    currPath = []
    currNode = (currPos, currPath)

    fringe.push(currNode)

    # keep track of the set of visited notes to not enter infinite loops
    visited = set()

    # while there are new nodes to visit
    while not fringe.isEmpty():
        """
        Grab the node off the bottom of the fringe and check if it is the goal state.
        The bottom of the fringe (least recently added) will always be shallower 
            than the previously visited node since the most recent nodes added to the fringe
            were the previous node's children.
        """
        currNode = fringe.pop()
        currPos = currNode[0]
        currPath = currNode[1]

        if (problem.isGoalState(currPos)):
            return currPath

        # we only want to keep exploring a node's children if we have never visited the node before
        if currPos not in visited:
            visited.add(currPos)

            # getting the successor states of the current state will help expand the graph and our BFS tree
            neighbors = problem.getSuccessors(currPos)
            for node in neighbors:
                # add all the children (successor states) to the fringe
                # a node looks like the 3-tuple (<pos (x,y)>, <action (NSEW)>, <cost>)
                newPath = currPath + [node[1]]
                fringe.push((node[0], newPath))


    # if there is no valid path return no path
    return []
    

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    """
    Initialize the fringe to track what we need to visit (potentially).
    Fringe will hold tuples (state, path).
    Use a PriorityQueue for UCS becuase we want the lowest priority (least cost) 
        node to be explored further before exploring more expensive nodes.
    """
    fringe = util.PriorityQueue()

    # add the starting point to the fringe
    currPos = problem.getStartState()
    currPath = []
    currNode = (currPos, currPath)

    fringe.push(currNode, 0)

    # keep track of the set of visited notes to not enter infinite loops
    visited = set()

    # while there are new nodes to visit
    while not fringe.isEmpty():
        """
        Grab the least priority node off the fringe and check if it is the goal state.
        The least priority node will always be the least cost choice.
        """
        currNode = fringe.pop()
        currPos = currNode[0]
        currPath = currNode[1]

        if (problem.isGoalState(currPos)):
            return currPath

        # we only want to keep exploring a node's children if we have never visited the node before
        if currPos not in visited:
            visited.add(currPos)

            # getting the successor states of the current state will help expand the graph
            neighbors = problem.getSuccessors(currPos)
            for node in neighbors:
                # add all the children (successor states) to the fringe
                # a node looks like the 3-tuple (<pos (x,y)>, <action (NSEW)>, <cost>)
                # include the total cost of the path so far for PriorityQueue
                newPath = currPath + [node[1]]
                total_cost = problem.getCostOfActions(newPath)
                fringe.push((node[0], newPath), total_cost)


    # if there is no valid path return no path
    return []


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    
    """
    Initialize the fringe to track what we need to visit (potentially).
    Fringe will hold tuples (state, path).
    Use a PriorityQueue for A* becuase we want the lowest priority (least cost + heuristic) 
        node to be explored further before exploring more expensive nodes.
    """
    fringe = util.PriorityQueue()

    # add the starting point to the fringe
    currPos = problem.getStartState()
    currPath = []
    currNode = (currPos, currPath)

    fringe.push(currNode, (0 + heuristic(currPos, problem)))

    # keep track of the set of visited notes to not enter infinite loops
    visited = set()

    # while there are new nodes to visit
    while not fringe.isEmpty():
        """
        Grab the least priority node off the fringe and check if it is the goal state.
        The least priority node will always be the least cost choice.
        """
        currNode = fringe.pop()
        currPos = currNode[0]
        currPath = currNode[1]

        if (problem.isGoalState(currPos)):
            return currPath

        # we only want to keep exploring a node's children if we have never visited the node before
        if currPos not in visited:
            visited.add(currPos)

            # getting the successor states of the current state will help expand the graph
            neighbors = problem.getSuccessors(currPos)
            for node in neighbors:
                # add all the children (successor states) to the fringe
                # a node looks like the 3-tuple (<pos (x,y)>, <action (NSEW)>, <cost>)
                # include the total cost of the path so far + the heuristic value for PriorityQueue
                newPath = currPath + [node[1]]
                total_cost = problem.getCostOfActions(newPath) + heuristic(node[0], problem)
                fringe.push((node[0], newPath), total_cost)


    # if there is no valid path return no path
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
