# brain to collect data for offline learning

from pyrobot.brain import Brain
from pyrobot.brain.conx import *
from time import *
from random import *
def saveListToFile(ls, file):
    for item in ls:
        file.write(str(item) + " ")
    file.write("\n")

class CollectDataBrain(Brain):
    """
    This brain collects data from a hand-coded controller and saves
    the sensor readings and motor commands to separate files.  This
    data can then be used to train a neural network to control a
    robot.

    NOTE: Data must be scaled before used with a neural network.  For
    networks in pyrobot, data must be scaled between 0 and 1.
    """
    def setup(self):
        self.counter = 1
        self.datafile1 = open("sensorInputs.dat", "w")
        self.datafile2 = open("motorTargets.dat", "w")
        self.maxvalue = self.robot.range.getMaxvalue()

    def determineMove(self, dist=1):
        """
        Teacher attemps to teach photoTaxis behavior for robot.
        Returns an appropriate translate and rotate value given
        the current sensor readings.
        """
        leftSensor = self.robot.light[0][0].value
        rightSensor = self.robot.light[0][1].value
        #set bounds for random reposition.
        x = (random()+.1) * 8
        y = (random()+.1) * 8
        o = random() * 6.28
        if (leftSensor + rightSensor)> 1.6:
          self.robot.simulation[0].setPose("RedPioneer", x, y, o)
          return [0, 0]
        elif (leftSensor > 0.025 and leftSensor > rightSensor):
          return [.4, .4]
        elif (rightSensor > 0.025 and rightSensor > leftSensor):
          return [.4, -.4]
        else:
          return [0, .4]

    def scaleSensor(self, val):

        """
        Normalizes the sonar sensor value.
        """
        x = val / self.maxvalue
        if x > 1:
            return 1
        else:
            return x

    def scaleMotor(self, val):
        """
        Given motor values between -0.5 and +0.5, puts them in the
        range 0 to 1.
        """
        return min(val + 0.5, 1.0)

    def step(self):
        """
        Collects data for 1000 steps.
        """

        leftSensor = self.robot.light[0][0].value
        rightSensor = self.robot.light[0][1].value

        translate, rotate = self.determineMove()
        if self.counter > 1000:
            self.move(0,0)
        elif self.counter == 1000:
            self.datafile1.close()
            self.datafile2.close()
            print "done collecting data"
        else:
            if self.counter % 100 == 0:
                print "move", self.counter
            saveListToFile([leftSensor,
                            rightSensor],
                           self.datafile1)
            saveListToFile([self.scaleMotor(translate),
                            self.scaleMotor(rotate)],
                           self.datafile2)
            self.move(translate, rotate)
        self.counter += 1

def INIT(engine):
    return CollectDataBrain('CollectDataBrain', engine)
