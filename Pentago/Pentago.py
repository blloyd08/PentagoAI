from random import choice
import math
import copy
from collections import deque

class MinMaxFunction:
    Min, Max = range(2)

#Find which position the AI should take
def startMiniMax(board, depth):
    #(Block#, Position#, RotationBlock, RotationDirection)
    nextMove = (0,0,0,"")
    value =  - math.inf
    #Create children, check value
    for i in range(4):
        addBlock = i + 1
        for j in range(9):
            addPos = j + 1
            if board.GetPosition(addBlock, addPos) != ".":
                continue
            # place token in block
            board.AddToken(addBlock,addPos, board.AIColor)
            #Check for win
            preRotationScore =  board.calcBoardTotalScore()
            if board.aiWin or board.playerWin:
                childValue = preRotationScore
                if childValue > value:
                    value = childValue
                    nextMove = (addBlock, addPos, 0, "")
                    print("Start AI Win: " + str(board.aiWin) + " Player Win: " + str(board.playerWin) + " Score: " + str(preRotationScore) + " Next Move: " + str(nextMove))
                board.RemoveToken(addBlock,addPos)
                continue
            #If no win, check rotation
            for k in range(4):
                rotationBlock = k + 1
                if board.AIColor == "b":
                    otherPlayer = "w"
                else:
                    otherPlayer = "b"
                # rotate left
                board.Rotate(rotationBlock, "l")
                #Check value Children from rotation
                childValue = minimax(depth, 1, board, addBlock, addPos, otherPlayer, MinMaxFunction.Min)
                if childValue != None and childValue > value:
                    value = childValue
                    nextMove = (addBlock, addPos, rotationBlock, "l");
                #UNDO left rotation
                board.Rotate(rotationBlock, "r")
                #rotate right
                board.Rotate(rotationBlock, "r")
                #Check value
                #Create children
                #Check value Children from rotation
                childValue = minimax(depth, 1, board, addBlock, addPos, otherPlayer, MinMaxFunction.Min)
                if childValue != None and childValue > value:
                    value = childValue
                    nextMove = (addBlock, addPos, rotationBlock, "r");
                    print("Pos: " + str(addBlock) + "/" + str(addPos) + " Score: " + str(childValue))
                #UNDO rotate right (Back to Initial state)
                board.Rotate(rotationBlock,"l")
            #Remove Token (Back to initial state)
            board.RemoveToken(addBlock,addPos)
    return nextMove


def minimax(maxDepth, depth, board, tokenBlock, tokenPos, player, minMaxFunction):
    value = 0
    if minMaxFunction == MinMaxFunction.Min:
        value = math.inf
    else:
        value = - math.inf
    if maxDepth < depth or board.GetPosition(tokenBlock, tokenPos) != ".":
        return  None

    #Create children, check value
    for i in range(4):
        addBlock = i + 1
        for j in range(9):
            addPos = j + 1
            # skip checks if position is already used
            if board.GetPosition(addBlock, addPos) != ".":
                 continue
            #place token in block
            board.AddToken(addBlock,addPos, player)
            #Check for win
            preRotationScore = board.calcBoardTotalScore()
            if board.aiWin or board.playerWin:
                if minMaxFunction == MinMaxFunction.Min:
                    value = min(value, preRotationScore)
                else:
                    value = max(value, preRotationScore)
                board.RemoveToken(addBlock,addPos)
                continue
            #If no win, check rotation
            for k in range(4):
                rotationBlock = k + 1
                # Toggle Player
                if player == "b":
                    otherPlayer = "w"
                else:
                    otherPlayer = "b"

                # rotate left
                board.Rotate(rotationBlock, "l")
                #Check value
                #Check value Children from rotation
                if minMaxFunction == MinMaxFunction.Min:
                     childValue = minimax(maxDepth, depth + 1, board, addBlock, addPos, otherPlayer,MinMaxFunction.Max)
                     if childValue != None:
                         value = min(value,childValue)
                else:
                    childValue = minimax(maxDepth, depth + 1, board, addBlock, addPos, otherPlayer, MinMaxFunction.Min)
                    if childValue != None:
                        value = max(value,childValue)
                #UNDO left rotation
                board.Rotate(rotationBlock, "r")
                #rotate right
                board.Rotate(rotationBlock, "r")
                #Check value
                #Create children
                #Check value Children from rotation
                if minMaxFunction == MinMaxFunction.Min:
                     childValue = minimax(maxDepth, depth + 1, board, addBlock, addPos, otherPlayer,MinMaxFunction.Max)
                     if childValue != None:
                         value = min(value,childValue)
                else:
                    childValue = minimax(maxDepth, depth + 1, board, addBlock, addPos, otherPlayer, MinMaxFunction.Min)
                    if childValue != None:
                        value = max(value,childValue)
                #UNDO rotate right (Back to Initial state)
                board.Rotate(rotationBlock,"l")
            #Remove Token (Back to initial state)
            board.RemoveToken(addBlock,addPos)
    if value == math.inf or value == - math.inf:
        if minMaxFunction == MinMaxFunction.Min:
            return  - math.inf
        else:
            return math.inf
    return value

