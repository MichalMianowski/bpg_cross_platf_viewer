from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QFileDialog, QAction, QStatusBar
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QPixmap, QImage, QPicture
import sys
from PIL import Image
import imageio, numpy
import os
from pathlib import Path
import bpg

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.image as mpimg


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        self.list_of_files = list()
        self.last_file_id = 0

        uic.loadUi("window.ui", self)

        self.button_next = self.findChild(QPushButton, "pushButton_next")
        self.button_prev = self.findChild(QPushButton, "pushButton_prev")
        self.label = self.findChild(QLabel, "label")
        self.status_bar = self.findChild(QStatusBar, "statusbar")
        self.figure = Figure(facecolor='None')
        self.canvas = FigureCanvas(self.figure)
        self.gridLayout.addWidget(self.canvas, 0, 0, 1, 1)
        self.ax = self.figure.subplots()
        self.ax.set_axis_off()

        self.action_open.triggered.connect(self.open_file)
        self.action_save.triggered.connect(self.save_file)
        self.button_next.clicked.connect(self.next)
        self.button_prev.clicked.connect(self.prev)
        self.direction_next = 1
        self.number_of_fails = 0

        self.show()

    def open_file(self):
        fname = QFileDialog.getOpenFileName(self, "Open File", "All (*)")
        parent_directory = os.path.split(fname[0])
        if (self.list_of_files):
            self.list_of_files.clear()
        for file in Path(parent_directory[0]).iterdir():
            self.list_of_files.append(file)
        self.last_file_id = self.list_of_files.index(Path(fname[0]))
        self.open_image()

    def save_file(self):
        filepath = QFileDialog.getSaveFileName(self, 'Save File As')[0]
        # try:
        #     imageio.imsave(filepath, self.image_array)
        #     self.status_bar.showMessage(f"Image saved: {filepath.split()[-1]}")
        # except Exception as e:
        #     print(e)
        #     self.status_bar.showMessage(f"Can not save image")
        imageio.imsave(filepath, self.image_array)


    def open_image(self):
        self.status_bar.showMessage(self.list_of_files[self.last_file_id].parts[-1])
        self.ax.cla()
        try:
            self.image_array = imageio.imread(self.list_of_files[self.last_file_id])

            self.ax.imshow(self.image_array)
            if len(self.image_array.shape) == 2:
                self.ax.imshow(self.image_array, cmap='gray')

            self.ax.set_axis_off()
            self.canvas.draw()
            self.number_of_fails = 0
        except:
            print(f"Can not read: {self.list_of_files[self.last_file_id]}")
            self.number_of_fails += 1
            if(self.number_of_fails < len(self.list_of_files)):
                if self.direction_next:
                    self.next_index()
                else:
                    self.prev_index()
                self.open_image()
            else:
                self.status_bar.showMessage("No image file to open in this directory")

    def next(self):
        self.direction_next = 1
        self.next_index()
        try:
            self.open_image()
        except:
            self.next()

    def prev(self):
        self.direction_next = 0
        self.prev_index()
        try:
            self.open_image()
        except:
            self.prev()

    def next_index(self):
        if self.last_file_id + 1 < len(self.list_of_files):
            self.last_file_id += 1
        else:
            self.last_file_id = 0

    def prev_index(self):
        if self.last_file_id-1 >= 0:
            self.last_file_id -= 1
        else:
            self.last_file_id = len(self.list_of_files)-1


app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()

# [+] TODO dodaj na dole pasek z nazwą obecnie oglądanego pliku
# [+] TODO ogarnij wczytywanie wszystkich plików bez krzywizny i dzikich pikseli
# zapisuwanie?
# TODO dokończ zapisywanie do wskazanego formatu
# TODO dopiero później ogranicz możliwości wyboru formatu do tych wczytanych z imageio
# TODO dodaj opcję domyślną zapisywania obrazu

# Image has some pixels limit - when images are larger the browser is slow
# maybe load 3 images further and prev ?