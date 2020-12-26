from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QListWidget, QVBoxLayout
from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5.QtWidgets import QLabel, QGridLayout
from PyQt5.QtWidgets import QLineEdit, QPushButton, QHBoxLayout
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QCoreApplication as QC
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import sys


class HalfLife(QWidget):
    MAX_MC_SIZE = 1_000_000
    def __init__(self, parent=None):
        super(HalfLife, self).__init__(parent)

        self.build_interface()

    def build_interface(self):
        particle_label = QLabel("Select particle", self)
        self.particle_list = self.build_particles_list()
        batch_size_label = QLabel("Set MC batch size", self)
        self.batch_editor = QLineEdit()
        self.batch_editor.setValidator(QIntValidator(1, HalfLife.MAX_MC_SIZE))
        self.batch_editor.setPlaceholderText(QC.translate('', 'Default value: 100'))
        startBtn = QPushButton("&Plot", self)

        editor_grid = QGridLayout()
        editor_grid.addWidget(particle_label, 0, 0)
        editor_grid.addWidget(self.particle_list, 1, 0)
        editor_grid.addWidget(batch_size_label, 2, 0)
        editor_grid.addWidget(self.batch_editor, 3, 0)
        editor_grid.addWidget(startBtn, 4, 0)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        plot_layout = QVBoxLayout()
        plot_layout.addWidget(self.toolbar)
        plot_layout.addWidget(self.canvas)

        main_grid = QHBoxLayout()
        main_grid.addLayout(editor_grid)
        main_grid.addLayout(plot_layout)

        self.setLayout(main_grid)

        self.setGeometry(0, 0, 900, 600)
        self.setWindowTitle("Half Life")
        self.center_main_window()
        self.show()

    def build_particles_list(self):
        particle_list = QListWidget()
        particle_list.addItem("U 265")
        particle_list.addItem("U 267")
        return particle_list

    def center_main_window(self):
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HalfLife()
    sys.exit(app.exec_())