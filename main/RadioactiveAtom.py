import numpy as np


class RadioactiveAtom:
    def __init__(self, symbol, name,  half_life, unit='years'):
        self.symbol = symbol
        self.name = name
        self.half_life = half_life
        self.unit = unit

    def get_decay_factor(self):
        return np.float_power(1 / 2, 1 / self.half_life)


class SeriesBuilder:
    def get_series_names(self):
        return ['Uranium', 'Actinium', 'Neptunium', 'Thorium']

    def get_series_by_name(self, name):
        if name == 'Uranium':
            return self._build_uranium_series()
        elif name == 'Actinium':
            return self._build_actinum_series()
        elif name == 'Neptunium':
            return self._build_neptunium_series()
        elif name == 'Thorium':
            return self._build_thorium_series()

    def _build_uranium_series(self):
        return [
            RadioactiveAtom('U 238', 'Uranium', 4.51, '10^9 years'),
            RadioactiveAtom('Th 234', 'Thorium', 24.10, 'd'),
            RadioactiveAtom('Pa 234', 'Protactinium', 1.18, '10^6 years'),
            RadioactiveAtom('U 234', 'Radon', 2.44, '10^5 years'),
            RadioactiveAtom('Th 230', 'Thorium', 7.50, '10^4 years'),
            RadioactiveAtom('Ra 226', 'Radium', 1.599, '10^3 years'),
            RadioactiveAtom('Rn 222', 'Radon', 3.823, 'd'),
            RadioactiveAtom('Po 218', 'Polonium', 3.05, 'min'),
            RadioactiveAtom('Pb 214', 'Lead', 26.8, 'min'),
            RadioactiveAtom('Bi 214', 'Bismuth', 19.7, 'min'),
            RadioactiveAtom('Po 214', 'Polonium', 162, 'ns'),
            RadioactiveAtom('Tl 210', 'Thallium', 1.32, 'min'),
            RadioactiveAtom('Pb 210', 'Lead', 22.3, 'years'),
            RadioactiveAtom('Bi 210', 'Bismuth', 5.0, 'd'),
            RadioactiveAtom('Po 210', 'Polonium', 138.375, 'd')
        ]

    def _build_actinum_series(self):
        return [
            RadioactiveAtom('U 235', 'Uranium', 6.96, '10^8 years'),
            RadioactiveAtom('Th 231', 'Thorium', 25.64, 'h'),
            RadioactiveAtom('Pa 231', 'Protactinium', 32.760, '10^3 years'),
            RadioactiveAtom('Ac 227', 'Actinium', 21.772, 'years'),
            RadioactiveAtom('Th 227', 'Thorium', 18.72, 'd'),
            RadioactiveAtom('Fr 223', 'Francium', 21.8, 'min'),
            RadioactiveAtom('Ra 223', 'Radium', 11.434, 'd'),
            RadioactiveAtom('Rn 219', 'Radon', 3.92, 's'),
            RadioactiveAtom('Po 215', 'Polonium', 1.78, 'ms'),
            RadioactiveAtom('Pb 211', 'Lead', 36.1, 'min'),
            RadioactiveAtom('Bi 211', 'Bismuth', 2.15, 'min'),
            RadioactiveAtom('Po 211', 'Polonium', 510, 'ms'),
            RadioactiveAtom('Tl 207', 'Thallium', 4.79, 'min'),
        ]

    def _build_neptunium_series(self):
        return [
            RadioactiveAtom('Np 237', 'Neptunium', 2.14, '10^6 years'),
            RadioactiveAtom('Pa 233', 'Protactinium', 27, 'd'),
            RadioactiveAtom('U 233', 'Uranium', 1.59, '10^5 years'),
            RadioactiveAtom('Th 229', 'Thorium', 7.340, '10^3 years'),
            RadioactiveAtom('Ra 225', 'Radium', 14.8, 'd'),
            RadioactiveAtom('Ac 225', 'Actinium', 10, 'd'),
            RadioactiveAtom('Fr 221', 'Francium', 4.8, 'min'),
            RadioactiveAtom('At 217', 'Astatine', 32.3, 'ms'),
            RadioactiveAtom('Bi 213', 'Bismuth', 46, 'min'),
            RadioactiveAtom('Po 213', 'Polonium', 4.2, '10^-6 s'),
            RadioactiveAtom('Tl 209', 'Thallium', 2.2, 'min'),
            RadioactiveAtom('Pb 209', 'Lead', 3.25, 'h'),
        ]

    def _build_thorium_series(self):
        return [
            RadioactiveAtom('Th 232', 'Thorium', 1.405, '10^10 years'),
            RadioactiveAtom('Ra 228', 'Radium', 5.75, 'years'),
            RadioactiveAtom('Ac 228', 'Actinium', 6.13, 'h'),
            RadioactiveAtom('Th 228', 'Thorium', 1.913, 'years'),
            RadioactiveAtom('Ra 224', 'Radium', 3.64, 'd'),
            RadioactiveAtom('Rn 220', 'Radon', 54.5, 's'),
            RadioactiveAtom('Po 216', 'Polonium', 158, 'ms'),
            RadioactiveAtom('Pb 212', 'Lead', 10.64, 'h'),
            RadioactiveAtom('Bi 212', 'Bismuth', 60.55, 'min'),
            RadioactiveAtom('Po 212', 'Polonium', 3, '10^-7 s'),
            RadioactiveAtom('Tl 208', 'Thallium', 3, 'min'),
        ]