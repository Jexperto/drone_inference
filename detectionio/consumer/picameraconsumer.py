import io
from detectionio.consumer.consumerinterface import AbstractVideoConsumer
import picamera


class PiVideoConsumer(AbstractVideoConsumer):
    def __init__(self, resolution=(640, 480), framerate=24, use_video_port=True, format='jpeg'):
        self.format = format
        self.use_video_port = use_video_port
        self.framerate = framerate
        self.running = False
        self.resolution = resolution

    def start(self):

        self.running = True
        camera = picamera.PiCamera(resolution=f'{self.resolution[0]}x{self.resolution[1]}', framerate=self.framerate,
                                   use_video_port=self.use_video_port)
        try:
            stream = io.BytesIO()
            for frame in camera.capture_continuous(stream, format=self.format):
                stream.truncate()
                stream.seek(0)
                yield frame
        finally:
            self.running = False
            camera.stop_recording()
            camera.close()
