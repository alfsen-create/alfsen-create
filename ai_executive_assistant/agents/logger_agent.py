import json
import queue
import threading
from utils.logging_utils import logger_queue, LOG_FILE_PATH

class LoggerAgent(threading.Thread):
    def __init__(self):
        super().__init__()
        self.input_q = logger_queue
        self.running = True

    def run(self):
        with open(LOG_FILE_PATH, 'a', encoding='utf-8') as log_file:
            while self.running:
                try:
                    log_entry = self.input_q.get(timeout=1)
                    if log_entry is None:
                        break
                    log_file.write(json.dumps(log_entry) + '\n')
                    log_file.flush()
                    self.input_q.task_done()
                except queue.Empty:
                    continue

    def stop(self):
        self.input_q.put(None)
        self.join()
