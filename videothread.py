import time
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self, video_src, video_type=None, parent=None):
        super().__init__(parent)
        self.video_src = video_src

    def run(self):
        cap = cv2.VideoCapture(self.video_src)
        while cap.isOpened():
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)

            time.sleep(0.001)
