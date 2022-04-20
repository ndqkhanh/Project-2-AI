from os.path import exists

class State:
    def __init__(self, l, accumulate = 0, heuristic = -1):
        self.queensPos = l
        self.mapDictionary = ','.join(str(x) for x in l)
        self.heuristic = heuristic
        self.accumulate = accumulate

    def toString(self):
        return self.mapDictionary

    def __del__(self):
        pass
    def pos_To_id(self,col, row):#ham nay khac voi ham cua cau c
        return row * 8 + col + 1
    def restrictions_Of_pos(self,col, row):#ham nay khac voi ham cua cau c
        result = []

        #row
        for i in range(8):
            if i != row:
                clause = []
                clause.append(-self.pos_To_id(col,row))
                clause.append(-self.pos_To_id(col,i))
                result.append(clause)
        #column
        for i in range(8):
            if i != col:
                clause = []
                clause.append(-self.pos_To_id(col,row))
                clause.append(-self.pos_To_id(i,row))
                result.append(clause)

        #main diagonal
        x = col - row if col - row > 0 else 0
        y = row - col if col - row < 0 else 0
        while x < 8 and y < 8:
            if x != col and y != row:
                clause = []
                clause.append(-self.pos_To_id(col,row))
                clause.append(-self.pos_To_id(x,y))
                result.append(clause)
            x += 1
            y += 1

        #anti diagonal
        y = row + col if row + col < 7 else 7
        x = col + col - 7 if row + col > 7 else 0

        while x < 8 and y >= 0:
            if x != col and y != row:
                clause = []
                clause.append(-self.pos_To_id(col,row))
                clause.append(-self.pos_To_id(x,y))
                result.append(clause)
            x += 1
            y -= 1

        return result
    def rowAndcolumnConditions(self):#ham nay giong voi cua cau c
        #OrTrue condition Ex: a v b
        list = []
        for i in range(8):#row and column
            row_OrTrueCondition = []
            column_OrTrueCondition = []

            for j in range(8):
                row_OrTrueCondition.append(i*8 + j + 1)
                column_OrTrueCondition.append(i + j*8 + 1)
            list.append(row_OrTrueCondition)
            list.append(column_OrTrueCondition)
        return list
    def toCNF(self):
        cnfSet = self.rowAndcolumnConditions()
        for i in self.queensPos:
            if self.queensPos[i] != -1:
                #i: column index
                #self.queensPos[i]: row index
                cnfSet = cnfSet + self.restrictions_Of_pos(i,self.queensPos[i])
                cnfSet.append([self.queensPos[i]*8 + i + 1])
        return cnfSet


def readInput():
    filename = input()
    if  exists(filename): 
        fileHandle = open(filename, 'r')
        fileHandle.readline() #read m
        list1 = [[int(j) for j in i.split()] for i in fileHandle]
        fileHandle.close()
    else:
        print("file does not exist")
        exit()
    return list1

def convertToState(queenPos):
    pos = [-1] * 8
    for i in queenPos:
        pos[i[0]] = i[1]
    #pos[x] = -1 => there is no queen in column x
    #pos[x] = y => there is 1 queen in column x row y and the tacit understanding logical variable x + y * 8 + 1 is true

    del queenPos #release data

    return State(pos)

def getNumOfQueenEachRowColumnDiagonal(s):
    row = [0] * 8
    column = [0] * 8
    mainDiagonal = [0] * 15
    antiDiagonal = [0] * 15

    for i in range(len(s.queensPos)):
        if s.queensPos[i] != -1:
            j = s.queensPos[i]
            column[i] += 1
            row[j] += 1
            mainDiagonal[i - j + 7] += 1
            antiDiagonal[i + j] += 1
    result = []
    result.append(row)
    result.append(column)
    result.append(mainDiagonal)
    result.append(antiDiagonal)

    return result

def getFalseCNFClause(boardIn4):
    counter = 0
    for i in range(2):# row and column
        for line in boardIn4[i]:
            counter += ( (line * (line - 1) ) // 2) + (1 if line == 0 else 0)# line C 2 false clause and 1 false clause if line = 0 means avbvcv...vz = false  

    for i in range(2,4):
        for line in boardIn4[i]:
            counter += (line * (line - 1)) // 2 # line C 2 false clause 

    return counter

def heuristicPlusAccumulateState(s):
    return s.heuristic + s.accumulate