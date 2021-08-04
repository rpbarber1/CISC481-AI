#Ryan Barber
#CISC 481
#Program 3

import math
import random
import copy

#PART 1

# FORMALIZATION

class State:
    def __init__(self, board, player):
        self.board = board
        self.player = player
#=========================================================

# RETURNS THE PLAYER WHO'S TURN IT IS (1 = WHITE, -1 = BLACK)
def toMove(state):
    return state.player
#=========================================================

# RETURNS SET OF ACTIONS POSSIBLE IN THE CURRENT STATE
#   'action' is a tuple = ("name of action", board row, board col)
def actions(state):
    action_list = list()
    player = toMove(state)
    if(player == -1): #Min turn (black) incrementing i
        for i in range(3):
            for j in range(3):
                if(state.board[i][j] == -1):
                    if(i < 2):
                        if(state.board[i+1][j] == 0):
                            tmp_action = ("advance", i+1, j)
                            action_list.append(tmp_action)
                        if(j > 0):
                            if(state.board[i+1][j-1] == 1):
                                tmp_action = ("capture left", i+1, j-1)
                                action_list.append(tmp_action)
                        if(j < 2):
                            if(state.board[i+1][j+1] == 1):
                                tmp_action = ("capture right",i+1,j+1)
                                action_list.append(tmp_action)
    if(player == 1): #Max turn (White) decrementing i
        for i in range(3):
            for j in range(3):
                if(state.board[i][j] == 1):
                    if(i > 0):
                        if(state.board[i-1][j] == 0):
                            tmp_action = ("advance",i-1,j)
                            action_list.append(tmp_action)
                        if(j > 0):
                            if(state.board[i-1][j-1] == -1):
                                tmp_action = ("capture left", i-1, j-1)
                                action_list.append(tmp_action)
                        if(j < 2):
                            if(state.board[i-1][j+1] == -1):
                                tmp_action = ("capture right",i-1,j+1)
                                action_list.append(tmp_action)
    return action_list
#=========================================================

# RETURNS THE STATE RESULTING FROM AN ACTION
#   'action' is a tuple = ("name of action", board row, board col)
#       board [row,col] is the space that will be moved to
def result(state, action):
    player = toMove(state)
    new_board = copy.deepcopy(state.board)
    new_state = State(new_board,(player*-1))

    if(action[0] == "advance"):
        new_state.board[action[1]][action[2]] = player
        if(player == 1):
            new_state.board[action[1]+1][action[2]] = 0
        else:
            new_state.board[action[1]-1][action[2]] = 0

    if(action[0] == "capture left"):
        new_state.board[action[1]][action[2]] = player
        if(player == 1):
            new_state.board[action[1]+1][action[2]+1] = 0
        else:
            new_state.board[action[1]-1][action[2]+1] = 0

    if(action[0] == "capture right"):
        new_state.board[action[1]][action[2]] = player
        if(player == 1):
            new_state.board[action[1]+1][action[2]-1] = 0
        else:
            new_state.board[action[1]-1][action[2]-1] = 0

    return new_state
#=========================================================

# RETURNS TRUE IF IN A FINAL STATE, FALSE OTHERWISE
def isTerminal(state):
    #check if no possible actions
    if(len(actions(state)) == 0):
        return True
    #check if pawn made it to the other side
    for i in range(3):
        if((state.board[0][i] == 1) or (state.board[2][i] == -1)):
            return True
    return False
#=========================================================

# RETURNS 1 IF WHITE WINS, -1 IF BLACK WINS
#   only called if in terminal statea
def utility(state):
    player = state.player
    #if it's in final state, and it's white's turn, black has won
    if(player == 1):
        return -1
    #if it's in final state, and it's black's turn, white has won
    if(player == -1):
        return 1
#=========================================================


#PART 2

# MINIMAX & POLICY TABLE


class Node:
    def __init__(self, state, parent_action):
        self.state = state
        self.payoff = None
        self.children = []
        self.parent_action = parent_action
#=========================================================

# GIVEN A ROOT NODE, BUILDS A MINIMAX TREE
#   returns node payoff for recusive purpose only
#  the function modifies the root given, no need to return a tree root
#  do:  my_root = Node(...)  ->    buildMinimax(my_root)
def buildMinimax(root):
    #print(root.state.board)
    #check if terminal and return
    if(isTerminal(root.state)):
        root.payoff = utility(root.state)
        return 

    #IF Not Terminal
    
    #get list of actions
    action_list = actions(root.state)

    #add children nodes with possible actions
    for action in action_list:
        root.children.append(Node(result(root.state, action), action))


    #get payoff of children
    child_payoffs = []
    for child in root.children:
        buildMinimax(child)
        child_payoffs.append(child.payoff)

    #print(child_payoffs)
    #set root payoff:
    #if its Max turn: pick payoff with highest value
    #if Min turn: pick payoff with lowest value
    if(root.state.player == 1):
        root.payoff = max(child_payoffs)
    else:
        root.payoff = min(child_payoffs)
