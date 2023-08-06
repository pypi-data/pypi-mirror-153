# coding=utf-8
#
# com_op.py in comperm
# created by 谢方圆 (XIE Fangyuan) on 2022-05-27
# Copyright © 2022 谢方圆 (XIE Fangyuan). All rights reserved.
#
# Combination operations.


from functools import reduce
from itertools import pairwise
from typing import NoReturn

from comperm.combinatorics_op import CombinatoricsOp


class ComOp(CombinatoricsOp):
    @classmethod
    def get_num(cls, n: int, k: int) -> int | NoReturn:
        """Calculate the number of combinations given n and k.

        Args:
            n: Total number of elements.
            k: Number of chosen elements.

        Returns:
            Number of combinations.
        """
        cls._check_n_k(n=n, k=k)
        return reduce(lambda num, i: num * (n - i) // (i + 1), range(k), 1)

    @classmethod
    def ordinal_to_combination(
            cls,
            n: int,
            k: int,
            o: int
    ) -> list[int] | NoReturn:
        """Find the combination given n, k and its lexicographical ordinal.

        Args:
            n: Total number of elements.
            k: Number of chosen elements.
            o: Lexicographical ordinal of a combination.

        Returns:
            A combination.
        """
        cls._check_ordinal(n=n, k=k, o=o)

        combination, total, num = [0] * k, n, cls.get_num(n=n, k=k)
        for i in range(k):
            num, n, k = num * k // n, n - 1, k - 1
            while o >= num:
                o, num, n = o - num, num * (n - k) // n, n - 1
            combination[i] = total - n
        return combination

    @classmethod
    def combination_to_ordinal(
            cls,
            n: int,
            combination: list[int]
    ) -> int | NoReturn:
        """Find the lexicographical ordinal of a combination given n, k.

        Args:
            n: Total number of elements.
            combination: A combination of k elements.

        Returns:
            Lexicographical ordinal of the combination.
        """
        cls._check_combination(n=n, combination=combination)

        o, total, num = 0, n, cls.get_num(n=n, k=(k := len(combination)))
        for c in combination:
            num, n, k = num * k // n, n - 1, k - 1
            while c > total - n:
                o, num, n = o + num, num * (n - k) // n, n - 1
        return o

    @classmethod
    def _check_combination(cls, n: int, combination: list[int]) -> NoReturn:
        """Check that a combination is valid.

        Args:
            n: Total number of elements.
            combination: A combination of k elements.
        """
        cls._check_n_k(n=n, k=len(combination))

        for c in combination:
            assert 1 <= c <= n, \
                f'{c=} should be a natural number within [1, {n=}].'
        for c1, c2 in pairwise(combination):
            assert c1 < c2, f'{c1} >= {c2}, elements in a combination ' \
                            f'should be in strictly increasing order.'
