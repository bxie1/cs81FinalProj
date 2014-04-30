from pyrobot.brain.conx import *
from pyrobot.system.log import * 
import matplotlib.pyplot as plt

import random
# create a basic feedforward backpropagation network
n = Network()

# add layers in the order they will be connected
n.addLayer('input', 8)        # input layer has eight units
n.addLayer('hidden', 5)
n.addLayer('output', 3)       # output layer has three units
n.connect('input', 'hidden', 'output')  # connect the layers together

# learning rate
n.setEpsilon(0.15)
# how often the network reports its total error during training
n.setReportRate(1)
# how close an output value has to be to the target to count as correct
n.setTolerance(0.1)

# specify the dataset to use for learning
n.loadInputsFromFile('balance-Inputs.dat')
n.loadTargetsFromFile('Output-Targets.dat')

"""
LISA's Pseudo Code
import random
ls = range(10)
print ls # [0, 1, ... , 9]
random.shuffle(ls)
print ls # [8, 7, 0, 9 ... ]

put in "step"
n.step(input = ls, output = ls)
"""

print "BAL network is set up"
log = Log(name = 'balLog')
currentBest = 0
numFullCorrect = 0

ins = n.inputs #list of all inputs
outs = n.targets

ls = range(1000) #indexing for shuffling

#filling a list with the problem types
problems = []
infile = open('problemType.dat', 'r')
for i in range(1000):
  probType = infile.readline()
  toAdd = probType.strip('\n')
  problems.append(toAdd)


outEasy = open('EasyError.dat', 'w')
outMedium = open('MediumError.dat', 'w')
outHard = open('HardError.dat', 'w')

firstFiveEasyVals = []
firstFiveMedVals = []
firstFiveHardVals = []

firstFiveEasyPcorrect = []
firstFiveMedPcorrect = []
firstFiveHardPcorrect = []

easyVals = []
mediumVals = []
hardVals = []

easyPcorrect = []
mediumPcorrect = []
hardPcorrect = []

for i in range(500):
      #SWEEP replaced with Step
      #n.inputs is the list that we loaded
      random.shuffle(ls)
      tssError = 0
      totalCorrect = 0
      totalCount = 0 
      totalPCorrect = 0
      totalEasy = 0
      totalMedium = 0
      totalHard = 0
      countHundred = 0
      easyError = 0
      mediumError = 0
      hardError = 0
      
      easyCorrect = 0
      mediumCorrect = 0
      hardCorrect = 0

      firstFiveEasyError = 0
      firstFiveMediumError = 0
      firstFiveHardError = 0
      
      for j in range(1000): #range size of inputs
         rindex = ls[j]
         countHundred += 1
         error, correct, count, PCorrect = n.step(input=ins[rindex], output=outs[rindex])
        
         if problems[rindex] == 'e':
           totalEasy +=count
           easyError += error
           firstFiveEasyError += error
           easyCorrect += correct
         if problems[rindex] == 'm':
           totalMedium += count
           mediumError += error
           firstFiveMediumError += error
           mediumCorrect += correct
         if problems[rindex] == 'h':
           totalHard += count
           hardError += error
           firstFiveHardError += error
           hardCorrect += correct
         if i < 5:
           if countHundred == 100:
             countHundred = 0
             easyPerCorrect = (easyCorrect*0.1)/ (totalEasy*0.1)
             mediumPerCorrect = (mediumCorrect*0.1) / (totalMedium*0.1)
             hardPerCorrect = (hardCorrect*0.1) / (totalHard*0.1)
             firstFiveEasyVals.append(firstFiveEasyError)
             firstFiveMedVals.append(firstFiveMediumError)
             firstFiveHardVals.append(firstFiveHardError)
             firstFiveEasyPcorrect.append(easyPerCorrect)
             firstFiveMedPcorrect.append(mediumPerCorrect)
             firstFiveHardPcorrect.append(hardPerCorrect)
             firstFiveEasyError = 0
             firstFiveMediumError = 0
             firstFiveHardError = 0
             
             



           
         tssError += error
         totalCorrect += correct
         totalCount += count
         #totalPCorrect += PCorrect[j]
      easyPerCorrect = (easyCorrect*0.1)/ (totalEasy*0.1)
      mediumPerCorrect = (mediumCorrect*0.1) / (totalMedium*0.1)
      hardPerCorrect = (hardCorrect*0.1) / (totalHard*0.1)
      
      #writing epoch and error for dif problem types
      outEasy.write("%d %d\n" %(i, easyError))
      outMedium.write("%d %d\n" %(i, mediumError))
      outHard.write("%d %d\n" %(i, hardError))
      easyVals.append(easyError)
      mediumVals.append(mediumError)
      hardVals.append(hardError)

      easyPcorrect.append(easyPerCorrect)
      mediumPcorrect.append(mediumPerCorrect)
      hardPcorrect.append(hardPerCorrect)

      
      
      
         
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
      if numFullCorrect == 5:
         break
print "Best percent correct during training was", currentBest

fig1 = plt.figure(1)
fig1.suptitle('TSS Errors over time', fontsize=14, fontweight='bold')
ax = fig1.add_subplot(111)
fig1.subplots_adjust(top=0.85)

ax.set_xlabel('Epoch')
ax.set_ylabel('TSS Error')


