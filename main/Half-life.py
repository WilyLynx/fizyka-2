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

from main.RadioactiveAtom import build_radioactive_collection


class HalfLife(QWidget):
    MAX_MC_SIZE = 1_000_000
    DEF_MC_SIZE = 100
    SIM_END_RATIO = 0.01

    def __init__(self, atoms, parent=None):
        super(HalfLife, self).__init__(parent)

        self.build_atoms_mapping(atoms)
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

    def build_plot_area(self):
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        plot_layout = QVBoxLayout()
        plot_layout.addWidget(self.toolbar)
        plot_layout.addWidget(self.canvas)
        return plot_layout

    def build_editor(self):
        particle_label = QLabel("Select particle", self)
        self.atoms_list = self.build_particles_list()
        self.atoms_list.setCurrentRow(0)
        batch_size_label = QLabel("Set MC batch size", self)
        self.batch_editor = QLineEdit()
        self.batch_editor.setValidator(QIntValidator(1, HalfLife.MAX_MC_SIZE))
        self.batch_editor.setPlaceholderText(QC.translate('', f'Default value: {HalfLife.DEF_MC_SIZE}'))
        startBtn = QPushButton("&Plot", self)
        startBtn.clicked.connect(self.plot)
        editor_grid = QGridLayout()
        editor_grid.addWidget(particle_label, 0, 0)
        editor_grid.addWidget(self.atoms_list, 1, 0)
        editor_grid.addWidget(batch_size_label, 2, 0)
        editor_grid.addWidget(self.batch_editor, 3, 0)
        editor_grid.addWidget(startBtn, 4, 0)
        return editor_grid

    def build_particles_list(self):
        particle_list = QListWidget()
        particle_list.addItems(self.atoms_map.keys())
        return particle_list

    def center_main_window(self):
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    def plot(self):
        MC_sim_size, atom = self.read_plot_parameters()
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        self.plot_simulation(MC_sim_size, atom, ax)
        self.plot_theory(atom, ax)
        ax.legend()
        ax.set_xlabel(atom.unit)
        ax.set_ylabel('N')
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
    atoms = build_radioactive_collection()
    app = QApplication(sys.argv)
    window = HalfLife(atoms)
    sys.exit(app.exec_())
