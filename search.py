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

def convertToState(queenPos):
    pos = [-1] * 8
    for i in queenPos:
        pos[i[0]] = i[1]
    #pos[x] = -1 => there is no queen in column x
    #pos[x] = y => there is 1 queen in column x row y and the tacit understanding logical variable x + y*8 + 1 is true

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