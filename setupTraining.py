from math import *
from random import *


def main():
  outfile = open('balance-Inputs.dat', 'w')
  in2 = open('test-set.dat', 'w')
  problemType = open('problemType.dat', 'w')
#writing training set
  easy = 0
  medium = 0
  hard = 0
  easyNums = []
  mediumNums = []
  hardNums = []
  for i in range(1000):
    num = randint(0,2)
    if num == 0:
      string = generateEasy()
      easy+=1
      easyNums.append((i, easy))
      problemType.write("e\n")
      outfile.write(string)
    elif num == 1:
      string = generateMedium()
      medium+=1
      easyNums.append((i, medium))
      problemType.write("m\n")
      outfile.write(string)
    elif num == 2:
      string = generateHard()
      hard+=1
      easyNums.append((i, hard))
      problemType.write("h\n")
      outfile.write(string)

#writing test set
  for i in range(1000):
    num = randint(0,2)
    if num == 0:
      string = generateEasy()
      in2.write(string)
    elif num == 1:
      string = generateMedium()
      in2.write(string)
    elif num == 2:
      string = generateHard()
      in2.write(string)
  
  outfile.close()
  in2.close()
  
  print "Easy %d" %(easy)
  print "Medium %d" %(medium)
  print "Hard %d" %(hard)

  infile = open('balance-Inputs.dat', 'r')
  in2 = open('test-set.dat', 'r')

  outfile = open('Output-Targets.dat', 'w')
  out2 = open('test-targets.dat', 'w')




  allNums = []
  for i in range(1000):
    string = infile.readline()
    nums = []
    #split line into list of individual digits
    number = string.split(" ")
    for j in range(8):
      if number[j].isdigit():
        nums.append(int(number[j]))
    #if (nums[8] == '\n'):
     # nums.remove('\n')
    allNums.append(nums)

####Here we find the answer####
  for i in range(1000):
  # give different weights based on the distance from center
    firstfour = allNums[i][0]*4 + allNums[i][1]*3 + allNums[i][2]*2 + allNums[i][3]*1
    secondfour = allNums[i][4]*1 + allNums[i][5]*2 + allNums[i][6]*3 + allNums[i][7]*4
    if firstfour == secondfour:
      outfile.write("0 1 0\n")
    elif firstfour > secondfour:
      outfile.write("1 0 0\n")
    elif firstfour < secondfour:
      outfile.write("0 0 1\n")


####Duplication for test targets####
  allNums = []
  for i in range(1000):
    string = in2.readline()
    nums = []
    # for i in range(8):
    number = string.split(" ")
    for j in range(8):
      if number[j].isdigit():
        nums.append(int(number[j]))
    #if (nums[8] == '\n'):
     # nums.remove('\n')
    allNums.append(nums)
  for i in range(1000):
    firstfour = allNums[i][0]*4 + allNums[i][1]*3 + allNums[i][2]*2 + allNums[i][3]*1
    secondfour = allNums[i][4]*1 + allNums[i][5]*2 + allNums[i][6]*3 + allNums[i][7]*4
  # write based on balance or left/right heavier
    if firstfour == secondfour:
      out2.write("0 1 0\n") #balanced
    elif firstfour > secondfour:
      out2.write("1 0 0\n") #left leaning
    elif firstfour < secondfour:
      out2.write("0 0 1\n") #right leaning


#have it return a string, representing an easy problem    
def generateEasy():
  choice = randint(0,1)  
  if choice == 0:
    return balanceProblem()
  else:
    return weightProblem()
  
 
def balanceProblem():
  num1 = randint(1,3)   
  position1 = randint(0,3)
  position2 = 7 - position1
  toReturn = ""
  for i in range(8):
    if i == position1 or i == position2:
      toReturn += str(num1) + " "
    else:
      toReturn += "0 "
  #toReturn += "e "
  toReturn += "\n"
  
  return toReturn

def weightProblem():
  
  num1 = randint(1,3)
  num2 = randint(1,3)
  while num1 == num2:
    num2 = randint(1,3)
  position1 = randint(0,3)
  position2 = 7 - position1
  toReturn = ""
  for i in range(8):
    if i == position1:
      toReturn += str(num1) + " "
    elif i == position2:
      toReturn += str(num2) + " "
    else:
      toReturn += "0 "
  #toReturn += "e"
  toReturn += "\n"
  return toReturn
  
def generateMedium():
  num = randint(0,1)
  if num == 0:
    return distanceProblem()
  else:
    return conflictWeight()


#helper function for generate medium
def distanceProblem():

  num1 = randint(1,3)   
  position1 = randint(0,3)
  position2 = randint(0,3)
  while position1 == position2:
    position2 = randint(0,3) #make sure position1 wont equal position2
  position2 = 7- position2

  toReturn = ""
  for i in range(8):
    if i == position1:
      toReturn += str(num1) + " "
    elif i == position2:
      toReturn += str(num1) + " "
    else:
      toReturn += "0 "
  
  #toReturn += "m"
  toReturn += "\n"
  
  return toReturn

def conflictWeight():

  heavy = randint(0,3)
  light = randint(0,3)
  f = randint(0,3)
  c = randint(0,3)
  fweight = 4-f
  cweight = 4-c
  while (light*fweight > heavy*cweight):
    heavy = randint(0,3)
    light = randint(0,3)
    f = randint(0,3)
    c = randint(0,3)
    fweight = 4-f
    cweight = 4-c
  decider = randint(0,1)
  if decider == 0:
    c = 7- c
  else:
    f = 7-f
  toReturn = ""
  for i in range(8):
    if i == f:
      toReturn += str(light) + " "
    elif i == c:
      toReturn += str(heavy) + " "
    else:
      toReturn += "0 "
  
  #toReturn += "m "
  toReturn += "\n"
  return toReturn

def generateHard():

  toReturn = ""
  for i in range(8):
    num = randint(0,3)
    toReturn += str(num) + " "
  
  #toReturn += "h "
  toReturn +=  "\n"
  return toReturn
    
    
main()

    
    



  








