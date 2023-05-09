import logging
import threading
from abc import ABC, abstractmethod

from detectionio.utils.streams import LazyStream


class AbstractVideoConsumer(ABC):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def close(self):
        pass


class GenericVideoConsumer:
    def __init__(self, frames_stream):
        self.frames_stream = frames_stream
        self.output_stream = LazyStream()
        self._runner = threading.Thread(target=self._run, args=(self.frames_stream, self.output_stream))

    # delivers consumed messages in generator fashion
    def start(self):
        self._runner.start()
        logging.info("Started reading from input")

        for frame in self.output_stream:
            yield frame

    # consumes messages from input as fast as possible
    @staticmethod
    def _run(input_stream, output_stream: LazyStream):
        try:
            for frame in input_stream:
                output_stream.push(frame)
        finally:
            input_stream.close()
            output_stream.close()
            logging.info("Consumer closed")
