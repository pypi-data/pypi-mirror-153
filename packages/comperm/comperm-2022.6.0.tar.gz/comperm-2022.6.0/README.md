# ComPerm

Version `2022.6.0`

Combination and permutation operations.

## Installation

```shell
pip install comperm
```

## Combination Operations

```python
from comperm.com_op import ComOp

# Get the number of combinations given n and k
print(ComOp.get_num(n=5, k=2))  # 10

# Get the lexicographical ordinal of a combination given n
print(ComOp.combination_to_ordinal(n=5, combination=[2, 3]))  # 4

# Get the combination given n, k and its lexicographical ordinal
print(ComOp.ordinal_to_combination(n=5, k=2, o=4))  # [2, 3]
```

## Permutation Operations

```python
from comperm.per_op import PerOp

# Get the number of permutations given n and k
print(PerOp.get_num(n=5, k=2))  # 20

# Get the lexicographical ordinal of a permutation given n
print(PerOp.permutation_to_ordinal(n=5, permutation=[2, 3]))  # 5

# Get the permutation given n, k and its lexicographical ordinal
print(PerOp.ordinal_to_permutation(n=5, k=2, o=5))  # [2, 3]
```

## Unit Test

Run testcases in all files:

```shell
PYTHONPATH='src' python -m unittest discover -s tests
```

Run testcases in a file:

```shell
python -m unittest tests/test_combinatorics_op.py
python -m unittest tests/test_com_op.py
python -m unittest tests/test_per_op.py
```
