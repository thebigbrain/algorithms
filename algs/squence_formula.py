from helpers.solution import Solution


class SequenceFormulaSolution(Solution):
    _cache = {
    }

    def init_cache(self, cache):
        self._cache = cache

    def set_cache(self, k, v):
        self._cache[k] = v

    def get_cache_size(self):
        return len(self._cache)

    def get_cache(self, n) -> int:
        return self._cache[n]

    def is_in_cache(self, i) -> bool:
        return i <= self.get_cache_size()

    def calculate(self, i) -> int:
        pass

    def fill_in_cache_if_not_exist(self, i):
        if not self.is_in_cache(i):
            self.set_cache(i, self.calculate(i))

    def calculate(self, n: int) -> int:
        for i in range(1, n + 1):
            self.fill_in_cache_if_not_exist(i)
        return self.get_cache(n)

