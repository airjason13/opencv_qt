import time

from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np
import subprocess


FFMPEG_BIN = 'ffmpeg'


class VideoThreadFFMpeg(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    ffmpeg_change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self, video_src, display_width, display_height, video_type=None, parent=None):
        super().__init__(parent)
        self.video_src = video_src
        self.display_width = display_width
        self.display_height = display_height

    def run(self):
        scale_factor = "scale=" + str(self.display_width) + ":" + str(self.display_height)
        command = [FFMPEG_BIN,
                   '-hide_banner',
                   '-loglevel', 'error',
                   '-hwaccel', 'auto',
                   '-re',
                   '-i', self.video_src,
                   '-f', 'image2pipe',
                   '-pix_fmt', 'rgb24',
                   '-vcodec', 'rawvideo', '-vf', scale_factor, '-']
        pipe = subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=10 ** 8)
        while True:
            try:
                self.raw_image = pipe.stdout.read(self.display_width * self.display_height * 3)
                # transform the byte read into a numpy array
                image = np.fromstring(self.raw_image, dtype='uint8')
                image = image.reshape((self.display_height, self.display_width, 3))
                # throw away the data in the pipe's buffer.
                pipe.stdout.flush()

                self.ffmpeg_change_pixmap_signal.emit(image)
            except Exception as e:
                pass
                # print("[ERROR] ", e)

            # time.sleep(0.033)
