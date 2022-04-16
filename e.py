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
    pos = [0] * 8
    for i in queenPos:
        pos[i[0]] = i[1]

    del queenPos #release data
    return State(pos)

def getNumOfQueenEachRowColumnDiagonal(s):
    row = [0] * 8
    column = [0] * 8
    mainDiagonal = [0] * 15
    antiDiagonal = [0] * 15

    for i in range(len(s.queensPos)):
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


def Astar(initState):

    expandedState = {}
    frontier = [initState]#priority queue
    while len(frontier) > 0:
        curState = frontier.pop(0)#print state to GUI here
        if curState.heuristic == 0:
            return curState

        if curState.mapDictionary not in expandedState.keys():
            expandedState[curState.mapDictionary] = True

            numOfQueenEachRowColumnDiagonal = getNumOfQueenEachRowColumnDiagonal(curState)
            falseCNFClause =  getFalseCNFClause(numOfQueenEachRowColumnDiagonal)

            for i in range(len(curState.queensPos)):#posistion each queen

                j = curState.queensPos[i]

                compress = numOfQueenEachRowColumnDiagonal
                decreaseFalseClause = (-(compress[0][j] - 1) if compress[0][j] > 1 else 1 ) - ( compress[2][i - j + 7] - 1) - ( compress[3][i + j] - 1 )

                for newj in range(8):# expanding states
                    if j != newj:

                        newPos = curState.queensPos.copy()
                        newPos[i] = newj
                        
                        increaseFalseClause = (compress[0][newj] if compress[0][newj] > 0 else -1) + compress[2][i - newj + 7] + compress[3][i + newj]
                        newHeurisistic = falseCNFClause + decreaseFalseClause + increaseFalseClause

                        newState = State(newPos, accumulate = curState.accumulate + 1, heuristic = newHeurisistic)# generate new state

                        #print(falseCNFClause)
                        #print(newState.toString())
                        #print(newState.accumulate)
                        #print(newState.heuristic)
                        #print()
                        if newState.mapDictionary not in expandedState.keys():#not in expanded list
                            frontier.append(newState)
            #sort to become priority queue
            frontier.sort(key = heuristicPlusAccumulateState)

    return initState





queenPos = readInput()
queenPos = convertToState(queenPos)

resultQueenPos = Astar(queenPos)
del queenPos

print(resultQueenPos.toString())
