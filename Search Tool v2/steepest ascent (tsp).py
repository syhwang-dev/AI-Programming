from tsp import *

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


def bestOf(neighbors, p): ###
    best = neighbors[0]
    bestValue = evaluate(best, p)  # best 값을 찾음 / bestValue는 현재값

    for i in range(1, len(neighbors)):
        newValue = evaluate(neighbors[i], p)

        if newValue < bestValue:  # 더 좋으면
            best = neighbors[i]
            bestValue = newValue 

    return best, bestValue

main()
