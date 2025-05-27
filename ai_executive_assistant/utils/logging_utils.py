import queue
import time
import json
from config import LOG_FILE_PATH

logger_queue = queue.Queue()

def log_event(event_type, tool_name, **kwargs):
    log_entry = {"timestamp": time.time(), "event_type": event_type, "tool_name": tool_name}
    log_entry.update(kwargs)
    logger_queue.put(log_entry)

class LoggerAgent(queue.Queue, object):
    def __init__(self, input_q, log_file_path=LOG_FILE_PATH):
        self.input_q = input_q
        self.log_file_path = log_file_path
        self.running = True

    def run(self):
        with open(self.log_file_path, 'a', encoding='utf-8') as log_file:
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
