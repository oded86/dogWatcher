import json
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import time
import requests
import concurrent
import concurrent.futures

class MyHandler(PatternMatchingEventHandler):

    def request_post(self, url, payload):
        r = requests.post("http://incontrol-sys.com:8000/dogcat", data=payload, headers={'Connection':'close'})
        print(r.text)

    def process(self, event):
        num_workers = 5
        url = event.src_path.replace('../', '')
        payload = {"lat": "31.97102", "long": "34.78939", "url": "http://incontrol-sys.com/" + url}
        # print(json.dumps(payload))a
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
                res = executor.submit(self.request_post(url, json.dumps(payload)))
                concurrent.futures.wait(res)
        except:
            pass

    def on_modified(self, event):
        if "png" in event.src_path:
            print("file modified " + event.src_path)
            self.process(event)
        else:
            pass

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
            time.sleep(100)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()