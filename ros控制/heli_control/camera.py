import cv2 as cv
import time


class camera:
    def __init__(self):
        self.video = cv.VideoCapture(0)
        # self.video = cv.VideoCapture("/home/heli/视频/Webcam/2021-03-29-203948.webm")
        if not self.video.isOpened():
            print("failed")

    def get_picture(self):
        ret, frame = self.video.read()
        dst = cv.resize(frame, (640, 640))
        return dst

    def get_video(self):

        fps = self.video.get(cv.CAP_PROP_FPS)
        a = time.time()
        b = time.time()
        size = (int(self.video.get(cv.CAP_PROP_FRAME_WIDTH)),
                int(self.video.get(cv.CAP_PROP_FRAME_HEIGHT)))

        videoWriter = cv.VideoWriter('./record.avi', cv.VideoWriter_fourcc('I', '4', '2', '0'),
                                     fps, size)
        success, frame = self.video.read()

        while success and (b - a) < 10:
            videoWriter.write(frame)
            b = time.time()
            success, frame = self.video.read()

    def camera_release(self):
        self.video.release()
        print("camera is closed")

    def re_open(self):
        if not self.video.isOpened():
            self.video = cv.VideoCapture(0)
            print("camera is open")


Camera = camera()
