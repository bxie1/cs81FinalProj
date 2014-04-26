from pyrobot.brain.conx import * 
from pyrobot.system.log import * 
  
def setFromFile(filename, delim = ' '):
   """
   Read in data from an existing file.  Each pattern should be separated
   by a newline and each item of data should be separated by the given
   delimiter (the default is a space).
   """
   fp = open(filename, "r") 
   data = []
   for line in fp:
      linedata = [float(x) for x in line.strip().split(delim)] 
      data.append(linedata)
   fp.close()
   print "length of data array is", len(data)
   return data 

def main():
   """
   Train a neural network on the collected data.  Log the progress and
   save the weights whenever the network's performance improves over
   its previous best.
   """
   # Create the network 
   n = Network() 
   n.addLayers(2,4,3,2) 
   # Set learning parameters 
   n.setEpsilon(0.3) 
   n.setMomentum(0.0) 
   n.setTolerance(0.05) 
   # set inputs and targets from collected data set 
   n.setInputs(setFromFile('sensorInputs.dat')) 
   n.setTargets(setFromFile('motorTargets.dat')) 
   # Logging 
   log = Log(name = 'photoTaxis')
   currentBest = 0 
   for i in range(1000):
      tssError, totalCorrect, totalCount, totalPCorrect = n.sweep()   
      correctpercent = (totalCorrect*0.1) / (totalCount*0.1) 
      log.writeln( "Epoch # "+ str(i)+ " TSS ERROR: "+ str(tssError)+
                   " Correct: "+ str(totalCorrect)+ " Total Count: "+
                   str(totalCount)+ " %correct = "+ str(correctpercent))
      # Whenever the network improves over previous best, save weights
      if currentBest < correctpercent: 
         n.saveWeightsToFile("photoTaxis.wts") 
         currentBest = correctpercent 
   print "Best percent correct during training was", currentBest
   
main()
