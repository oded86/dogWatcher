import sys
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import time
import requests


class MyHandler(PatternMatchingEventHandler):

    def process(self, event):
        payload = {"lat": "12345", "lon": "654321", "url": "https://127.0.0.1/risoh-images/" + event.src_path}
        r = requests.post("http://incontrol-sys.com:8000/dogcat", data=payload)
        print(r.text)

    def on_modified(self, event):
        print("file modified " + event.src_path)
        self.process(event)

    def on_created(self, event):
        print("file created" + event.src_path)
        pass  # self.process(event)

    def on_moved(self, event):
        print("file moved" + event.src_path)
        pass  # self.process(event)

    def on_deleted(self, event):
        print("file deleted" + event.src_path)
        pass  # self.process(event)


if __name__ == '__main__':
    args = sys.argv[1:]
    observer = Observer()
    observer.schedule(MyHandler(), path=args[0] if args else '.')
    print("Start")
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
