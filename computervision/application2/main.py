from os import listdir
from os.path import isfile, join
from PyQt5 import QtWidgets, uic,QtGui
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QPixmap
import cv2
import sys
qtcreator_file = "design.ui" # Enter file here.
Ui_MainWindow, QtBaseClass =uic.loadUiType(qtcreator_file)
file_path=""
class designWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.parcourir.clicked.connect(self.get_image)
        self.valider.clicked.connect(self.CompressedImg)
        self.Rimagesimilaire.clicked.connect(self.showSimilarImages)

    def makeFigure(self,widget_name,pixmap):
        pixmap=pixmap.scaled(self.findChild(QtWidgets.QLabel,widget_name).width(),self.findChild(QtWidgets.QLabel,widget_name).height())
        self.findChild(QtWidgets.QLabel,widget_name).setPixmap(pixmap)
    def get_image(self):
        global file_path
        file_path,_=QFileDialog.getOpenFileName(self,'Open Image File',r"<Defaultdir>","Image files(* JPG * jpeg * png)")
        img=cv2.imread(file_path)
        img_Qt_format=self.convert_cv_qt(img)
        self.makeFigure('imageoriginale',img_Qt_format)
    def convert_cv_qt(self, cv_image):
        h, w, ch = cv_image.shape
        bytes_per_line = ch * w
        cv_image_Qt_format = QtGui.QImage(cv_image.data, w, h, bytes_per_line, QtGui.QImage.Format_BGR888)
        return QPixmap.fromImage(cv_image_Qt_format)
    def compHistColor(self,img1,img2):
        hist1 = cv2.calcHist(img1, [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256,0, 256])
        hist2 = cv2.calcHist(img2, [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256,0, 256])
        cv2.normalize(hist1, hist1, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
        cv2.normalize(hist2, hist2, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
        dist = cv2.compareHist(hist1, hist2, 0)
        return dist
    def showSimilarImages(self):
        img = cv2.imread(file_path)
        fichiers = [f for f in listdir(file_path[0:file_path.rfind('/')]) if isfile(join(file_path[0:file_path.rfind('/')], f))]
        d=dict()
        for el in fichiers:
            if (el.find('.png')!=-1 or el.find('.jpg')!=-1):
                file_name=file_path[0:file_path.rfind('/')]+'/'+el
                img1=cv2.imread(file_name)
                d[file_name]=self.compHistColor(img, img1)

        l=sorted(d.items(), key=lambda t: t[1], reverse=True)

        img1=cv2.imread(l[1][0])
        img2 =cv2.imread(l[2][0])
        img3 =cv2.imread(l[3][0])
        img4 =cv2.imread(l[4][0])
        img_Qt_format = self.convert_cv_qt(img1)
        self.makeFigure('imagesimilaire1', img_Qt_format)
        self.imgs1.setText(str(l[1][1]))
        img_Qt_format = self.convert_cv_qt(img2)
        self.makeFigure('imagesimilaire2', img_Qt_format)
        self.imgs2.setText(str(l[2][1]))
        img_Qt_format = self.convert_cv_qt(img3)
        self.makeFigure('imagesimilaire3', img_Qt_format)
        self.imgs3.setText(str(l[3][1]))
        img_Qt_format = self.convert_cv_qt(img4)
        self.makeFigure('imagesimilaire4', img_Qt_format)
        self.imgs4.setText(str(l[4][1]))















    def CompressedImg(self):
        img = cv2.imread(file_path)
        if self.JPEG.isChecked():
            filename=file_path[0:len(file_path)-3]+"JPG"
            cv2.imwrite(filename, img)
            img2 = cv2.imread(filename)
            img_Qt_format = self.convert_cv_qt(img2)
            self.makeFigure('imagecompresse', img_Qt_format)
            psnr = cv2.PSNR(img, img2)
            self.imgc.setText("psnr="+str(psnr))
        else :
            filename = file_path[0:len(file_path) - 3] + "JP2"
            cv2.imwrite(filename, img)
            cv2.imwrite(filename, img)
            img2 = cv2.imread(filename)
            img_Qt_format = self.convert_cv_qt(img2)
            self.makeFigure('imagecompresse', img_Qt_format)
            psnr = cv2.PSNR(img, img2)
            self.imgc.setText("psnr="+str(psnr))










if __name__ == "__main__":
 app = QtWidgets.QApplication(sys.argv)
 window = designWindow()
 window.show()
 sys.exit(app.exec_())
