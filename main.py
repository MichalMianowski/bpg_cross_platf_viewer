from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QFileDialog, QAction
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QPixmap, QImage, QPicture
import sys
from PIL import Image
import imageio, numpy
import os
from pathlib import Path

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.image as mpimg

# Image has some pixels limit - when images are larger the browser is slow
# maybe load 3 images further and prev ?


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        self.list_of_files = list()
        self.last_file_id = 0

        uic.loadUi("window_2.ui", self)

        self.button_next = self.findChild(QPushButton, "pushButton_next")
        self.button_prev = self.findChild(QPushButton, "pushButton_prev")
        self.label = self.findChild(QLabel, "label")
        self.figure = Figure(facecolor='None')
        self.canvas = FigureCanvas(self.figure)
        self.gridLayout.addWidget(self.canvas, 0, 0, 1, 1)
        self.ax = self.figure.subplots()
        self.ax.set_axis_off()

        self.action_open.triggered.connect(self.open_file)
        self.action_save.triggered.connect(self.save_file)
        self.button_next.clicked.connect(self.next)
        self.button_prev.clicked.connect(self.prev)
        self.image_array = []

        self.show()

    # def resizeEvent(self, event):
    #     self.pixmap = self.pixmap.scaled(self.width(), self.height())
    #     self.label.setPixmap(self.pixmap)
    #     self.label.resize(self.width(), self.height())

    def open_file(self):
        fname = QFileDialog.getOpenFileName(self, "Open File", "All (*)")
        parent_directory = os.path.split(fname[0])
        for file in Path(parent_directory[0]).iterdir():
            self.list_of_files.append(file)
        self.last_file_id = self.list_of_files.index(Path(fname[0]))
        self.open_image()

    def save_file(self):
        name = QFileDialog.getSaveFileName(self, 'Save File', filter='Images (*.png *.jpg)')
        file = open(name[0], 'w')
        print(file)
        # print(name)

    '''
    def open_image(self):
        self.image_array = imageio.imread(self.list_of_files[self.last_file_id])
        print("image readed")
        if Image.MAX_IMAGE_PIXELS < self.image_array.size:
            print("jest mniejszy limit!")
            Image.MAX_IMAGE_PIXELS = self.image_array.size
        # # opcja A
        # im = Image.fromarray(self.image_array)
        # im.convert('RGB')
        # data = im.tobytes('raw', 'RGB')
        # qim = QImage(data, im.size[0], im.size[1], QImage.Format_RGB888)
        # self.pixmap = QPixmap(QPixmap.fromImage(qim))
        # self.label.setPixmap(self.pixmap)

        # # opcja B
        # qim = QImage(self.image_array, self.image_array.shape[1], self.image_array.shape[0], QImage.Format_RGB888)
        # self.pixmap = QPixmap(QPixmap.fromImage(qim))
        # self.label.setPixmap(self.pixmap)

        # # opcja C
        # cvImg = self.image_array
        # height, width, channel = cvImg.shape
        # bytesPerLine = 3 * width
        # qim = QImage(cvImg.data, width, height, bytesPerLine, QImage.Format_RGB888)

        # self.pixmap = QPixmap(QPixmap.fromImage(qim))
        # self.pixmap = self.pixmap.scaled(self.label.size() , QtCore.Qt.KeepAspectRatio)
        # self.label.setPixmap(self.pixmap)

        # opcja D
        from PIL import Image as Image_pil
        image_from_array = Image_pil.fromarray(self.image_array)
        self.pixmap = QPixmap(image_from_array)
        # picture = QPicture(image_from_array)
        self.label.setPicture(image_from_array)
    '''

    def open_image(self):
        try:
            self.image_array = imageio.imread(self.list_of_files[self.last_file_id])
            # # img = mpimg.imread('image_test_2.jpg')
            # img = imageio.imread('image_test_2.jpg')

            self.ax.imshow(self.image_array)
            if len(self.image_array.shape) == 2:
                self.ax.imshow(self.image_array, cmap='gray')

            self.ax.set_axis_off()
            self.canvas.draw()
            # self.setCentralWidget(self.canvas)
        except:
            print(f"error in reading: {self.list_of_files[self.last_file_id]}")
            self.next_index()
            self.open_image()

    def save_image(self):
        pass

    def next(self):
        print("open next file")
        self.next_index()
        try:
            self.open_image()
        except:
            self.next()

    def prev(self):
        print("open prev file")
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

# TODO dodaj na dole pasek z nazwą obecnie oglądanego pliku
# TODO ogarnij wczytywanie wszystkich plików bez krzywizny i dzikich pikseli
# TODO dokończ zapisywanie do wskazanego formatu
# TODO dopiero później ogranicz możliwości wyboru formatu do tych wczytanych z imageio
# TODO dodaj opcję domyślną zapisywania obrazu