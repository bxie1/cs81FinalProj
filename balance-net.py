from pyrobot.brain.conx import *
from pyrobot.system.log import * 
# create a basic feedforward backpropagation network
n = Network()

# add layers in the order they will be connected
n.addLayer('input', 8)        # input layer has eight units
n.addLayer('hidden', 5)
n.addLayer('output', 3)       # output layer has three units
n.connect('input', 'hidden', 'output')  # connect the layers together

# learning rate
n.setEpsilon(0.2)
# how often the network reports its total error during training
n.setReportRate(1)
# how close an output value has to be to the target to count as correct
n.setTolerance(0.1)

# specify the dataset to use for learning
n.loadInputsFromFile('balance-Inputs.dat')
n.loadTargetsFromFile('Output-Targets.dat')

print "BAL network is set up"
log = Log(name = 'balLog')
currentBest = 0
numFullCorrect = 0
for i in range(500):
      tssError, totalCorrect, totalCount, totalPCorrect = n.sweep()   
      correctpercent = (totalCorrect*0.1) / (totalCount*0.1) 
      log.writeln( "Epoch # "+ str(i)+ " TSS ERROR: "+ str(tssError)+
                   " Correct: "+ str(totalCorrect)+ " Total Count: "+
                   str(totalCount)+ " %correct = "+ str(correctpercent))
      # Whenever the network improves over previous best, save weights
      if currentBest < correctpercent: 
         n.saveWeightsToFile("balance-net.wts") 
         currentBest = correctpercent
      if (correctpercent == 1.0):
         numFullCorrect += 1
      if numFullCorrect == 20:
         break
print "Best percent correct during training was", currentBest
