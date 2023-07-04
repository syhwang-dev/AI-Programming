import random
import math

DELTA = 0.01
NumEval = 0

def createProblem(): ###
    ## Read in an expression and its domain from a file.
    ## Then, return a problem 'p'.
    ## 'p' is a tuple of 'expression' and 'domain'.
    ## 'expression' is a string.
    ## 'domain' is a list of 'varNames', 'low', and 'up'.
    ## 'varNames' is a list of variable names.
    ## 'low' is a list of lower bounds of the varaibles.
    ## 'up' is a list of upper bounds of the varaibles.
    fileName = input("Enter the filename of a function > ")
    infile = open(fileName, mode='r')
    expression = infile.readline()
    
    varName = []
    low = []
    up = []

    line = infile.readline()
    while line != '':  # line이 끝나지 않으면 계속
        data = line.split(',')
        varName.append(data[0])
        low.append(float(data[1]))
        up.append(float(data[2]))
        line = infile.readline()
    
    infile.close()
    domain = [varName, low, up]

    return expression, domain

def randomInit(p): ###
    domain = p[1]
    low = domain[1]
    up = domain[2]

    init = []
    # 반복문
    for i in range(len(low)):
        # r = random.uniform(low, up)  # 랜덤 값 generation    -> 에러 발생
        r = random.uniform(low[i], up[i])
        init.append(r)
    return init    # Return a random initial point
                   # as a list of values

def evaluate(current, p):
    ## Evaluate the expression of 'p' after assigning
    ## the values of 'current' to the variables
    global NumEval  # 글로벌 변수 값을 바꾸려고 할 때 사용
    
    NumEval += 1
    expr = p[0]         # p[0] is function expression
    varNames = p[1][0]  # p[1] is domain
    for i in range(len(varNames)):
        assignment = varNames[i] + '=' + str(current[i])  # x1 = 2.3
        exec(assignment)
    return eval(expr)

def mutate(current, i, d, p): ## Mutate i-th of 'current' if legal
    curCopy = current[:]
    domain = p[1]        # [VarNames, low, up]
    l = domain[1][i]     # Lower bound of i-th
    u = domain[2][i]     # Upper bound of i-th
    if l <= (curCopy[i] + d) <= u:
        curCopy[i] += d
    return curCopy

def describeProblem(p):
    print()
    print("Objective function:")
    print(p[0])   # Expression
    print("Search space:")
    varNames = p[1][0] # p[1] is domain: [VarNames, low, up]
    low = p[1][1]
    up = p[1][2]
    for i in range(len(low)):
        print(" " + varNames[i] + ":", (low[i], up[i])) 

def displaySetting():
    print()
    print("Search algorithm: Steepest-Ascent Hill Climbing")
    print()
    print("Mutation step size:", DELTA)

def displayResult(solution, minimum):
    print()
    print("Solution found:")
    print(coordinate(solution))  # Convert list to tuple
    print("Minimum value: {0:,.3f}".format(minimum))
    print()
    print("Total number of evaluations: {0:,}".format(NumEval))

def coordinate(solution):
    c = [round(value, 3) for value in solution]
    return tuple(c)  # Convert the list to a tuple