import sys

import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtCore import QCoreApplication as QC
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QListWidget, QVBoxLayout
from PyQt5.QtWidgets import QLabel, QGridLayout
from PyQt5.QtWidgets import QLineEdit, QPushButton, QHBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from RadioactiveAtom import SeriesBuilder


class HalfLife(QWidget):
    MAX_MC_SIZE = 1_000_000
    DEF_MC_SIZE = 100
    SIM_END_RATIO = 0.01

    def __init__(self, series_builder, parent=None):
        super(HalfLife, self).__init__(parent)

        self.builder = series_builder
        self.build_atoms_mapping(series_builder.get_series_by_name(builder.get_series_names()[0]))
        self.build_interface()
        self.plot()

    def build_atoms_mapping(self, atoms):
        atom_map = dict()
        for a in atoms:
            atom_map[a.symbol] = a
        self.atoms_map = atom_map

    def build_interface(self):
        editor_grid = self.build_editor()
        plot_layout = self.build_plot_area()
        main_grid = QHBoxLayout()
        main_grid.addLayout(editor_grid)
        main_grid.addLayout(plot_layout)
        self.setLayout(main_grid)

        self.setGeometry(0, 0, 900, 600)
        self.setWindowTitle("Half Life")
        self.center_main_window()
        self.show()

    def build_editor(self):
        series_label = QLabel("Select series", self)
        self.series_list = self.build_series_list()
        self.series_list.setCurrentRow(0)
        atoms_label = QLabel("Select atom", self)
        self.atoms_list = self.build_atom_list()
        self.atoms_list.setCurrentRow(0)
        batch_size_label = QLabel("Set MC batch size", self)
        self.batch_editor = QLineEdit()
        self.batch_editor.setValidator(QIntValidator(1, HalfLife.MAX_MC_SIZE))
        self.batch_editor.setPlaceholderText(QC.translate('', f'Default value: {HalfLife.DEF_MC_SIZE}'))
        startBtn = QPushButton("&Plot", self)
        startBtn.clicked.connect(self.plot)
        self.series_list.currentItemChanged.connect(self.change_series)
        editor_layout = QVBoxLayout()
        editor_layout.addWidget(series_label)
        editor_layout.addWidget(self.series_list)
        editor_layout.addWidget(atoms_label)
        editor_layout.addWidget(self.atoms_list)
        editor_layout.addWidget(batch_size_label)
        editor_layout.addWidget(self.batch_editor)
        editor_layout.addWidget(startBtn)
        return editor_layout

    def build_series_list(self):
        series = QListWidget()
        series.addItems(self.builder.get_series_names())
        return series

    def build_atom_list(self):
        atom_list = QListWidget()
        atom_list.addItems(self.atoms_map.keys())
        return atom_list

    def center_main_window(self):
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    def change_series(self):
        selected_series = self.series_list.currentItem().text()
        self.build_atoms_mapping(self.builder.get_series_by_name(selected_series))
        self.atoms_list.clear()
        self.atoms_list.addItems(self.atoms_map.keys())
        self.atoms_list.setCurrentRow(0)

    def build_plot_area(self):
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        plot_layout = QVBoxLayout()
        plot_layout.addWidget(self.toolbar)
        plot_layout.addWidget(self.canvas)
        return plot_layout

    def plot(self):
        MC_sim_size, atom = self.read_plot_parameters()
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        self.plot_simulation(MC_sim_size, atom, ax)
        self.plot_theory(atom, ax)
        ax.legend()
        ax.set_xlabel(atom.unit)
        ax.set_ylabel('N')
        ax.set_title(f'{atom.name} {atom.symbol}   T_1/2 = {atom.half_life} {atom.unit}')
        self.canvas.draw()

    def read_plot_parameters(self):
        MC_sim_size = HalfLife.DEF_MC_SIZE
        MC_size_str = self.batch_editor.text()
        if MC_size_str != '':
            MC_sim_size = int(MC_size_str)
        atom_symbol = self.atoms_list.selectedItems()[0].text()
        atom = self.atoms_map[atom_symbol]
        return MC_sim_size, atom

    def plot_theory(self, atom, ax):
        N = 1
        t = 0
        theory_data = [N]
        step = atom.get_decay_factor()
        while N > HalfLife.SIM_END_RATIO:
            t += 1
            N = N * step
            theory_data.append(N)
        ax.plot(theory_data, '-', label='theory', alpha=0.7)

    def plot_simulation(self, MC_sim_size, atom, ax):
        current_MC = MC_sim_size
        sim = [1]
        P = 1 - atom.get_decay_factor()
        while current_MC > HalfLife.SIM_END_RATIO * MC_sim_size:
            for _ in range(current_MC):
                if np.random.random() < P:
                    current_MC -= 1
            sim.append(current_MC / MC_sim_size)
        ax.plot(sim, '.', label='simulation', alpha=0.5)


if __name__ == '__main__':
    builder = SeriesBuilder()
    app = QApplication(sys.argv)
    window = HalfLife(builder)
    sys.exit(app.exec_())