class PentagoBlock:
    def __init__(self,startRow, startColumn, board):
        self.startRow = startRow
        self.startColumn = startColumn
        self.board = board

    def AddToken(self, position, color):
        pos = self.calcPosition(position)
        self.board[pos[0]][pos[1]] = color

    def RemoveToken(self, position):
        pos = self.calcPosition(position)
        self.board[pos[0]][pos[1]] = "."

    def GetPosition(self, position):
        pos = self.calcPosition(position)
        return str(self.board[pos[0]][pos[1]])

    def calcPosition(self, pentagoPosition):
        pos = pentagoPosition -1
        column = pos % 3
        row = pos //3
        return (row + self.startRow, column + self.startColumn)

    def rotateRight(self):
        originalList = copy.deepcopy(self.board)
        for i in range(3):
            for j in range(3):
                self.board[self.startRow + i][self.startColumn +j] = originalList[self.startRow + 3 - j - 1][self.startColumn + i]

    def rotateLeft(self):
        originalList = copy.deepcopy(self.board)
        for i in range(3):
            for j in range(3):
                self.board[self.startRow + i][self.startColumn + j] = originalList[self.startRow + j][self.startColumn + 3 - i - 1]


class PentagoBoard:
    def __init__(self, aiColor):
        self.board = [[0 for j in range(6)] for i in range(6)]
        self.blocks = [PentagoBlock(0,0, self.board), PentagoBlock(0,3,self.board), PentagoBlock(3,0,self.board),PentagoBlock(3,3,self.board)]
        self.aiWin = False
        self.playerWin = False
        self.AIColor = aiColor
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                self.board[i][j] = "."

    def AddToken(self,block, position, color):
        self.blocks[block-1].AddToken(position,color)

    def RemoveToken(self,block, position):
        self.blocks[block-1].RemoveToken(position)

    def GetPosition(self, block, position):
        return self.blocks[block-1].GetPosition(position)

    def Rotate(self,block,direction):
        if direction.lower() == "l":
            self.blocks[block-1].rotateLeft()
        else:
            self.blocks[block-1].rotateRight()

    def calcBoardTotalScore(self):
        #Init variables
        self.aiWin = False
        self.playerWin = False
        scoreArray = [[0 for j in range(6)] for i in range(6)]
        #Initialize Array
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                scoreArray[i][j] = 0
        #Calc score of board
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                color = self.board[i][j]
                if color == ".":
                    continue
                self.findPositionScore((i,j),color, scoreArray)
        #Handle win state
        if self.aiWin or self.playerWin:
            value = 0;
            if self.aiWin:
                value += 1000
            if self.playerWin:
                value -= 1000;
            return value
        total = 0
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                total += scoreArray[i][j]
                #print("Total: " + str(total) + " position: " + str(i) + "-" + str(j))
        return total

    def findPositionScore(self, position, color, scoreArray):
        playerMultiplier = 1
        if color != self.AIColor:
            playerMultiplier = -1

        directions = [upPositions(position), leftPositions(position), diagPositionsLeft(position), diagPositionsRight(position)]
        for j in range(len(directions)):
            searchPositions = directions[j]
            searchResult = self.searchDirection(searchPositions, color)
            count = searchResult[0]
            validPositions = searchResult[1]
            #Check for win state
            if count >= 5:
                if color == self.AIColor:
                    self.aiWin = True
                else:
                    self.playerWin = True
                return
            #Set the score
            self.setScore(scoreArray,validPositions,count,playerMultiplier)

    def searchDirection(self, positions, color):
        validPositions = []
        count = 0
        for i in range(len(positions)):
            testPosition = positions.popleft()
            #print("Board:" + str(self.board[testPosition[0]][testPosition[1]]) + " Compare:" + color)
            if self.board[testPosition[0]][testPosition[1]] == str(color):
                count += 1
                validPositions.append(testPosition)
        if count < 1:
            validPositions.clear()
        return (count,validPositions)

    #Apply the score from the valid positions
    def setScore(self, scoreArray, validPositions, count, playerMultiplier):
        if (count > 1):
            while validPositions:
                scorePosition = validPositions.pop()
                if abs(scoreArray[scorePosition[0]][scorePosition[1]]) < count:
                    scoreArray[scorePosition[0]][scorePosition[1]] = count * playerMultiplier
        else:
            validPositions.clear()


    def print(self):
        boarder = "+---+---+"
        print(boarder)
        for i in range(len(self.board)):
            row =["|"]
            for j in range(len(self.board[i])):
                row.append(self.board[i][j])
                if j == 2:
                    row.append("|")
            row.append("|")
            print("".join(row))
            if i == 2:
                print(boarder)
        print(boarder)


