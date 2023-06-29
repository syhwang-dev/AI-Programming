import random
import math

# 제목에 n은 뉴메릭을 의미함.

# 실행 속도가 체감상 steepest ascent 보다 빠름.

DELTA = 0.01   # Mutation step size
# 델타값이 더 작아지면 값은 더 좋아짐. 물론 속도가 더 걸리지만
# steepest ascent는 무조건 10번을 했지만, 이것은 하나를 뽑아서 좋으면 업데이트를 바로함.
LIMIT_STUCK = 100 # Max number of evaluations enduring no improvement
NumEval = 0    # Total number of evaluations


def main():
    # Create an instance of numerical optimization problem
    p = createProblem()   # 'p': (expr, domain)
    # Call the search algorithm
    solution, minimum = firstChoice(p)
    # Show the problem and algorithm settings
    
    # 출력 part
    describeProblem(p)
    displaySetting()
    # Report results
    displayResult(solution, minimum)


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

# firstChoice의 특징: 랜덤하게 '하나'를 선택
def firstChoice(p):
    current = randomInit(p)   # 'current' is a list of values
    valueC = evaluate(current, p)
    i = 0
    while i < LIMIT_STUCK:  # LIMIT_STUCK: 추가적인 횟수(기회)를 주는 것
        successor = randomMutant(current, p)
        valueS = evaluate(successor, p)
        if valueS < valueC:  # 좋아졌으면 업데이트하고 i를 리셋함.
            current = successor
            valueC = valueS
            i = 0              # Reset stuck counter
        else:
            i += 1
    return current, valueC


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
    global NumEval
    
    NumEval += 1
    expr = p[0]         # p[0] is function expression
    varNames = p[1][0]  # p[1] is domain: [varNames, low, up]
    for i in range(len(varNames)):
        assignment = varNames[i] + '=' + str(current[i])
        exec(assignment)
    return eval(expr)

# 중요한 part
def randomMutant(current, p): ###
    i = random.randint(0, len(current)-1)
    # len(current)는 5임.
    # 필요한 값은 0, 1, 2, 3, 4 이므로 len(current)에서 -1을 해줌.

    if random.uniform(0,1)> 0.5:
        d = DELTA
    else:
        d = -DELTA    
    # d = DELTA
    return mutate(current, i, d, p) # Return a random successor


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
    print("Search algorithm: First-Choice Hill Climbing")
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

main()
