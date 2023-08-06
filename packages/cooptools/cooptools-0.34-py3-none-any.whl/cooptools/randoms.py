from typing import Dict, Any
import numpy.random as rnd

def weighted_random_choice(choices_dict: Dict[Any, float], seed: int = None):
    if seed is not None:
        rnd.seed(seed)

    total = sum([v for k, v in choices_dict.items()])
    selection_probs = [v / total for k, v in choices_dict.items()]

    return list(choices_dict)[rnd.choice(len(choices_dict), p=selection_probs)]

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)

    choices = {
        "a": 1,
        "b": 2,
        "c": 1.5,
        "d": 4
    }

    #TEST 1
    # rnd.seed(0)
    # ret = weighted_random_choice(choices)
    # print(ret)

    #TEST 2
    rets = {}
    for ii in range(0, 1000):
        ret = weighted_random_choice(choices)
        rets.setdefault(ret, 0)
        rets[ret] += 1

    for k, v in choices.items():
        print(f"{k} -- {v} ({round(v / sum([x for x in choices.values()]) * 100, 1)}%)")

    for k, v in rets.items():
        print(f"{k} -- {v} ({round(v / sum([x for x in rets.values()]) * 100, 1)}%)")


