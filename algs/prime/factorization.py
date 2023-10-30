import math
import unittest

from algs.prime.prime import is_prime


def is_prime_factor(n, p) -> bool:
    return is_prime(p) and n % p == 0


def naive_prime_factorization(n: int) -> [int]:
    result = []
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:  # 如果 i 能够整除 n，说明 i 为 n 的一个质因子。
            while n % i == 0:
                n //= i
                result.append(i)
    if n != 1:  # 说明再经过操作之后 n 留下了一个素数
        result.append(n)
    return result


class TestFactorization(unittest.TestCase):
    def test_naive_factorization(self):
        prime_factorization = naive_prime_factorization

        self.assertEqual([2], prime_factorization(2))
        self.assertEqual([3], prime_factorization(3))
        self.assertEqual([2, 2], prime_factorization(4))
        self.assertEqual([5], prime_factorization(5))
        self.assertEqual([19], prime_factorization(19))
        self.assertEqual([2, 2, 5], prime_factorization(20))
        self.assertEqual([2, 353, 283286119], prime_factorization(200000000014))
        self.assertEqual(True, 2 * 253 * 283286119 * 2 > 200000000014)

        self.assertEqual(True, is_prime(941))
        self.assertEqual(True, is_prime(10627))
        self.assertEqual(True, is_prime(283286119))
