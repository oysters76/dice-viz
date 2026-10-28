import math

import numpy as np


def roll(n=6):
    return np.random.randint(1, n + 1)


def experiment(n=6, dices=1, rolls=10000):
    values = []
    for _ in range(0, rolls):
        s = 0
        for _ in range(dices):
            s += roll(n)
        values.append(s)
    return np.array(values)


def theoretical_stats(num_dice: int, faces: int) -> tuple[float, float]:
    mu = num_dice * (faces + 1) / 2
    sigma = math.sqrt(num_dice * (faces**2 - 1) / 12)
    return mu, sigma