ax.text(.85, 0.90, '--- Easy',
        verticalalignment='top', horizontalalignment='right',
        transform=ax.transAxes,
        color='green', fontsize=12)

ax.text(.85, 0.85, '--- Medium',
        verticalalignment='top', horizontalalignment='right',
        transform=ax.transAxes,
        color='blue', fontsize=12)

ax.text(.85, 0.80, '--- Hard',
        verticalalignment='top', horizontalalignment='right',
        transform=ax.transAxes,
        color='red', fontsize=12)

plt.plot(range(len(easyVals)),easyVals, 'g-', label='easy', linewidth=1)
plt.plot(range(len(mediumVals)), mediumVals, 'b-', label = 'medium', linewidth=1)
plt.plot(range(len(hardVals)), hardVals, 'r-', label = 'hard', linewidth=1)
plt.axis([0, i+5, -10, 300])
#plt.show()
plt.savefig("tssErrors.png")

fig2 = plt.figure(2)
fig2.suptitle('Percent Correct over time', fontsize=14, fontweight='bold')

ax = fig2.add_subplot(111)
fig2.subplots_adjust(top=0.85)

ax.text(.85, 0.50, '--- Easy',
        verticalalignment='top', horizontalalignment='right',
        transform=ax.transAxes,
        color='green', fontsize=12)

ax.text(.85, 0.45, '--- Medium',
        verticalalignment='top', horizontalalignment='right',
        transform=ax.transAxes,
        color='blue', fontsize=12)

ax.text(.85, 0.40, '--- Hard',
        verticalalignment='top', horizontalalignment='right',
        transform=ax.transAxes,
        color='red', fontsize=12)



ax.set_xlabel('Epoch')
ax.set_ylabel('% Correct')


plt.plot(range(len(easyPcorrect)),easyPcorrect, 'g-', label='easy', linewidth=1)
plt.plot(range(len(mediumPcorrect)), mediumPcorrect, 'b-', label = 'medium', linewidth=1)
plt.plot(range(len(hardPcorrect)), hardPcorrect, 'r-', label = 'hard', linewidth=1)
plt.axis([0, i+5, 0, 1.2])
plt.savefig("PerCorrect.png")



fig1 = plt.figure(3)
fig1.suptitle('TSS Errors Over First 5 Generations', fontsize=14, fontweight='bold')
ax = fig1.add_subplot(111)
fig1.subplots_adjust(top=0.85)

ax.set_xlabel('Steps (in Hundreds aka first five generations)')
ax.set_ylabel('TSS Error')


ax.text(.85, 0.50, '--- Easy',
        verticalalignment='top', horizontalalignment='right',
        transform=ax.transAxes,
        color='green', fontsize=12)

ax.text(.85, 0.45, '--- Medium',
        verticalalignment='top', horizontalalignment='right',
        transform=ax.transAxes,
        color='blue', fontsize=12)

ax.text(.85, 0.40, '--- Hard',
        verticalalignment='top', horizontalalignment='right',
        transform=ax.transAxes,
        color='red', fontsize=12)

plt.plot(range(len(firstFiveEasyVals)),firstFiveEasyVals, 'g-', label='easy', linewidth=1)
plt.plot(range(len(firstFiveMedVals)), firstFiveMedVals, 'b-', label = 'medium', linewidth=1)
plt.plot(range(len(firstFiveHardVals)), firstFiveHardVals, 'r-', label = 'hard', linewidth=1)
plt.axis([0, 60, 0, 50])
#plt.show()
plt.savefig("firstFiveTSSError.png")

fig1 = plt.figure(4)
fig1.suptitle('% Correct Over First 5 generations', fontsize=14, fontweight='bold')
ax = fig1.add_subplot(111)
fig1.subplots_adjust(top=0.85)

ax.set_xlabel('Steps (in Hundreds aka first five generations)')
ax.set_ylabel('% Correct')


ax.text(.85, 0.50, '--- Easy',
        verticalalignment='top', horizontalalignment='right',
        transform=ax.transAxes,
        color='green', fontsize=12)

ax.text(.85, 0.45, '--- Medium',
        verticalalignment='top', horizontalalignment='right',
        transform=ax.transAxes,
        color='blue', fontsize=12)

ax.text(.85, 0.40, '--- Hard',
        verticalalignment='top', horizontalalignment='right',
        transform=ax.transAxes,
        color='red', fontsize=12)
plt.plot(range(len(firstFiveEasyPcorrect)),firstFiveEasyPcorrect, 'g-', label='easy', linewidth=1)
plt.plot(range(len(firstFiveMedPcorrect)), firstFiveMedPcorrect, 'b-', label = 'medium', linewidth=1)
plt.plot(range(len(firstFiveHardPcorrect)), firstFiveHardPcorrect, 'r-', label = 'hard', linewidth=1)

plt.axis([0, 60, 0, 1.2])
#plt.show()
plt.savefig("firstFive%correct.png")


plt.close()





"""for i in range(min(len(easyVals), len(mediumVals), len(hardVals))):
  x = easyVals[i][0]
  y1 = easyVals[i][1]
  y2 = mediumVals[i][1]
  y3 = hardVals[i][1]
  plt.plot(x,y1, x, y2, x, y3)
  #plt.plot(x, y2, 'r')
  #plt.plot(x, y3, 'g')
  #plt.show()
"""
