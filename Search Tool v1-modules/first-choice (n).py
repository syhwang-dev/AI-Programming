from numeric import *

LIMIT_STUCK = 100

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

main()
