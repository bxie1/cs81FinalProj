from pyrobot.brain import Brain
from pyrobot.brain.conx import *
from pyrobot.system.log import * 
from time import *

# create a basic feedforward backpropagation network
n = Network()
n.addLayers(8,5,3)
n.loadWeightsFromFile("balance-net.wts")

#outfile = open('balance-Inputs.dat', 'r')
#in2 = open('test-set.dat', 'r')

# specify the dataset to use for testing
n.loadInputsFromFile('test-set.dat')
n.loadTargetsFromFile('test-targets.dat')


print "test network is set up"
log = Log(name = 'testLog')
currentBest = 0
for i in range(1):
      tssError, totalCorrect, totalCount, totalPCorrect = n.sweep()   
      correctpercent = (totalCorrect*0.1) / (totalCount*0.1) 
      log.writeln( "Epoch # "+ str(i)+ " TSS ERROR: "+ str(tssError)+
                   " Correct: "+ str(totalCorrect)+ " Total Count: "+
                   str(totalCount)+ " %correct = "+ str(correctpercent))
      # Whenever the network improves over previous best, save weights
      """
      if currentBest < correctpercent: 
         n.saveWeightsToFile("balance-net.wts") 
         currentBest = correctpercent
      
      if (correctpercent == 1.0):
         break;
      """
