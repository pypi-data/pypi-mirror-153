import math
from typing import List
import itertools

def flattened_list_of_lists(list_of_lists: List[List], unique: bool = False) -> List:
    flat = list(itertools.chain.from_iterable(list_of_lists))

    if unique:
        flat = list(set(flat))

    return flat

def all_indxs_in_lst(lst: List, value) -> List[int]:
    idxs = []
    idx = -1
    while True:
        try:
            idx = lst.index(value, idx + 1)
            idxs.append(idx)
        except ValueError as e:
            break
    return idxs

def next_perfect_square_rt(n: int) -> int:
    int_root_n = int(math.sqrt(n))
    if int_root_n == n:
        return n
    return int_root_n + 1

if __name__ == "__main__":
    # import random as rnd
    # l_o_l = [[x for x in range(rnd.randint(5, 10))] for y in range(rnd.randint(5, 10))]
    #
    # print(l_o_l)
    # print(flattened_list_of_lists(l_o_l))
    # print(flattened_list_of_lists(l_o_l, unique=True))

    print(next_perfect_square(9))