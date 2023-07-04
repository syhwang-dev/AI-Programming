# 이 파일은 일종의 라이브러리이며, main()에서 가져다 씀.

import math
import random

# 기본 뼈대만 제공 - interface 역할
class Problem:
    # 기본적으로 호출되는 클래스
    def __init__(self):
        pass


class Numeric(Problem):
    def __init__(self):
        Problem.__init__(self)
    

class Tsp(Problem):
    def __init__(self):
        Problem.__init__(self)
