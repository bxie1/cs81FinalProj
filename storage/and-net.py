from pyrobot.brain.conx import *

# create a basic feedforward backpropagation network
n = BackpropNetwork()

# add layers in the order they will be connected
n.addLayer('input', 2)        # input layer has two units
n.addLayer('output', 1)       # output layer has one unit
n.connect('input', 'output')  # connect the layers together

# learning rate
n.setEpsilon(0.5)
# how often the network reports its total error during training
n.setReportRate(1)
# how close an output value has to be to the target to count as correct
n.setTolerance(0.1)

# specify the dataset to use for learning
n.loadInputsFromFile('inputs.dat')
n.loadTargetsFromFile('and-targets.dat')

print "AND network is set up"

# Type the following at the python prompt:
#
# >>> n.printWeights('input', 'output')
# >>> n.showPerformance()
# >>> n.train()
# >>> n.printWeights('input', 'output')
# >>> n.showPerformance()