def upPositions(startPosition):
    x = startPosition[0]
    y = startPosition[1]
    count = 0
    positions = deque()
    while count < 5 and x - count >= 0:
        positions.append((x - count, y))
        count += 1
    return positions

def leftPositions(startPosition):
    x = startPosition[0]
    y = startPosition[1]
    count = 0
    positions = deque()
    while count < 5 and y - count >= 0:
        positions.append((x, y - count))
        count += 1
    return positions

def diagPositionsLeft(startPosition):
    x = startPosition[0]
    y = startPosition[1]
    count = 0
    positions = deque()
    while count < 5 and x - count >= 0 and y - count >= 0:
        positions.append((x - count, y - count))
        count += 1
    return positions

def diagPositionsRight(startPosition):
    x = startPosition[0]
    y = startPosition[1]
    count = 0
    positions = deque()
    while count < 5 and x - count >= 0 and y + count < 6:
        positions.append((x - count, y + count))
        count += 1
    return positions


#aiColor = choice(["b","w"])
aiColor = "w"
aiPlayer = choice([1,2])
print("AI is player: " + str(aiPlayer))
print("AI is color: " + aiColor)
board = PentagoBoard(aiColor)
board.AddToken(1,1,"b")
board.AddToken(1,2,"b")
board.AddToken(1,3,"b")
board.AddToken(2,1,"b")
board.AddToken(2,4,"w")
board.AddToken(2,3,"w")
board.print()
print(board.calcBoardTotalScore())
nextMove =  startMiniMax(board,1)
print(nextMove)
board.AddToken(nextMove[0], nextMove[1],aiColor)
board.Rotate(nextMove[2],nextMove[3])
board.print()
while True:
    var = input("Enter next move:")
    addBlock = int(var[0])
    pos = int(var[2])
    rotationBlock = int(var[4])
    rotationDirection = var[5]
    board.AddToken(addBlock,pos, "b")
    board.Rotate(rotationBlock,rotationDirection)
    board.print()
    nextMove = startMiniMax(board, 2)
    print("AI chooses: " + str(nextMove))
    board.AddToken(nextMove[0], nextMove[1],aiColor)
    board.Rotate(nextMove[2],nextMove[3])
    board.print()
#board.Rotate(1,"l")
#board.print()
#print(board.calcBoardTotalScore())




