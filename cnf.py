import random
def rowAndcolumnConditions():
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

def pos_To_id(x, y):
    return x * 8 + y + 1

def id_To_pos(v):
    clause = []
    tmp = int((v - 1) / 8)
    clause.append(tmp)
    clause.append(v - 1 - tmp * 8)
    return clause

def restrictions_Of_pos(x, y):
    result = []

    currentV = pos_To_id(x, y)

    # column+
    xcol = x + 1
    while xcol >= 0 and xcol < 8:
        clause=[]
        clause.append(-currentV)
        clause.append(-pos_To_id(xcol, y))
        result.append(clause)
        xcol += 1
    # column-
    xcol = x - 1
    while xcol >= 0 and xcol < 8:
        clause=[]
        clause.append(-currentV)
        clause.append(-pos_To_id(xcol, y))
        result.append(clause)
        xcol -= 1


    # row+
    yrow = y + 1
    while yrow >= 0 and yrow < 8:
        clause=[]
        clause.append(-currentV)
        clause.append(-pos_To_id(x, yrow))
        result.append(clause)
        yrow += 1
    # row-
    yrow = y - 1
    while yrow >= 0 and yrow < 8:
        clause=[]
        clause.append(-currentV)
        clause.append(-pos_To_id(x, yrow))
        result.append(clause)
        yrow -= 1


    # major diag+
    xdiag = x + 1
    ydiag = y + 1
    while xdiag >= 0 and xdiag < 8 and ydiag >= 0 and ydiag < 8:
        clause=[]
        clause.append(-currentV)
        clause.append(-pos_To_id(xdiag, ydiag))
        result.append(clause)
        ydiag += 1
        xdiag += 1
    # major diag-
    xdiag = x - 1
    ydiag = y - 1
    while xdiag >= 0 and xdiag < 8 and ydiag >= 0 and ydiag < 8:
        clause=[]
        clause.append(-currentV)
        clause.append(-pos_To_id(xdiag, ydiag))
        result.append(clause)
        ydiag -= 1
        xdiag -= 1


    # minor diag+
    xdiag = x - 1
    ydiag = y + 1
    while xdiag >= 0 and xdiag < 8 and ydiag >= 0 and ydiag < 8:
        clause=[]
        clause.append(-currentV)
        clause.append(-pos_To_id(xdiag, ydiag))
        result.append(clause)
        ydiag += 1
        xdiag -= 1
    # minor diag-
    xdiag = x + 1
    ydiag = y - 1
    while xdiag >= 0 and xdiag < 8 and ydiag >= 0 and ydiag < 8:
        clause=[]
        clause.append(-currentV)
        clause.append(-pos_To_id(xdiag, ydiag))
        result.append(clause)
        ydiag -= 1
        xdiag += 1

    return result

def createCNFSet(level = 1):
    isSatisfy = False

    while True:
        if isSatisfy == True:
            break

        # return result
        resultList = []

        #return postitions of queen place consecutively
        Positions = []

        # Board from 1 to 64 for level == 2
        board = list(range(1, 65))

        # count number of queens have been placed
        count = 0

        # set of 8 columns to pick for level 1
        if level == 1:
            columnpicks = []
            for i in range(8):
                column_OrTrueCondition = []
                for j in range(8):
                    column_OrTrueCondition.append(i + j*8 + 1)
                columnpicks.append(column_OrTrueCondition)

        for item in rowAndcolumnConditions():
            resultList.append(item)

        # level == 1
        if level == 1:
            for col in columnpicks:
                if len(col) == 0: break
                pos = random.choice(col)
                col.remove(pos)

                for i in restrictions_Of_pos(id_To_pos(pos)[0], id_To_pos(pos)[1]):
                    resultList.append(i)

                for i in columnpicks:
                    for j in resultList:
                        for t in j:
                            if t < 0:
                                if -t in i:
                                    i.remove(-t)
                Positions.append(pos)
                count += 1
        else: # level == 2
            while count < 8:
                if len(board) == 0: break
                pos = random.choice(board)
                board.remove(pos)

                for i in restrictions_Of_pos(id_To_pos(pos)[0], id_To_pos(pos)[1]):
                    resultList.append(i)

                # for i in columnpicks:
                for j in resultList:
                    for t in j:
                        if t < 0:
                            if -t in board:
                                board.remove(-t)
                Positions.append(pos)
                count += 1

        # Make positions of queen placed to true
        for i in Positions:
            resultList.append([i])

        # check if we successfully place 8 queens in board
        if count >= 8: isSatisfy = True

    return resultList

