import cv2

from detectionio.consumer.consumerinterface import AbstractVideoConsumer, GenericVideoConsumer


class VideoCaptureIterable:
    def __init__(self, capture):
        self.capture = capture
        self.running = False

    def __iter__(self):
        self.running = True
        success, image = self.capture.read()
        while success and self.running:
            yield image
            success, image = self.capture.read()

    def close(self):
        self.running = False


class FileVideoConsumer(AbstractVideoConsumer):

    def __init__(self, filepath):
        self.filepath = filepath
        self.running = False
        self._videocap = cv2.VideoCapture(self.filepath)
        self.capture = VideoCaptureIterable(self._videocap)
        self.shape = (int(self._videocap.get(3)), int(self._videocap.get(4)))
        self.consumer = GenericVideoConsumer(self.capture)

    def start(self):
        try:
            self.running = True
            for frame in self.consumer.start():
                if self.running:
                    yield frame

        finally:
            self.running = False

    def close(self):
        self.running = False
