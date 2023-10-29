from algs.prime.prime import is_prime


class PrimeIterator:
    def __init__(self):
        self._current = 2

    def next(self) -> int:
        n = self._current
        self._advance()
        return n

    def _advance(self):
        while True:
            self._current += 1
            if is_prime(self._current):
                break
