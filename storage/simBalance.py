"""Graphics stuff"""
from graphics import *
from time import *
from random import*

def main():

  w = 600
  h = 400
  textpt = Point(300,50)
  win = GraphWin("Simulation", w, h)
  message = Text(textpt,"Click to continue")
  message.setFill("Black")
  message.draw(win)
  win.getMouse()

  #draw bottom triangle

  pt1 = Point(150, 400)
  pt2 = Point(300, 300)
  pt3 = Point(450, 400)

  triangle = Polygon(pt1, pt2, pt3)
  triangle.setFill("white")
  triangle.draw(win)

  #draw rectangle on top

  pt4 = Point(150, 250)
  pt5 = Point(450, 300)
  rect = Rectangle(pt4, pt5)
  rect.setFill("blue")
  rect.draw(win)

  #place rectangle on bar

  pt6 = Point(200,200)
  pt7 = Point(250,250)
  weight = Rectangle(pt6, pt7)
  weight.setFill("red")
  weight.draw(win)
  
  center = weight.getCenter()
  y = center.getY()
  x = center.getX()
  offsety = 0
  offsetx = 0
  for i in range(1000):
    center = weight.getCenter()
    y = center.getY()
    x = center.getX()
    pt4 = Point(150+offsetx, 250-offsety)
    pt5 = Point(450+offsetx, 300-offsety)
    rect = Rectangle(pt4, pt5)
    rect.setFill("blue")
    rect.draw(win)
    if y < 250 and y > 200:
      weight.move(0, 1.25)
      sleep(.01)
      offsety +=1
    if x < 250 and x > 200:
      weight.move(-1.25, 0)
      sleep(.01)
      offsetx -= 1

    

  win.getMouse()


########


main()


  
