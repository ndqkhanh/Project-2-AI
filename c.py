from pysat.solvers import Solver

# Each rows and columns must have one queen
def rowAndcolumnConditions(level = 2):
    #OrTrue condition Ex: a v b
    list = []
    for i in range(8):#row and column
        row_OrTrueCondition = []
        column_OrTrueCondition = []

        for j in range(8):
            if level == 2:
                row_OrTrueCondition.append(i*8 + j + 1)
            column_OrTrueCondition.append(i + j*8 + 1)
        if level == 2:
            list.append(row_OrTrueCondition)
        list.append(column_OrTrueCondition)
    return list


# Restrict the number of queens in each row and column and digonal in each level
def createCNFSet(queenPositions=[], level=2):
    CNFclauses = []

    #  Restrict for row and columns in each level
    for item in rowAndcolumnConditions(level):
        CNFclauses.append(item)

    for i in range(8):
        for j in range(8):
            currentV = i * 8 + j + 1

            # column
            for t in range(i + 1, 8):
                clause = []
                clause.append(-currentV)
                clause.append(-(t * 8 + j + 1))
                CNFclauses.append(clause)

            if level == 2:
                # row
                for t in range(j + 1, 8):
                    clause = []
                    clause.append(-currentV)
                    clause.append(-(i*8 + t + 1))
                    CNFclauses.append(clause)

                # main digonal
                ti = i + 1
                tj = j + 1
                while ti < 8 and tj < 8:
                    clause = []
                    clause.append(-currentV)
                    clause.append(-(ti*8 + tj + 1))
                    CNFclauses.append(clause)
                    ti += 1
                    tj += 1

                # anti digonal
                ti = i + 1
                tj = j - 1
                while ti < 8 and tj >= 0:
                    clause = []
                    clause.append(-currentV)
                    clause.append(-(ti*8 + tj + 1))
                    CNFclauses.append(clause)
                    ti += 1
                    tj -= 1

    for pos in queenPositions:
        CNFclauses.append([pos[0] * 8 + pos[1] + 1])
    return CNFclauses


# Pass in all the CNF clauses then return the result and visualize
def solveCNFClauses(resultList):
    s = Solver(bootstrap_with = resultList)

    isSatisfy = s.solve()
    result = s.get_model()

    if isSatisfy == True:
        print("\nChessboard solution found:\n")
        for i in range(8):
            for j in range(8):
                if result[i*8 + j] > 0:
                    print("Q", end = " ")
                else:
                    print(".", end = " ")
            print("")
        print("\nResult:\n")
        print(s.get_model())
    else:
        print("There are conflicts in the CNF clauses")



queenPositions = [[3,5]]
resultList = createCNFSet(queenPositions, level=1)

for clause in resultList:
    print(*clause, sep='v')

solveCNFClauses(resultList)