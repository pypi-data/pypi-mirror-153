import cv2


class Video:
    def __init__(self, video_file):
        cap = cv2.VideoCapture(video_file)
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.cap = cap
        self.fps = fps
        self.size = (width, height)

    def __call__(self):
        success, frame = self.cap.read()
        self.frame = frame

        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            return False
        return success

    def __del__(self):
        self.cap.release()


class Writer:
    def __init__(self, video_file, fps, size):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.writer = cv2.VideoWriter(video_file, fourcc, fps, size)

    def __call__(self, image):
        self.writer.write(image)

    def __del__(self):
        self.writer.release()
