import os
import time

LOG_DIR = "logs"

class Logger:
    def __init__(self):
        os.makedirs(LOG_DIR, exist_ok=True)
        self.current_day = None
        self.file = None

    def _get_filename(self):
        day = time.strftime("%Y-%m-%d")
        return os.path.join(LOG_DIR, f"hive_{day}.log")

    def _open(self):
        day = time.strftime("%Y-%m-%d")
        if day != self.current_day:
            if self.file:
                self.file.close()
            self.current_day = day
            self.file = open(self._get_filename(), "a", encoding="utf-8")

    def log(self, agent_id, task_id, model_type, content, result=None, status="running"):
        self._open()
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{timestamp}]\nAGENT={agent_id}\nTASK={task_id}\nmodel_type={model_type}\nSTATUS={status}\n{content}\n"
        if result is not None:
            line += f"  RESULT: {result.strip()}\n\n"
        self.file.write(line)
        self.file.flush()

    def close(self):
        if self.file:
            self.file.close()
            
logger = Logger ()
