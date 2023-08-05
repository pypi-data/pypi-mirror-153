import cv2
import matplotlib.pyplot as plt
import numpy as np


class Recorder(object):
    def __init__(self,
                 video_path: str = None,
                 ):
        """
        This class handles the recording of a video which consists of frames generated from the passed matplotlib
        figure by the add_frame method.
        :param video_path: full path to output video
        """
        self.video_path = video_path
        self._frame_counter = 0
        self.__video: cv2.VideoWriter = None

    def add_frame(self, fig: plt.figure = None):
        fig.canvas.draw()
        fig.canvas.flush_events()
        img = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        img = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        if self._frame_counter == 0:
            # initialize recorder
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            height, width, layers = img.shape
            self.__video = cv2.VideoWriter(self.video_path, fourcc, 1, (width, height))
        self.__video.write(img)
        self._frame_counter += 1

    def end_recording(self):
        self.__video.release()
        print('A total of {:} frames were added to {:}'.format(
            self._frame_counter,
            self.video_path))
