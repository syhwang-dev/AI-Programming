from numeric import *

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

def mutants(current, p): ###
    neighbors = []
    for i in range(len(current)):
        mutant = mutate(current, i, DELTA, p)
        neighbors.append(mutant)
        mutant = mutate(current, i, -DELTA, p)
        neighbors.append(mutant)


    # 총 10개 출력?
    return neighbors     # Return a set of successors


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

main()
