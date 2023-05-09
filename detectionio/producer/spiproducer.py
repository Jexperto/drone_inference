import enum

import numpy as np
import spidev

from detectionio.producer.producerinterface import GenericVideoProducer, AbstractVideoProducer, AbstractWriter
from detectionio.utils.spiconfig import SPIModeConfig, SPIHzConfig
from detectionio.utils.streams import LazyStream


class SPIWriter(AbstractWriter):
    def __init__(self, bus_num=0, device_num=0, spi_mode=SPIModeConfig.LOW_CLOCK_LEADING,
                 spi_max_speed_hz=SPIHzConfig.Hz7629):
        self.spi = spidev.SpiDev()
        self.spi.open(bus_num, device_num)
        self.spi.mode = spi_mode
        self.spi.max_speed_hz = spi_max_speed_hz

    def write(self, data: bytes):
        self.spi.writebytes(data)

    def close(self):
        self.spi.close()


class SPIVideoProducer(AbstractVideoProducer):
    def __init__(self, bus_num=0, device_num=0, spi_mode=SPIModeConfig.LOW_CLOCK_LEADING,
                 spi_max_speed_hz=SPIHzConfig.Hz7629):
        self.stream = LazyStream()
        self.writer = SPIWriter(bus_num, device_num, spi_mode, spi_max_speed_hz)
        self.producer = GenericVideoProducer(self.stream, self.writer)
        self.running = False

    def start(self):
        self.producer.start()

    def push_image(self, image: np.ndarray):
        if not self.running:
            self.start()
            self.running = True
        self.stream.push(image.tobytes())

    def close(self):
        self.stream.close()
        self.running = False
