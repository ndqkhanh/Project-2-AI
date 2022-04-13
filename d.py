from random import randint
from pysat.solvers import Solver

resultList = []

#OrTrue condition Ex: a v b
for i in range(8):#row and column
    row_OrTrueCondition = []
    column_OrTrueCondition = []

    for j in range(8):
        row_OrTrueCondition.append(i*8 + j + 1)
        column_OrTrueCondition.append(i + j*8 + 1)

    resultList.append(row_OrTrueCondition)
    resultList.append(column_OrTrueCondition)
   
#Pair orFalse condition Ex: !a v !b, 
#we do not have or true digonal condition because a digonal can have at most 1 queen
#so its condition is only "Pair orFalse condition"
for i in range(8):
    for j in range(8):
        currentV = i*8 + j + 1

        #row
        for t in range(j + 1, 8):
            clause = []
            clause.append(-currentV)
            clause.append(-(i*8 + t + 1))
            resultList.append(clause);

        #column
        for t in range(i + 1, 8):
            clause = []
            clause.append(-currentV)
            clause.append(-(t*8 + j + 1))
            resultList.append(clause);

        #main digonal
        ti = i + 1
        tj = j + 1
        while ti < 8 and tj < 8:
            clause = []
            clause.append(-currentV)
            clause.append(-(ti*8 + tj + 1))
            resultList.append(clause);
            ti += 1
            tj += 1

        #anti digonal
        ti = i + 1
        tj = j - 1
        while ti < 8 and tj >= 0:
            clause = []
            clause.append(-currentV)
            clause.append(-(ti*8 + tj + 1))
            resultList.append(clause);
            ti += 1
            tj -= 1

resultList.append([randint(1,64)])#put one queen to a square

for clause in resultList:
    print(*clause, sep ='^')

s = Solver(bootstrap_with = resultList)
print(s.solve())
print(s.get_model())
