from helpers.runner import run_with_elapse


class Solution:
    def calculate(self, *args):
        pass


class TestSolution(Solution):
    def test_run(self):
        def fib(n):
            if n < 3:
                return 1
            return fib(n - 1) + fib(n - 2)

        fib(36)

    def calculate(self):
        self.test_run()


if __name__ == "__main__":
    run_with_elapse(TestSolution())
