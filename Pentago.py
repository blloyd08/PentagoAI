import copy
from collections import deque
class PentagoBlock:
    def __init__(self,startRow, startColumn, board):
        self.startRow = startRow
        self.startColumn = startColumn
        self.board = board

    def AddToken(self, position, color):
        pos = self.calcPosition(position)
        self.board[pos[0]][pos[1]] = color

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
    def __init__(self):
        self.board = [[0 for j in range(6)] for i in range(6)]
        self.blocks = [PentagoBlock(0,0, self.board), PentagoBlock(0,3,self.board), PentagoBlock(3,0,self.board),PentagoBlock(3,3,self.board)]
        self.player1Win = False
        self.player2Win = False
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                self.board[i][j] = "."

    def AddToken(self,block, position, color):
        self.blocks[block-1].AddToken(position,color)

    def Rotate(self,block,direction):
        if direction.lower() == "l":
            self.blocks[block-1].rotateLeft()
        else:
            self.blocks[block-1].rotateRight()

    def calcBoardTotalScore(self):
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
                self.findPositionScore((i,j),color,scoreArray)
        if self.player1Win or self.player2Win:
            return 1000
        total = 0
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                total += scoreArray[i][j]
                #print("Total: " + str(total) + " position: " + str(i) + "-" + str(j))
        return total

    def findPositionScore(self, position, color, scoreArray):
        playerMultiplier = 1
        if color == "b":
            playerMultiplier = -1

        directions = [upPositions(position), leftPositions(position), diagPositionsLeft(position), diagPositionsRight(position)]
        for j in range(len(directions)):
            searchPositions = directions[j]
            validPositions = []
            count = 0
            searchResult = self.searchDirection(searchPositions, color, count)
            count = searchResult[0]
            validPositions = searchResult[1]
            #Check for win state
            if count >= 5:
                if color == "w":
                    self.player1Win = True
                else:
                    self.player2Win = True
                return
            #Set the score
            self.setScore(scoreArray,validPositions,count,playerMultiplier)

    def searchDirection(self, positions, color, count):
        validPositions = []
        count = 0
        for i in range(len(positions)):
            testPosition = positions.popleft()
            #print("Board:" + str(self.board[testPosition[0]][testPosition[1]]) + " Compare:" + color)
            if self.board[testPosition[0]][testPosition[1]] == str(color):
                count += 1
                validPositions.append(testPosition)
        if count < 2:
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

board = PentagoBoard()
board.AddToken(1,1,"b")
board.AddToken(1,5,"b")
board.AddToken(1,3,"b")
board.AddToken(2,1,"b")
board.AddToken(2,2,"b")
board.AddToken(2,3,"w")
board.print()
#print(board.calcBoardTotalScore())
board.Rotate(1,"l")
board.print()
print(board.calcBoardTotalScore())


