import unittest

from algs.prime.iterator import PrimeIterator
from algs.prime.prime import is_prime
from helpers.runner import run_with_elapse
from helpers.solution import Solution


def is_prime_factor(n, p) -> bool:
    return is_prime(p) and n % p == 0


class PrimeFactorization(Solution):
    pass


class NaivePrimeFactorization(PrimeFactorization):
    _iter: PrimeIterator

    def calculate(self, n: int) -> [int]:
        result = []
        while n >= 2:
            self._iter = PrimeIterator()
            p = self.find_prime_factor(n)
            n = n / p
            result.append(p)

        return result

    def find_prime_factor(self, n: int):
        p = self._iter.next()
        while not is_prime_factor(n, p):
            p = self._iter.next()

        return p


class TestFactorization(unittest.TestCase):
    def test_naive_factorization(self):
        naive = NaivePrimeFactorization()
        prime_factorization = naive.calculate

        self.assertEqual([2], prime_factorization(2))
        self.assertEqual([3], prime_factorization(3))
        self.assertEqual([2, 2], prime_factorization(4))
        self.assertEqual([5], prime_factorization(5))
        self.assertEqual([19], prime_factorization(19))
        self.assertEqual([2, 2, 5], prime_factorization(20))

        self.assertEqual(True, is_prime(941))
        self.assertEqual(True, is_prime(10627))

        run_with_elapse(prime_factorization, 20000014)
