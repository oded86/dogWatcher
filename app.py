import sys
import json
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import time
import requests
import concurrent
import concurrent.futures
from image_details import ImageDetails


class MyHandler(PatternMatchingEventHandler):


    def request_post(self, url, payload):
        r = requests.post("http://incontrol-sys.com:8000/dogcat", data=payload, headers={'Connection':'close'})
        print(r.text)

    def process(self, event):
        num_workers = 5
        url = "var/www/html/" + event.src_path.replace('../', '')
        image_details = ImageDetails(event.src_path).get_image_details()
        lat = str(image_details['Latitude'])
        lon = str(image_details['Longitude'])
        payload = {"lat": lat, "long":  lon, "url": url}
        # print(json.dumps(payload))
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
                res = executor.submit(self.request_post(url, json.dumps(payload)))
                concurrent.futures.wait(res)

        except:
            pass

    def on_modified(self, event):
        if "jpg" in event.src_path:
            print("file modified " + event.src_path)
            time.sleep(5)
            self.process(event)
        else:
            pass

    def on_created(self, event):
        if "jpg" in event.src_path:
            print("file created " + event.src_path)
            time.sleep(5)
            self.process(event)
        else:
            pass

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