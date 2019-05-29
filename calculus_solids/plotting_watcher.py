import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler
import subprocess

class RunScript(FileSystemEventHandler):
    def on_modified(self,event):
        print('changed file?'+event.src_path)
        if "plotting_math.py" in event.src_path:
            subprocess.call("python plotting_math.py".split())

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = RunScript()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()