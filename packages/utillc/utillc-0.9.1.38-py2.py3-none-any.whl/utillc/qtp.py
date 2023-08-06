from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QFrame, QVBoxLayout, QHBoxLayout, QFormLayout, QGridLayout, QPushButton, QLineEdit, QSlider, QSpinBox, QCheckBox, QSizePolicy

from PyQt5.QtGui import QPixmap
import sys, os
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np
from utillc import *
import cv2
import threading

import queue


#EKOX(dir(mp_face_mesh))
import numpy as np

__all__ = ( 'video')


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    def __init__(self) :        
        super().__init__()        
        self.queue = queue.Queue(maxsize=50)

    def run(self):
        while True:
            image = self.queue.get()
            #EKOX(image is None)
            if not (image is None) :
                self.change_pixmap_signal.emit(image)

class App(QWidget):
    def foo(self, *arg, **kwargs):
        t = (arg[0].x(), arg[0].y())
        self.cb(t)
        #EKOX(t)
        self.queue.put(t)

    def key(self, *arg, **kwargs):
        EKOX(arg)
        EKOX(kwargs)
        
    def __init__(self, cb, title="demo"):
        super().__init__()
        self.queue = queue.Queue()
        self.cb = cb
        self.setWindowTitle(title)
        self.disply_width = 640
        self.display_height = 480
        # create the label that holds the image
        self.image_label = QLabel(self)
        self.image_label.resize(self.disply_width, self.display_height)
        # create a text label
        self.textLabel = QLabel('xxx')
        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)

        
        quit = QPushButton("Quit")
        quit.clicked.connect(lambda : (os._exit(), sys.exit(0)))
        self.counter = QLabel('')
        self.image_label.mousePressEvent = self.foo
        self.image_label.keyPressEvent = self.key
        self.image_label.keyReleaseEvent = self.key

        # create a vertical box layout and add the two labels
        hbox = QWidget()
        hbox.setLayout(QHBoxLayout())
        vbox.addWidget(hbox)

        hbox.layout().addWidget(self.textLabel)
        hbox.layout().addWidget(quit)
        hbox.layout().addWidget(self.counter)

        # set the vbox layout as the widgets layout
        self.setLayout(vbox)

        def update() :
            #EKOX(self.xRotationSlider.value())
            self.cb(self.xRotationSlider.value())
        
        self.xRotationSlider = QSlider(Qt.Horizontal)
        vbox.addWidget( self.xRotationSlider)
        self.xRotationSlider.valueChanged.connect(update)
        

        
        # create the video capture thread
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.thread.start()
        self.count=0


    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        self.count += 1
        self.counter.setText(str(self.count))
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

class GUI(threading.Thread):
    def __init__(self, cb) :
        super().__init__()
        self.queue = queue.Queue(maxsize=50)
        self.cb = cb
        pass
    def run(self) :
        EKO()
        app = QApplication(sys.argv)
        self.a = App(cb)
        self.a.show()
        self.queue.put(1)
        app.exec_()
        EKO()
    def push(self, image) :
        self.a.thread.queue.put(image)

    def go(self) :
        self.start()
        self.queue.get()
        

def video(cb) :
    gui = GUI(cb)
    gui.go()

    return gui

    
if __name__=="__main__":
    def cb(x) :
        EKOX(x)
    gui = video(cb)
    cap = cv2.VideoCapture(0)
    
    while cap.isOpened():
        success, image = cap.read()
        #EKOX(image is None)
        gui.push(image)
