import numpy as np


class RadioactiveAtom:
    def __init__(self, symbol,  half_life, unit='years'):
        self.symbol = symbol
        self.half_life = half_life
        self.unit = unit

    def get_decay_factor(self):
        return np.float_power(1 / 2, 1 / self.half_life)


def build_radioactive_collection():
    return [
        RadioactiveAtom('U 236', 12),
        RadioactiveAtom('U 237', 10),
    ]