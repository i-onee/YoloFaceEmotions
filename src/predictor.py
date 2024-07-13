# import required package 🚀
from signal import SIGINT, signal
from .utils import plotters
from ultralytics import YOLO
from cv2 import (
    CAP_PROP_FRAME_WIDTH,
    CAP_PROP_FRAME_HEIGHT,
    VideoCapture,
    imread,
    imshow,
    waitKey,
    destroyAllWindows,
)


class Predictor:
    def __init__(self, weight, conf=0.25):
        # setup confidence treshold
        self.__conf = conf

        # load models .pt
        self.__model = YOLO(weight)
        self.__model.fuse()

    def image(self, source):
        # load image from path
        image = imread(source)

        # predict & plot image
        predict = self.__model.predict(image, conf=self.__conf)
        plotted = plotters(predict, image)

        # show predicted image
        imshow("Yolo Face Emotions (Image Predictor)", plotted)
        waitKey(0)
        destroyAllWindows()

    def video_cam(self, source):
        # load video from path or camera
        capture = VideoCapture(source)

        # initialize frame dimensions for better window
        capture.set(CAP_PROP_FRAME_WIDTH, 1280)
        capture.set(CAP_PROP_FRAME_HEIGHT, 720)

        # handling signals for keyboard interupt
        signal(SIGINT, lambda s, f: (capture.release(), destroyAllWindows()))

        while capture.isOpened():
            try:
                # get frame from video
                _, frame = capture.read()

                # predict and plot frame
                predict = self.__model.predict(frame, conf=self.__conf)
                plotted = plotters(predict, frame)

                # show plotted frame
                imshow("Yolo Face Emotions (Video Predictor)", plotted)
                if waitKey(5) and 0xFF == 27:
                    break
            except KeyboardInterrupt:
                pass
