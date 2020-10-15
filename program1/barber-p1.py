# Ryan Barber
# CISC 481 
# Project 1

import sys
import cProfile
from collections import deque
import copy

# Functions and Node class

#Node class for holding board, depth, parents, children, parent move
class Node:
	children = None
	f_score = 0
	def __init__(self, board, parentMove, parent, depth):
		self.board = board
		self.parent = parent
		self.parentMove = parentMove #root does not have parent move
		self.depth = depth

#Since my profiler does not include memory info, I am using
#this funciton to get the max size of the frontier in each search
def getMaxListSize(nodeList, currentMax):
	newMax = 0
	if(len(nodeList) > currentMax):
		newMax = len(nodeList)
		return newMax
	else:
		return currentMax

# PART 1
# Write a function possible-actions that takes a board as input 
# and outputs a list of all actions possible on the given board.
def possibleActions(board):
	#find empty spot
	for i in range(len(board)):#row = i
		for j in range(len(board[i])):#col = j
			if board[i][j] == None:
				#if empty spot is on corner:
				if i==0 and j==0:
					return ["up","left"]
				elif i==0 and j==len(board)-1:
					return ["up","right"]
				elif i==len(board)-1 and j==0:
					return ["down","left"]
				elif i==len(board)-1 and j==len(board)-1:
					return ["down","right"]
				#if empty spot is on middle edge
				elif 0<i<len(board)-1 and j==0:
					return ["down","left","up"]
				elif 0<i<len(board)-1 and j==len(board)-1:
					return ["down","right","up"]
				elif i==0 and 0<j<len(board)-1:
					return ["left","right","up"]
				elif i==len(board)-1 and 0<j<len(board)-1:
					return ["left","right","down"]
				#else its in the middle so all 4 moves possible
				else: return ["left","right","up","down"]


# PART 2
#Write a function result that takes as input an action and a board and 
#outputs the new board that will result after actually carrying out the
#input move in the input state. Be certain that you do not accidentally 
#modify the input board variable
def result(action,board):
	#first find empty spot
	row = None
	col = None
	for i in range(len(board)):#row = i
		for j in range(len(board[i])):#col = j
			if board[i][j] == None:
				row = i
				col = j
	#convert to list to change vals
	newBoard = []
	for i in range(len(board)):
		newBoard.append(list(board[i]))
	#switch the value opposite the move direction with None value
	if action == "up":
		newBoard[row][col] = newBoard[row+1][col] #set None space to vlaue below
		newBoard[row+1][col] = None #set the space below to None
	elif action == "down":
		newBoard[row][col] = newBoard[row-1][col]
		newBoard[row-1][col] = None
	elif action == "left":
		newBoard[row][col] = newBoard[row][col+1]
		newBoard[row][col+1] = None
	elif action == "right":
		newBoard[row][col] = newBoard[row][col-1]
		newBoard[row][col-1] = None
	#return the new board
	#convert back to tuples 
	for i in range(len(board)):
		newBoard[i] = tuple(newBoard[i])
	newBoard = tuple(newBoard)
	return newBoard


# PART 3
#Write a function expand that takes a board as input, and outputs a list
#of all states that can be reached in one Action from the given state.
#I had to do this with node as input.
def expand(node):
	newNodesList = [] #list of all new nodes;
	newNode = [] # node to be added to newNodes
	actions = possibleActions(node.board) #get possible actions
	#for each action: get new board, add it and the action to list of child nodes
	for action in actions:
		newNode = Node(result(action,node.board), action, node, node.depth+1)
		newNodesList.append(newNode)

	#return list of all child nodes
	return newNodesList


# PART 4
#Iterative deepening
def iterativeDeepening(initialNode, goalBoard):
	result = None
	actionsList = []
	frontier_size = 1
	for i in range(1,100):#starting at depth = 1 stop at depth = 100
		frontier = [initialNode]
		depth = i
		currentNode = None
		while(len(frontier) != 0):
			frontier_size = getMaxListSize(frontier, frontier_size)
			currentNode = frontier.pop()
			if(currentNode.board == goalBoard):
				result = currentNode
				break
			if(currentNode.depth == depth):
				continue
			else:
				currentNode.children = expand(currentNode)
				for child in currentNode.children:
					frontier.append(child)
			#end while
		if(result):
			print("Depth (from 0): ", depth)
			tmpNode = result
			while(tmpNode.parent):
				actionsList.append(tmpNode.parentMove)
				tmpNode = tmpNode.parent
			break
	actionsList.reverse()
	print("Iterative Deepening:")
	print("Moves: \n", actionsList, "\n")
	print("Max size of frontier: ", frontier_size, "\n")


# PART 5
#Breadth First Search
def breadthFirst(initialNode, goalBoard):
	result = None
	actionsList = []
	frontier = deque([initialNode]) # FIFO queue, right is front
	frontier_size = 1
	reached = set() #set to hold reached nodes
	currentNode = None
	while(len(frontier) != 0):
		frontier_size = getMaxListSize(frontier, frontier_size)
		currentNode = frontier.pop()
		if(currentNode.board == goalBoard):
			result = currentNode
			break
		else:
			currentNode.children = expand(currentNode)
			for child in currentNode.children:
				#pruned repeated states
				if(child.board not in reached):
					reached.add(child.board)
					frontier.appendleft(child)#add to back of queue
		#end while
	if(result):
		tmpNode = result
		while(tmpNode.parent):
			actionsList.append(tmpNode.parentMove)
			tmpNode = tmpNode.parent
	actionsList.reverse()
	print("Breadth-First-Search:")
	print("Moves: \n", actionsList, "\n")
	print("Max Size of frontier: ", frontier_size, "\n")



