import threading


# a buffer to detach io read from image consumption to improve overall speed
class LazyStream:
    def __init__(self):
        self.images = []
        self.event = threading.Event()
        self.running = True

    def push(self, image):
        self.images.append(image)
        self.event.set()

    def __iter__(self):
        while self.running:
            # Wait until there are images in the buffer
            self.event.wait()
            if not self.running:
                return
            # Yield images while there are images in the buffer
            while len(self.images) > 0:
                yield self.images.pop(0)
            # Reset the event so it blocks again until a new image is added
            self.event.clear()

    def close(self):
        self.running = False
        self.event.set()
