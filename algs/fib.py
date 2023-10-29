from algs.squence_formula import SequenceFormulaSolution
from helpers.runner import run_with_elapse


class FibSolution(SequenceFormulaSolution):
    def __init__(self):
        self.init_cache({1: 1, 2: 1})

    def calculate(self, i) -> int:
        return self.get_cache(i - 1) + self.get_cache(i - 2)


class Fib3Solution(SequenceFormulaSolution):
    def __init__(self):
        self.init_cache({1: 1, 2: 1, 3: 1})

    def calculate(self, i) -> int:
        return self.get_cache(i - 1) + self.get_cache(i - 2) + self.get_cache(i - 3)


def fib(n):
    f = [1, 1]
    skip = len(f)
    for i in range(skip, n):
        f.append(f[i-1] + f[i-2])
    return f[n - 1]


if __name__ == '__main__':
    run_with_elapse(FibSolution().calculate, 20000)
    # run(Fib3Solution().call, 400)
    run_with_elapse(fib, 20000)
