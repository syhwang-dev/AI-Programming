import random
import math

LIMIT_STUCK = 100 # Max number of evaluations enduring no improvement
NumEval = 0

def createProblem():
    ## Read in a TSP (# of cities, locatioins) from a file.
    ## Then, create a problem instance and return it.
    fileName = input("Enter the file name of a TSP: ")
    infile = open(fileName, 'r')
    # First line is number of cities
    numCities = int(infile.readline())  # 도시의 수
    locations = []
    line = infile.readline()  # The rest of the lines are locations
    while line != '':
        locations.append(eval(line)) # Make a tuple and append / eval(): 있는 그대로 실행
        line = infile.readline()
    infile.close()
    table = calcDistanceTable(numCities, locations)  # locations: tuple로 구성된 리스트 
    return numCities, locations, table

def calcDistanceTable(numCities, locations): ###
    table = [] # 2d

    # 같은 도시라면 0이 나올 것임.
    # (1, 1) = 0
    # (2, 2) = 0

    for i in range(numCities):
        # 첫번째 도시에 대한 다른 도시의 거리
        row = []
        for j in range(numCities):
            # print("locations[i]:", i, locations[i])
            # print("locations[j]:", j, locations[j])

            dx = locations[i][0]-locations[j][0]  # x축
            dy = locations[i][1]-locations[j][1]  # y축
            d = round(math.sqrt(dx ** 2 + dy ** 2), 1)
            row.append(d)
        table.append(row)

    return table # A symmetric matrix of pairwise distances

def randomInit(p):   # Return a random initial tour
    n = p[0]
    init = list(range(n))
    random.shuffle(init)
    return init

def evaluate(current, p): ###
    global NumEval
    NumEval += 1
    # numCities, locations, tables = p
    numCities = p[0]
    table = p[2]
    cost = 0

    # print("p:", p)  # 디버깅이 안 될 때 사용

    for i in range(numCities-1):  # 범위가 numCities까지 가면 안 됨.
        locFrom = current[i]
        locTo = current[i+1]
        cost += table[locFrom][locTo]
    
    # 끝에서 앞으로 되돌아가기
    cost += table[current[numCities-1]][current[0]]

    return cost

def inversion(current, i, j):  ## Perform inversion
    curCopy = current[:]  # 복사하기
    while i < j:
        curCopy[i], curCopy[j] = curCopy[j], curCopy[i]  # 파이썬 장점: 임시 변수를 만들지 않고 이동
        i += 1
        j -= 1
    return curCopy

def describeProblem(p):
    print()
    n = p[0]
    print("Number of cities:", n)
    print("City locations:")
    locations = p[1]
    for i in range(n):
        print("{0:>12}".format(str(locations[i])), end = '')
        if i % 5 == 4:
            print()

def displaySetting():
    print()
    print("Search algorithm: Steepest-Ascent Hill Climbing")

def displayResult(solution, minimum):
    print()
    print("Best order of visits:")
    tenPerRow(solution)       # Print 10 cities per row
    print("Minimum tour cost: {0:,}".format(round(minimum)))
    print()
    print("Total number of evaluations: {0:,}".format(NumEval))

def tenPerRow(solution):
    for i in range(len(solution)):
        print("{0:>5}".format(solution[i]), end='')
        if i % 10 == 9:
            print()