#=========================================================

# GIVEN A ROOT NODE OF MINIMAX TREE, BUILDS A POLICY TABLE
#  give root node of minimax tree
#   return policy table: a list of tuples (state,value,action_list)
def buildPolicyTable(table, root):
    #if at a terminal node, return
    if(len(root.children) == 0):
        return

    state = None
    value = None
    action_list = []

    state = root.state
    value = root.payoff
    for child in root.children:
        if(child.payoff == value):
            action_list.append(child.parent_action)

    entry = (state,value,action_list)
    table.append(entry)

    for child in root.children:
        buildPolicyTable(table, child)
#=========================================================

#PART 3

class Neuron:
    def __init__(self,parent_size):
        self.parents = []
        self.children = []
        self.w0 = random.random()
        self.weights = [random.random()]*parent_size
        self.inputs = [0]*parent_size
        self.output = 0
        self.activation = "relu"
#=========================================================

# BUILD A NETWORK
#   all hidden layers use relu
#   output layer uses sigmoid
# give number of inputs, outputs, hidden layers, hidden units
#   return the first hidden layer (one that receivs inputs)
def buildNetwork(inputs, outputs, hidden_layers, hidden_units):

    first_layer = [] #layer that recieves inputs (first hidden layer)

    #if 0 hidden layers, first_layer is output layer
    if(hidden_layers == 0):
        for i in range(outputs):
            first_layer.append(Neuron(inputs))
        return first_layer


    for i in range(hidden_units):
        first_layer.append(Neuron(inputs))


    #create hidden layers
    current_layer = first_layer
    for i in range(hidden_layers-1): #do the below to make each hidden layer after first
        next_layer = []
        for j in range(hidden_units): #make a new unit
            new_unit = Neuron(len(current_layer))
            for k in range(len(current_layer)): #add each unit of current layer to parents of new unit (next level)
                new_unit.parents.append(current_layer[k])
                current_layer[k].children.append(new_unit)
            next_layer.append(new_unit)
        current_layer = next_layer

    #create ouput layer 
    for i in range(outputs):
        output_layer = []
        new_unit = Neuron(len(current_layer))
        new_unit.activation = "sigmoid"
        for j in range(hidden_units):
            new_unit.parents.append(current_layer[j])
            current_layer[j].children.append(new_unit)
        output_layer.append(new_unit)
    
    return first_layer
#=========================================================


#PART 4

# RUN THE NETWORK ONCE THROUGH
# give network instance and input vector
#   return the network instance 
def classify(network, input_vector):
    first_layer = network

    output_vector = []

    #set inputs in first layer
    for unit in first_layer:
        unit.inputs = input_vector

    tmp = first_layer

    while(len(tmp) != 0):
        next_input = [] #will be composed of outputs of tmp[i]

        for i in range(len(tmp)): #for each unit in the layer
            #get sumnation sigma(w * x)
            sum_of_inputs = tmp[i].w0 * -1
            for j in range(len(tmp[i].inputs)):
                sum_of_inputs += (tmp[i].inputs[j])*(tmp[i].weights[j])

            #get output of each unit based on activation function
            if(tmp[i].activation == "relu"):
                if(sum_of_inputs < 0):
                    tmp[i].output = 0
                else:
                    tmp[i].output = 1
            else:
                tmp[i].output = 1 / (1 + math.exp(-(sum_of_inputs)))

            next_input.append(tmp[i].output)

        #set inputs for children
        for child in tmp[0].children:
            child.inputs = next_input

        #set tmp to be set of children
        #this works because all neurons have the same children in the same order
        tmp = tmp[0].children

        #set output vector for when we reach the last layer
        output_vector = next_input

    return [first_layer, output_vector]
#=========================================================


# PART 5

