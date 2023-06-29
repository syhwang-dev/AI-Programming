import random
import math

# 글로벌 변수
DELTA = 0.001   # Mutation step size  // 스텝 사이즈가 너무 작아도 너무 커도 안 좋음.
# 값이 작아질수록 세밀해지지만 동작 시간이 오래 걸림.
# DELTA = 0.01   # Mutation step size
NumEval = 0    # Total number of evaluations


def main():
    # Create an instance of numerical optimization problem
    p = createProblem()   # 'p': (expr, domain)
    # Call the search algorithm
    solution, minimum = steepestAscent(p)
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


def steepestAscent(p):
    # current: 시작점
    current = randomInit(p) # 'current' is a list of values
    valueC = evaluate(current, p)  # valueC: 시작점에 해당하는 함수값
    while True:
        neighbors = mutants(current, p)  # neighbors: 주변의 후보들을 의미
        successor, valueS = bestOf(neighbors, p)  # bestOf: 제일 좋은 것을 찾아내는 함수 / successor, valueS: 변수, 함수값
        # 현재보다 좋아지는지 판단을 해야 함.
        # 계속 값을 낮추고 있는 중
        if valueS >= valueC:  # 나빠진 것을 의미 - 멈춰야 함.
            break
        else:  # 그렇지 않으면 계속 진행해야 함.
            # 업데이트
            current = successor
            valueC = valueS
    return current, valueC

# input으로 p가 들어감. / 도메인: 범위
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

# 한 줄 씩: statement
# expression
# x = exp 이렇게 주어질 때가 많음.
# statement - exec 펑션 / expression - eval 펑션

# mutants: 델타 상수 값으로 변화를 준다,
def mutants(current, p): ###
    neighbors = []
    for i in range(len(current)):
        mutant = mutate(current, i, DELTA, p)
        neighbors.append(mutant)
        mutant = mutate(current, i, -DELTA, p)
        neighbors.append(mutant)


    # 총 10개 출력?
    return neighbors     # Return a set of successors

# d = 델타 사이즈를 의미
def mutate(current, i, d, p): ## Mutate i-th of 'current' if legal
    curCopy = current[:]
    domain = p[1]        # [VarNames, low, up]
    l = domain[1][i]     # Lower bound of i-th
    u = domain[2][i]     # Upper bound of i-th
    if l <= (curCopy[i] + d) <= u:
        curCopy[i] += d
    return curCopy

def bestOf(neighbors, p): ###
    best = neighbors[0]
    bestValue = evaluate(best, p)  # best 값을 찾음 / bestValue는 현재값

    for i in range(1, len(neighbors)):
        newValue = evaluate(neighbors[i], p)

        if newValue < bestValue:  # 더 좋으면
            best = neighbors[i]
            bestValue = newValue 

    # for neighbor in neighbors[1:]:
    #     neighborValue = evaluate(neighbor, p)

    #     if neighborValue > bestValue:
    #         best = neighbor
    #         bestValue = neighborValue

    return best, bestValue

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


main()
