from typing import Tuple

import cv2

from detectionio.producer.producerinterface import AbstractVideoProducer, GenericVideoProducer
from detectionio.utils.streams import LazyStream


class FileVideoProducer(AbstractVideoProducer):
    def __init__(self, output_path, framerate: int = 24, resolution: Tuple[int, int] = (640, 480)):
        self.stream = LazyStream()
        self.writer = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*"mp4v"), framerate, resolution)
        self.producer = GenericVideoProducer(self.stream, self.writer)
        self.running = False

    def start(self):
        self.producer.start()

    def push_image(self, image):
        if not self.running:
            self.start()
            self.running = True
        self.stream.push(image)

    def close(self):
        self.stream.close()
        self.running = False
