import threading
import logging

LOG = logging.getLogger(__name__);

class LocalstackLogger():
    stream = None
    def __init__(self, localsack_container) -> None:
        stream = localsack_container.logs(stream=True, follow=True)    

    
    def start(self):
        log_thread = threading.Thread(target=log_stream,args=[self.stream])
            
def log_stream(stream):
    try:
        print("starting logs")
        while True:
            line = next(stream).decode("utf-8")
            LOG.warning(line)
    except StopIteration:
        print("LOGS ENDED")    