# PART 6

#heuristic functions
def manhattanDistance(board, goalBoard):
	x1,x2,y1,y2 = 0,0,0,0 # x1,y1 for goalBoard, x2,y2 for board
	tile = 1 #starting value to check
	manhattanDistance = 0
	#find position of tile in board and goalBoard
	while(tile < len(board)**2):
		for row in range(len(board)):
			for col in range(len(board[row])):
				if(goalBoard[row][col] == tile):
					x1 = row
					y1 = col
				if(board[row][col] == tile):
					x2 = row
					y2 = col
		tile += 1
		#get absolute value of difference
		manhattanDistance += abs((x1-x2)) + abs((y1-y2))
	return manhattanDistance


def misplacedTiles(board, goalBoard):
	tiles = 0
	for row in range(len(board)):
		for col in range(len(board)):
			if(goalBoard[row][col] != board[row][col]):
				tiles += 1

	return tiles

def zero(board, goalBoard):
	return 0


#A* (A star) search
def aStar(initialNode, goalBoard, heuristic):
	openSet = set()
	openSet_size = 1
	reached = set()
	result = None
	actionsList = []
	# f(x) = g(x) + h(x)
	openSet.add(initialNode)
	while(result == None):
		openSet_size = getMaxListSize(openSet, openSet_size)
		current = None
		#get node with smalles f(x) value
		for element in openSet:
			if(current == None):
				current = element
				continue
			if(element.f_score < current.f_score):
				current = element
		#if there are no nodes with lower f(x) value, find one thats equal
		if(current == None):
			for element in openSet:
				if(element.f_score == current.f_score):
					current = element
		#remove node with smallest f(x) from openSet
		openSet.remove(current)
		#add board to reached set so we dont expand what we already see
		reached.add(current.board)
		if(current.board == goalBoard):
			result = current
			break
		#expand the current node
		current.children = expand(current)
		for child in current.children:
			#assign f,g,h
			child_g = child.depth
			child_h = heuristic(child.board, goalBoard)
			child.f_score = child_g + child_h
			if(child.board not in reached):
				openSet.add(child)
		if(result):
			break
			
	tmpNode = result
	while(tmpNode.parent):
		actionsList.append(tmpNode.parentMove)
		tmpNode = tmpNode.parent
	actionsList.reverse()
	print("A* (A-Star) Search:")
	print("Heuristic: ", heuristic.__name__)
	print("Moves: \n", actionsList, "\n")
	print("Max size of frontier aka \"openSet\": ", openSet_size, "\n")
###################################

#puzzles
#the board is held in nested tuples
puzzle0 = Node(((3,1,2),(7,None,5),(4,6,8)), None, None, 0)
puzzle1 = Node(((7,2,4),(5,None,6),(8,3,1)), None, None, 0)
puzzle2 = Node(((6,7,3),(1,5,2),(4,None,8)), None, None, 0)
puzzle3 = Node(((None,8,6),(4,1,3),(7,2,5)), None, None, 0)
puzzle4 = Node(((7,3,4),(2,5,1),(6,8,None)), None, None, 0)
puzzle5 = Node(((1,3,8),(4,7,5),(6,None,2)), None, None, 0)
puzzle6 = Node(((8,7,6),(5,4,3),(2,1,None)), None, None, 0)
#goal board
goal = ((None,1,2),(3,4,5),(6,7,8))


# PART 4 TEST
#print("PART 4 TEST: \n")
#iterativeDeepening(puzzle0, goal)

# PART 5 TESTS
#print("PART 5 TEST: \n")
#breadthFirst(puzzle0, goal)
#breadthFirst(puzzle1, goal)

# PART 6.1 TEST
#print("PART 6 TEST: \n")
#aStar(puzzle0, goal, zero)

# PART 6.2 TEST
#print("PART 6.1 TEST: \n")
#aStar(puzzle0, goal, manhattanDistance)
#aStar(puzzle1, goal, manhattanDistance)

# PART 7.1 TEST
#print("PART 7.1 TEST: \n")
#cProfile.run('iterativeDeepening(puzzle0, goal)')
#cProfile.run('breadthFirst(puzzle0, goal)')
#cProfile.run('aStar(puzzle0, goal, manhattanDistance)')

# PART 7.2 TEST
#print("PART 7.2 TEST: \n")
#cProfile.run('aStar(puzzle2, goal, misplacedTiles)')
#cProfile.run('aStar(puzzle2, goal, manhattanDistance)')

# PART 7.3 TEST
#print("PART 7.3 TEST: \n")
#cProfile.run('breadthFirst(puzzle2, goal)')
#cProfile.run('breadthFirst(puzzle3, goal)')
#cProfile.run('breadthFirst(puzzle4, goal)')
#cProfile.run('breadthFirst(puzzle5, goal)')
#cProfile.run('breadthFirst(puzzle6, goal)')

#cProfile.run('aStar(puzzle2, goal, manhattanDistance)')
#cProfile.run('aStar(puzzle3, goal, manhattanDistance)')
#cProfile.run('aStar(puzzle4, goal, manhattanDistance)')
#cProfile.run('aStar(puzzle5, goal, manhattanDistance)')
#cProfile.run('aStar(puzzle6, goal, manhattanDistance)')

##################################
