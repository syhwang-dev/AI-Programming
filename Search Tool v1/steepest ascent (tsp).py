#### steepest ascent (n)과 비교했을 때, 조합의 문제
#### 알고리즘이 바뀌지는 않음.

#### 5 라는 도시가 있을 때 도시의 숫자를 5.1 이렇게 바꿀 수 없으므로 랜덤 사용


import random
import math

NumEval = 0    # Total number of evaluations
# 델타값이 없음.


def main():
    # Create an instance of TSP
    p = createProblem()    # 'p': (numCities, locations, table) / table: 직선 거리 계산
    # Call the search algorithm
    solution, minimum = steepestAscent(p)
    # Show the problem and algorithm settings
    
    # 출력 part
    describeProblem(p)
    displaySetting()
    # Report results
    displayResult(solution, minimum)
    
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


# 직선 거리 계산 / 도시 간의 거리 계산
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

    
    # for i in range(numCities):
    #     for j in range(i+1, numCities):
    #         # 거리 계산
    #         distance = locations
    #         table[i][j] = distance
    #         table[j][i] = distance


    return table # A symmetric matrix of pairwise distances


def steepestAscent(p):
    current = randomInit(p)   # 'current' is a list of city ids
    valueC = evaluate(current, p)
    while True:
        neighbors = mutants(current, p)
        (successor, valueS) = bestOf(neighbors, p)
        if valueS >= valueC:
            break
        else:
            current = successor
            valueC = valueS
    return current, valueC


def randomInit(p):   # Return a random initial tour
    n = p[0]
    init = list(range(n))
    random.shuffle(init)
    return init


def evaluate(current, p): ###
    ## Calculate the tour cost of 'current'
    ## 'p' is a Problem instance
    ## 'current' is a list of city ids
    # p는 전체 정보를 의미함.
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

# 후보를 뽑아내기
def mutants(current, p): # Apply inversion
    n = p[0]
    neighbors = []
    count = 0
    triedPairs = []
    while count <= n:  # Pick two random loci for inversion
        i, j = sorted([random.randrange(n) for _ in range(2)])
        if i < j and [i, j] not in triedPairs:
            triedPairs.append([i, j])
            curCopy = inversion(current, i, j)
            count += 1
            neighbors.append(curCopy)
    return neighbors

def inversion(current, i, j):  ## Perform inversion
    curCopy = current[:]  # 복사하기
    while i < j:
        curCopy[i], curCopy[j] = curCopy[j], curCopy[i]  # 파이썬 장점: 임시 변수를 만들지 않고 이동
        i += 1
        j -= 1
    return curCopy

# 거리의 합이 가장 작은 것을 뽑아내면 됨.
def bestOf(neighbors, p): ###
    best = neighbors[0]
    bestValue = evaluate(best, p)  # best 값을 찾음 / bestValue는 현재값

    for i in range(1, len(neighbors)):
        newValue = evaluate(neighbors[i], p)

        if newValue < bestValue:  # 더 좋으면
            best = neighbors[i]
            bestValue = newValue 

    return best, bestValue

# 공통적으로 사용하는 함수는 '모듈화'해서 사용할 수 있음.

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

main()