# UPDATE THE WEIGHTS OF THE NETWORK THROUGH BACKPROPIGATION
# give network instance and vector of expected outputs
#   return the netowrk instance
def updateWeights(network, expected_vector):
    #get last layer
    tmp = network
    while(len(tmp[0].children) != 0):
        tmp = tmp[0].children

    #now tmp = output layer

    eta = 0.5 #learning rate
    delta_child_current = [] #keep track of for next layers

    #delta weight ji = eta * (yi - oi) * relu' * xji
    #OUTPUT LAYERS - based on sigmoid function
    for i in range(len(tmp)): #for each output unit

        deltaJ = (expected_vector[i] - tmp[i].output) * tmp[i].output * (1 - tmp[i].output)
        delta_child_current.append(deltaJ)

        #update weights
        for j in range(len(tmp[i].weights)): #for each weight in unit 
            tmp[i].weights[j] += eta * deltaJ * tmp[i].inputs[j]
        tmp[i].w0 += eta * deltaJ * -1    #w0  (x0 input is always -1)

    #move tmp back a layer
    tmp = tmp[0].parents

    #HIDDEN LAYERS - based on relu function
    delta_child_next = []
    while(len(tmp) != 0): #repeat for each hidden layer
        for i in range(len(tmp)): # for each unit

            # sigma(wj * delta_current[j])
            sumnation_children = 0
            for j in range(len(tmp[0].children)): #for each child
                sumnation_children += tmp[i].children[j].weights[i] * delta_child_current[j]

                relu_prime = 0
            if(tmp[i].output < 0):
                relu_prime = 0
            else:
                relu_prime = 1

            deltaJ = relu_prime * sumnation_children
            delta_child_next.append(deltaJ)

            for k in range(len(tmp[0].weights)): #for each weight in unit
                tmp[i].weights[k] += eta * deltaJ * tmp[i].inputs[k]
            tmp[i].w0 += eta * deltaJ * -1

        #reset delta lists for next layer back
        delta_child_current = delta_child_next
        delta_child_next = []

        #move tmp one layer back
        tmp = tmp[0].parents

    return network
#=========================================================


# PART 6

# First we have to get the training set [[input-1, output-1],...,[input-i, output-i]]

# GET TRAINING DATASET FROM THE POLICY TABLE
#  give policy table
#   return training set of the form [[input-1, output-1],...,[input-i, output-i]]
def getTrianingSet(policy_table):
    training_set = []

    #policy table: a list of tuples (state,value,action_list)

    for i in range(len(policy_table)):
        #get tmp input [player, board]
        in_tmp = [policy_table[i][0].player]
        in_board = policy_table[i][0].board

        #turn nested lists in to list of bits [[0,1,0]] -> [0,1,0]
        for j in range(3):
            for k in range(3):
                in_tmp.append(in_board[j][k])

        #get tmp output [board]: always set to the first action in the list
        #   
        out_tmp = [0]*9
        out_tmp[(3*policy_table[i][2][0][1])+ ((policy_table[i][2][0][2]))] = 1

        training_set.append([in_tmp, out_tmp])

    return training_set
#=========================================================

# TRAIN NETWORK ON RANDOM PERMUTATIONS OF GIVEN TRAINING DATASET
#  give network instance and training data
#   NO return, this modifies the given network instance
def train(network, training_set, epochs):
    #EPOCHS
    for i in range(epochs):
        random.shuffle(training_set)
        for j in range(len(training_set)):
            my_return = classify(network, training_set[j][0])
            one_update = updateWeights(network, training_set[j][1])
#=========================================================

# TEST NETWORK ON POLICY TABLE GENERATED FROM PART 2
#  give network and training list
#   return percentage of correct matches to training list output
def test(network, training_list, accuracy_threshold):
    accuracy = 0
    correct = 0
    wrong = 0
    for i in range(len(training_list)):
        result = classify(network, training_list[i][0])[1]
        for j in range(len(result)):
            if(result[j] > accuracy_threshold):
                result[j] = 1
            if(result[j] <= 0.1):
                result[j] = 0
            else:
                result[j] = 1
        
        if(result == training_list[i][1]):
            correct += 1
        else:
            wrong += 1

    accuracy = correct / (correct + wrong)

    return accuracy


#Used to print the minimax tree
def printTree(root,i):
    for j in range(i):
        print("\t",end="")
    print(root.state.board, root.parent_action)
    for child in root.children:
        printTree(child,i+1)
#=========================================================
#=========================================================

#Initail Board
test_board = [ [-1,-1,-1],[0,0,0],[1,1,1] ]

#Inintal State; Max = white = 1  is the first to move
test_state = State(test_board, 1)

#Root node to generate minimax tree
root_node = Node(test_state,None)

#Build Minimax tree
buildMinimax(root_node)

#Build Policy table
test_table = []
buildPolicyTable(test_table, root_node)

#Build training data
# I am formatting the data to be passed into the netowrk
training_list = getTrianingSet(test_table)

#Build Networks
# Description of the below network:
#   10 INPUTS
#   9 OUTPUTS
#   1 HIDDEN LAYER
#   10 UNITS PER HIDDEN LAYER
test_network_3 = buildNetwork(10,9,1,10)

#Test Network


# THIRD TEST: 1000 EPOCHS
train(test_network_3, training_list,1000)
print("\n1000 Epochs:")
acc = test(test_network_3, training_list, 0.89999)
print("\tAccuracy Threshold = 0.89999\n\t\t",acc)
acc = test(test_network_3, training_list, 0.94999)
print("\tAccuracy Threshold = 0.94999\n\t\t",acc)
acc = test(test_network_3, training_list, 0.98999)
print("\tAccuracy Threshold = 0.98999\n\t\t",acc)
print("==========================================\n")