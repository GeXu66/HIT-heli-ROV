import cv2 as cv
import time


class camera:
    def __init__(self):
        # self.video = cv.VideoCapture(0)
        self.video = cv.VideoCapture("new.mp4")
        if not self.video.isOpened():
            print("failed")
        # self.fps = self.video.get(cv.CAP_PROP_FPS)
        # self.size = (int(self.video.get(cv.CAP_PROP_FRAME_WIDTH)),
        #              int(self.video.get(cv.CAP_PROP_FRAME_HEIGHT)))
        # self.videoWriter = cv.VideoWriter('./record.avi', cv.VideoWriter_fourcc('I', '4', '2', '0'),
        #                                   self.fps, self.size)

    def get_picture(self):
        ret, frame = self.video.read()
        dst = cv.resize(frame, (640, 640))
        return dst

    def get_video(self, frame):
        pass
        # self.videoWriter.write(frame)

    def camera_release(self):
        self.video.release()
        # self.videoWriter.release()
        print("camera is closed")

    def re_open(self):
        if not self.video.isOpened():
            self.video = cv.VideoCapture(0)
            print("camera is open")


Camera = camera()
