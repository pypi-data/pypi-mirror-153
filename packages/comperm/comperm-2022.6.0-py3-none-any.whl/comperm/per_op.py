# coding=utf-8
#
# per_op.py in comperm
# created by 谢方圆 (XIE Fangyuan) on 2022-05-28
# Copyright © 2022 谢方圆 (XIE Fangyuan). All rights reserved.
#
# Permutation operations.


from functools import reduce
from typing import NoReturn

from comperm.combinatorics_op import CombinatoricsOp


class PerOp(CombinatoricsOp):
    @classmethod
    def get_num(cls, n: int, k: int) -> int | NoReturn:
        """Calculate the number of permutations given n and k.

        Args:
            n: Total number of elements.
            k: Number of chosen elements.

        Returns:
            Number of permutations.
        """
        cls._check_n_k(n=n, k=k)
        return reduce(lambda num, i: num * (n - i), range(k), 1)

    @classmethod
    def ordinal_to_permutation(
            cls,
            n: int,
            k: int,
            o: int
    ) -> list[int] | NoReturn:
        """Find the permutation given n, k and its lexicographical ordinal.

        Args:
            n: Total number of elements.
            k: Number of chosen elements.
            o: Lexicographical ordinal of a permutation.

        Returns:
            A permutation.
        """
        cls._check_ordinal(n=n, k=k, o=o)

        permutation, total, num = [0] * k, n, cls.get_num(n=n, k=k)
        for i in range(k):
            num, n, k, p = num // n, n - 1, k - 1, 1
            while p in permutation[:i]:
                p += 1
            while o >= num:
                o, p = o - num, p + 1
                while p in permutation[:i]:
                    p += 1
            permutation[i] = p
        return permutation

    @classmethod
    def permutation_to_ordinal(
            cls,
            n: int,
            permutation: list[int]
    ) -> int | NoReturn:
        """Find the lexicographical ordinal of a permutation given n, k.

        Args:
            n: Total number of elements.
            permutation: A permutation of k elements.

        Returns:
            Lexicographical ordinal of the permutation.
        """
        cls._check_permutation(n=n, permutation=permutation)

        o, total, num = 0, n, cls.get_num(n=n, k=(k := len(permutation)))
        for i, p in enumerate(permutation):
            num, n, k = num // n, n - 1, k - 1
            o += num * (p - 1 - sum(x < p for x in permutation[:i]))
        return o

    @classmethod
    def _check_permutation(cls, n: int, permutation: list[int]) -> NoReturn:
        """Check that a permutation is valid.

        Args:
            n: Total number of elements.
            permutation: A permutation of k elements.
        """
        cls._check_n_k(n=n, k=len(permutation))
        for p in permutation:
            assert 1 <= p <= n, \
                f'{p=} should be a natural number within [1, {n=}].'
        assert len(permutation) == len(set(permutation)), \
            f'All the elements in a permutation should be distinct.'
