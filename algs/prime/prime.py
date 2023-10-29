import math
import unittest


def is_prime(n: int) -> bool:
    if n < 4:
        return True

    s_root = int(math.sqrt(n))
    for i in range(2, s_root + 1):
        if n % i == 0:
            return False
    return True


class TestPrime(unittest.TestCase):
    def test_is_prime(self):
        self.assertEqual(is_prime(2), True)
        self.assertEqual(is_prime(4), False)
        self.assertEqual(is_prime(117), False)
