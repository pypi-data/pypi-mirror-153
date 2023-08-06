# coding=utf-8
#
# combinatorics_op.py in comperm
# created by 谢方圆 (XIE Fangyuan) on 2022-05-27
# Copyright © 2022 谢方圆 (XIE Fangyuan). All rights reserved.
#
# Combinatorics operations.


from abc import ABCMeta, abstractmethod
from typing import NoReturn


class CombinatoricsOp(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def get_num(cls, n: int, k: int) -> NoReturn:
        """Calculate the number of combinations or permutations given n and k.
        This function must be overridden.

        Args:
            n: Total number of elements.
            k: Number of chosen elements.
        """
        raise NotImplementedError

    @staticmethod
    def _check_n_k(n: int, k: int) -> NoReturn:
        """Check that n and k are valid.

        Args:
            n: Total number of elements.
            k: Number of chosen elements.
        """
        assert n >= 0, f'{n=} should be a natural number.'
        assert 0 <= k <= n, \
            f'{k=} should be a natural number within [0, {n=}].'

    @classmethod
    def _check_ordinal(cls, n: int, k: int, o: int) -> NoReturn:
        """Check that n, k and o are valid.

        Args:
            n: Total number of elements.
            k: Number of chosen elements.
            o: Lexicographical ordinal of a combination or permutation.
        """
        num = cls.get_num(n=n, k=k)
        assert 0 <= o < num, \
            f'{o=} should be a natural number within [0, {num=}).'
