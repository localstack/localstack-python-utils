import threading
import logging


class LocalstackLogger:
    stream = None
    log_thread = None

    def __init__(self, localsack_container) -> None:
        self.stream = localsack_container.logs(stream=True, follow=True)

    def start(self):
        self.log_thread = threading.Thread(
            target=log_stream, args=[self.stream]
        ).start()


def log_stream(stream):
    try:
        while True:
            line = next(stream).decode("utf-8").replace("\n", "")
            logging.info(line)
    except StopIteration:
        pass
