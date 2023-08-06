import cv2
from videocv.timer import Timer


class Camera:
    def __init__(self, index):
        cap = cv2.VideoCapture(index)
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.cap = cap
        self.fps = fps
        self.size = (width, height)

        self.timer = Timer()
        self.latency = self.timer.latency

    def __call__(self):
        success, frame = self.cap.read()
        self.frame = frame

        self.latency = self.timer()

        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            return False
        return success

    def __del__(self):
        self.cap.release()
