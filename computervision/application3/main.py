from PyQt5 import QtWidgets, uic, QtGui  # import PyQt5 widgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from matplotlib import pyplot as plt
import cv2
import sys


qtcreator_file = "design.ui"  # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)
file_path = ""


class designWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.parcourir.clicked.connect(self.get_image)
        self.appliquer.clicked.connect(self.show_ImgHistEqualized)
        self.valider1.clicked.connect(self.show_ImgFiltered)
        self.valider2.clicked.connect(self.show_ImgThresholding)

    def get_image(self):
        global file_path
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open Image File', r"<Default dir>",
                                                   "Image files (*.jpg *.jpeg *.png)")
        img = cv2.imread(file_path)
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        h, w, ch = img.shape
        gray_image_qt = QtGui.QImage(gray_image.data, w, h, w, QImage.Format_Grayscale8)
        self.makeFigure('img1', QPixmap.fromImage(gray_image_qt))
        self.show_HistOriginal(gray_image)

    def makeFigure(self, widget_name, pixmap):

        pixmap = pixmap.scaled(self.findChild(QtWidgets.QLabel, widget_name).width(),
                               self.findChild(QtWidgets.QLabel, widget_name).height())
        self.findChild(QtWidgets.QLabel, widget_name).setPixmap(pixmap)

    def show_HistOriginal(self, img):
        hist = cv2.calcHist(img, [0], None, [256], [0, 256])
        # plot the histogram
        plt.figure()
        plt.title("Original Histogram")
        plt.plot(hist)
        plt.xlim([0, 256])
        plt.savefig('Original_Histogram.png')
        gray_hist = cv2.imread('Original_Histogram.png')
        h, w, ch = gray_hist.shape
        bytes_per_line = ch * w
        gray_hist_to_Qt_format = QtGui.QImage(gray_hist.data, w, h, bytes_per_line, QtGui.QImage.Format_BGR888)
        self.makeFigure('histimg1', QPixmap.fromImage(gray_hist_to_Qt_format))

    def show_ImgHistEqualized(self):
        img = cv2.imread(file_path)
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # generate the equalized image
        equalized_image = cv2.equalizeHist(gray_image)
        cv2.imwrite("Equalized_Image.png", equalized_image)
        h, w, ch = img.shape
        equalized_image_qt = QtGui.QImage(equalized_image.data, w, h, w, QImage.Format_Grayscale8)
        self.makeFigure('img2', QPixmap.fromImage(equalized_image_qt))
        # compute the histogram of the equalized image
        equalized_hist = cv2.calcHist(equalized_image, [0], None, [256], [0, 256])
        # plot the histogram
        plt.figure()
        plt.title("Equalized Histogram")
        plt.plot(equalized_hist)
        plt.xlim([0, 256])
        plt.savefig('Equalized_Histogram.png')
        gray_hist = cv2.imread('Equalized_Histogram.png')
        h, w, ch = gray_hist.shape
        bytes_per_line = ch * w
        gray_hist_to_Qt_format = QtGui.QImage(gray_hist.data, w, h, bytes_per_line, QtGui.QImage.Format_BGR888)
        self.makeFigure('histimg2', QPixmap.fromImage(gray_hist_to_Qt_format))

    def show_ImgFiltered(self):
        img = cv2.imread(file_path)
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # generate the filtered image
        if self.gaussian.isChecked():
            Filtered_image = cv2.GaussianBlur(gray_image, (5, 5), 3)
        elif self.average.isChecked():
            Filtered_image = cv2.blur(gray_image, (5, 5))
        elif self.median.isChecked():
            Filtered_image = cv2.medianBlur(gray_image, 5)
        else:
            Filtered_image=gray_image.copy()

        cv2.imwrite("Filtered_Image.png", Filtered_image)
        h, w, ch = img.shape
        Filtered_image_qt = QtGui.QImage(Filtered_image.data, w, h, w, QImage.Format_Grayscale8)
        self.makeFigure('img3', QPixmap.fromImage(Filtered_image_qt))

    def show_ImgThresholding(self):
        img = cv2.imread(file_path)
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # generate the thresholding image
        if self.binary.isChecked():
            ret, new_image = cv2.threshold(gray_image, 120, 255, cv2.THRESH_BINARY)
        elif self.otsu.isChecked():
            ret, new_image = cv2.threshold(gray_image, 120, 255, cv2.THRESH_OTSU)
        else:
            new_image=gray_image.copy()

        cv2.imwrite("Thresholding_Image.png", new_image)
        h, w, ch = img.shape
        new_image_qt = QtGui.QImage(new_image.data, w, h, w, QImage.Format_Grayscale8)
        self.makeFigure('img4', QPixmap.fromImage(new_image_qt))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = designWindow()
    window.show()
    sys.exit(app.exec_())
