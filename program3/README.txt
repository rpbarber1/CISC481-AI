Ryan Barber
CICS 481
Program 3

My code runs slow. Sorry.


As per the recomendation in class, I used sigmoid everywhere.
    I used relu as hidden layer activations but was getting nonsense results.
    I have submitted the program with relu as hidden layer activation, however
    I do not count that as my working submission.



SUMMARY:
        I Start with a inital State composed of inital board and player value.
    I then use the inital state to generate a Minimax tree. Then I generate the
    policy table with the resulting tree. I then generate the training_set. This
    is a list with the data from the policy table formated for the network to
    read. Next, I build the network. Now I train the network by feeding random
    permutations of the training_set for X number of epochs. For testing, I
    compare the output of the network to the output of the training set. I
    set the accuracy threshold to 3 different levels (see code output).

    Minimax Tree:
        I start with inital state as root node. First check if state is termianl.
    If yes, set payoff to utility of the state. If no, generate possible acitons
    from the current state then create children with call to result(). Then set
    current node's payoff to min or max of child payoffs.

    Policy table:
        Entry into table: current node state, current node payoff, list of acitons
    whose payoff is = parent payoff. Continue down tree in depth first search
    adding entries to list. 

    Generate Training Set: [[input list], [output list]]
        Since the network takes a list of number and my board is represented by a
    nested list, I must format my data in the policy table to be not nested.
    
        The input list is as specified in the writeup; a list of 10 numbers, one
    for the player, 9 for the board in row major order.

        The output list is 9 numbers representing the board in row major order.
    All the numbers are 0 except the cell where the pawn should be moved.

    Network:
        The network is made using the Neuron class. Each Neuron has a list of
    parents and children. The parents are the list of units in the previous layer.
    The children are a list of units in the next layer. Therefore the first layer
    has no parents and the last (output) layer has no children. For each unit
    in a layer, the units have the same list of parents and children in the same
    order.



TESTING:

    Let the code run, it may be a bit slow.

    I test on the training_set (generated by policy table)

    I run 3 sets of tests:
        500 Epochs:
            accuracy thresholds: 0.8999, 0.94999, 0.98999
        750 Epochs:
            accuracy thresholds: 0.8999, 0.94999, 0.98999
        1000 Epochs:
            accuracy thresholds: 0.8999, 0.94999, 0.98999

    What is accuracy?
        I take the sigmoid output and set the value to 1 if >= the threshold.
    If the ouput <= 0.1 I set it to 0, else 1. If the resulting list is the
    same as the output list, it's correct, else its wrong. Then I caculate
    the accuracy = correct / (correct+wrong)



