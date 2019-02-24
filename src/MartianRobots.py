
import sys
import re

test = False

orientation = ('N', 'S', 'E', 'W')
command = ('F', 'L', 'R')

turnLeftSwitcher = {
    'N': 'W',
    'S': 'E',
    'E': 'N',
    'W': 'S'
}

turnRightSwitcher = {
    'N': 'E',
    'S': 'W',
    'E': 'S',
    'W': 'N'
}


class Scent:
    'Definition of a scent'

    def __init__(self, xCoord, yCoord, orientation):
        self.xCoord = xCoord
        self.yCoord = yCoord
        self.orientation = orientation

    def compareScent(self, xCoord, yCoord, orientation):
        return (self.xCoord == xCoord) and (self.yCoord == yCoord) and (self.orientation == orientation)


class Map:
    'Definition of the map'

    __listScent = []

    def __init__(self, xSize, ySize):
        self.xSize = xSize
        self.ySize = ySize

    def addScent(self, Scent):
        self.__listScent.append(Scent)

    def checkScent(self, Scent):
        for i in range(len(self.__listScent)):
            if self.__listScent[i].compareScent(Scent.xCoord, Scent.yCoord, Scent.orientation):
                return True
        return False

    def printScent(self):
        for i in range(len(self.__listScent)):
            print(self.__listScent[i].xCoord, self.__listScent[i].yCoord)


class Robot:
    'Robot that will land in the planet landscape'

    isLost = False

    def __init__(self, origX, origY, orientation):
        self.xPos = origX
        self.yPos = origY
        self.orientation = orientation

    def move(self, command, Map):

        if self.isLost:
            return

        tempScent = Scent(self.xPos, self.yPos, self.orientation)

        if Map.checkScent(tempScent) and command == 'F':
            del tempScent
            return

        if command == 'F':  # Move Formard
            if self.orientation == 'N':
                self.yPos += 1
            elif self.orientation == 'S':
                self.yPos -= 1
            elif self.orientation == 'E':
                self.xPos += 1
            elif self.orientation == 'W':
                self.xPos -= 1
        elif command == 'L':  # Turn Left
            self.orientation = turnLeftSwitcher.get(self.orientation)
        elif command == 'R':  # Turn Right
            self.orientation = turnRightSwitcher.get(self.orientation)

        if self.xPos > Map.xSize or self.yPos > Map.ySize or self.xPos < 0 or self.yPos < 0:
            self.isLost = True
            self.xPos = tempScent.xCoord
            self.yPos = tempScent.yCoord
            Map.addScent(tempScent)

        return True


if test is not True:
    inputString = raw_input("Please, input the planet size in this format: 23 32 (Max 50x50)\n")
    valid = bool(re.match("^(([0-9]|[0-4][0-9]|50)\s([0-9]|[0-4][0-9]|50))$", inputString))
    if valid != True:
        print("Incorrect input, the first line format is x y to define the size of the planet landscape. X and Y must to be between 1 and 50.")
        sys.exit(-1)

    listInput = inputString.split(' ')
    xSize = int(listInput[0])
    ySize = int(listInput[1])

    print("Planet size: {}x{}\n".format(xSize, ySize))

    listRobots = {}

    moreInput = True
    while moreInput:
        inputString = raw_input("Input the initial position of the robot in this format: 1 1 W\n")
        valid = bool(re.match("^(([0-9]|[0-4][0-9]|50)\s([0-9]|[0-4][0-9]|50)\s(W|E|N|S))$", inputString))
        if valid is not True:
            print("Incorrect input, the format must to be: X Y (one of W, N, S, E).")
            del inputString
            del valid
            del moreInput
            sys.exit(-1)
        listInput = inputString.split(' ')
        if int(listInput[0]) > xSize or int(listInput[1]) > ySize:
            print("Incorrect input, the coordinates for the robot need to be within the planet size.")
            del inputString
            del valid
            del moreInput
            del listInput
            sys.exit(-1)
        tempRobot = Robot(int(listInput[0]), int(listInput[1]), str(listInput[2]))
        inputString = raw_input("Input the list of commands for this robot. Commands valid are F, R or L. Max 100 commands.\n")
        valid = bool(re.match("^(R|F|L){1,100}$", inputString))
        if valid is not True:
            print("Incorrect input, wrong command found or too many commands.")
            del inputString
            del valid
            del moreInput
            del listInput
            del tempRobot
            sys.exit(-1)
        listRobots.update({tempRobot: inputString})
        inputString = raw_input("Do you want to add another robot? (y/n): \n")
        if inputString[0] == 'n' or inputString[0] == 'N':
            moreInput = False

    mars = Map(xSize, ySize)
    for key, value in listRobots.items():
        for i in value:
            key.move(i, mars)
        print("{} {} {} {}".format(key.xPos, key.yPos, key.orientation, 'LOST' if key.isLost else ''))
    del listRobots
    del inputString
    del valid
    del moreInput
    del listInput
    del tempRobot
    del mars
else:
    print("---Test Mode---")
    # We initiliaze the planet landscape
    xSize = 5
    ySize = 3
    mars = Map(xSize, ySize)
    r1 = Robot(1, 1, 'E')
    r1.move('R', mars)
    r1.move('F', mars)
    r1.move('R', mars)
    r1.move('F', mars)
    r1.move('R', mars)
    r1.move('F', mars)
    r1.move('R', mars)
    r1.move('F', mars)
    print(r1.isLost, r1.xPos, r1.yPos, r1.orientation)
    del r1

    r2 = Robot(3, 2, 'N')
    r2.move('F', mars)
    r2.move('R', mars)
    r2.move('R', mars)
    r2.move('F', mars)
    r2.move('L', mars)
    r2.move('L', mars)
    r2.move('F', mars)
    r2.move('F', mars)
    r2.move('R', mars)
    r2.move('R', mars)
    r2.move('F', mars)
    r2.move('L', mars)
    r2.move('L', mars)
    print(r2.isLost, r2.xPos, r2.yPos, r2.orientation)
    del r2

    r3 = Robot(0, 3, 'W')
    r3.move('L', mars)
    r3.move('L', mars)
    r3.move('F', mars)
    r3.move('F', mars)
    r3.move('F', mars)
    r3.move('L', mars)
    r3.move('F', mars)
    r3.move('L', mars)
    r3.move('F', mars)
    r3.move('L', mars)
    print(r3.isLost, r3.xPos, r3.yPos, r3.orientation)
    del r3

    del mars
