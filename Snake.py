from graphics import *
import time
import random

#start clock
moveTime = 0.1
timeLeft = moveTime
startTime = time.perf_counter()

class Snake():

    def __init__(self):
        #create window - be sure numBoxes is even
        self.boxWidth = 25
        self.numBoxesX = 48
        self.numBoxesY = 34
        self.win = GraphWin("Snake", self.boxWidth * self.numBoxesX, self.boxWidth * self.numBoxesY)
        self.win.setBackground("#90EE90")

        #create list of all rects in snake (snake starts in center)
        self.rects = [Rectangle(Point(self.boxWidth * round(self.numBoxesX / 2) - self.boxWidth,self.boxWidth * round(self.numBoxesY / 2)),Point(round(self.boxWidth * self.numBoxesX / 2),round(self.boxWidth * self.numBoxesY / 2) - self.boxWidth)),
              Rectangle(Point(self.boxWidth * round(self.numBoxesX / 2) - 2 * self.boxWidth,self.boxWidth * round(self.numBoxesY / 2)),Point(round(self.boxWidth * self.numBoxesX / 2) - self.boxWidth,round(self.boxWidth * self.numBoxesY / 2) - self.boxWidth))]

        #create list of all previous moves in form [xDir, yDir] as long as self.rects
        self.prevMoves = []
        for rect in self.rects:
            self.prevMoves.append([1,0])
            rect.setFill("#CBC3E3")

        #current direction of snake
        self.xDir = 1
        self.yDir = 0

    def drawRects(self):
        for rect in self.rects:
            rect.draw(self.win)

    def moveSnake(self):
        #add new direction to list of moves and shorten moves list
        self.prevMoves.insert(0,[self.xDir,self.yDir])
        self.endOfSnakeMove = self.prevMoves[-1]
        self.prevMoves = self.prevMoves[:-1]

        for i in range(0,len(self.rects)):
            self.rects[i].move(self.boxWidth * self.prevMoves[i][0], self.boxWidth * self.prevMoves[i][1])

        self.wrapAroundEdge()

    def addNewRect(self):
        #create new rect at end of snake
        newRect = self.rects[-1].clone()
        self.rects.append(newRect)
        self.prevMoves.append(self.endOfSnakeMove)
        #move backwards using previous moves
        self.rects[-1].move(self.boxWidth * -self.prevMoves[-2][0], self.boxWidth * -self.prevMoves[-2][1])
        #draw
        self.rects[-1].draw(self.win)

    def isDead(self):
        for i in range(0, len(self.rects)):
            for j in range(0, len(self.rects)):
                if i != j and self.rects[i].getP1().getX() == self.rects[j].getP1().getX() and self.rects[i].getP1().getY() == self.rects[j].getP1().getY():
                    return True

    def wrapAroundEdge(self):
        for rect in self.rects:
            if rect.getP1().getX() >= self.boxWidth * self.numBoxesX:
                rect.move(-self.boxWidth * self.numBoxesX, 0)
            if rect.getP1().getX() < 0:
                rect.move(self.boxWidth * self.numBoxesX, 0)
            if rect.getP1().getY() <= 0:
                rect.move(0, self.boxWidth * self.numBoxesY)
            if rect.getP1().getY() > self.boxWidth * self.numBoxesY:
                rect.move(0, -self.boxWidth * self.numBoxesY)

class Apple():
    def __init__(self, snake):
        self.boxWidth = snake.boxWidth
        self.numBoxesX = snake.numBoxesX
        self.numBoxesY = snake.numBoxesY
        self.win = snake.win

        self.xPos = self.boxWidth * random.randint(0,self.numBoxesX - 1)
        self.yPos = self.boxWidth * random.randint(1,self.numBoxesY)

        self.apple = Rectangle(Point(self.xPos,self.yPos), Point(self.xPos + self.boxWidth, self.yPos - self.boxWidth))
        self.apple.setFill("#FF7276")
        self.apple.draw(self.win)
    
    def drawNewApple(self):
        #undraw old apple
        self.apple.undraw()

        #draw new apple in random location
        self.xPos = self.boxWidth * random.randint(0,self.numBoxesX - 1)
        self.yPos = self.boxWidth * random.randint(1,self.numBoxesY)

        self.apple = Rectangle(Point(self.xPos,self.yPos), Point(self.xPos + self.boxWidth, self.yPos - self.boxWidth))
        self.apple.setFill("#FF7276")
        self.apple.draw(self.win)

    def isTouchingSnake(self, snake):
        for rect in snake.rects:
            if rect.getP1().getX() == self.xPos and rect.getP1().getY() == self.yPos:
                return True

snake = Snake()
apple = Apple(snake)

#draw starting boxes
snake.drawRects()
    

while True:

    #Input... change direction of snake
    key = snake.win.checkKey()
    if key == "Up":
        snake.xDir = 0
        snake.yDir = -1
    if key == "Down":
        snake.xDir = 0
        snake.yDir = 1
    if key == "Left":
        snake.xDir = -1
        snake.yDir = 0
    if key == "Right":
        snake.xDir = 1
        snake.yDir = 0
    if key == "Escape":
        #Close window
        break
    if key == "m":
        snake.addNewRect()

    #move snake
    timeLeft -= time.perf_counter() - startTime
    startTime = time.perf_counter()
    if timeLeft <= 0:
        timeLeft = moveTime
        snake.moveSnake()
        if apple.isTouchingSnake(snake):
            apple.drawNewApple()
            snake.addNewRect()

        if snake.isDead():
            break

#close window
snake.win.close()