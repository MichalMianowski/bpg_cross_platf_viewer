import sys
import numpy as np

from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

#
# class MplCanvas(FigureCanvasQTAgg):
#
#     def __init__(self, parent=None, width=5, height=4, dpi=100):
#         fig = Figure(figsize=(width, height), dpi=dpi)
#         self.axes = fig.add_subplot(111)
#         super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.figure = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.subplots()

        # delta = 0.025
        # x = y = np.arange(-3.0, 3.0, delta)
        # X, Y = np.meshgrid(x, y)
        # Z1 = np.exp(-(X ** 2) - Y ** 2)
        # Z2 = np.exp(-((X - 1) ** 2) - (Y - 1) ** 2)
        # Z = (Z1 - Z2) * 2

        # self.ax.imshow(Z)
        # self.ax.set_axis_off()

        self.figure = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.subplots()
        img = mpimg.imread('image_test_2.jpg')
        # imgplot = plt.imshow(img)
        self.ax.imshow(img)
        self.ax.set_axis_off()

        self.setCentralWidget(self.canvas)


# app = QtWidgets.QApplication(sys.argv)
# w = MainWindow()
# app.exec_()

app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
w.resize(640, 480)
w.show()

sys.exit(app.exec_())