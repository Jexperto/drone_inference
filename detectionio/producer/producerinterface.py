import logging
from abc import ABC, abstractmethod
import threading


class AbstractVideoProducer(ABC):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def close(self):
        pass


class AbstractWriter(ABC):
    @abstractmethod
    def write(self, data):
        pass

    @abstractmethod
    def close(self):
        pass


class GenericVideoProducer:
    def __init__(self, frames_stream, output_writer: AbstractWriter):
        self.stream = frames_stream
        self.writer = output_writer
        self._runner = threading.Thread(target=self._run, args=(self.writer, self.stream))

    def start(self):
        self._runner.start()
        logging.info("Started writing to output")

    @staticmethod
    def _run(writer, stream):
        try:
            for frame in stream:
                writer.write(frame)
        finally:
            writer.release()
            logging.info("Writer closed")
