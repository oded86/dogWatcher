import sys
import json
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import time
import requests
import concurrent
import concurrent.futures
from image_details import ImageDetails
from backoffice_trello import Backoffice_trello
from message_center import MessageCenter

class MyHandler(PatternMatchingEventHandler):

    def request_post(self, url, payload):
        r = requests.post("http://incontrol-sys.com:8000/dogcatIn", data=payload, headers={'Connection': 'close'})
        # print(r.text)
        return r

    def process(self, event):
        num_workers = 5
        url = event.src_path.replace('../', '')
        url = event.src_path.replace('.\\', 'rishon_images/')
        image_full_details = ImageDetails(event.src_path).get_full_image_details()
        #print(type(image_full_details))
        #print(str(image_full_details))
        image_details = ImageDetails(event.src_path).get_image_details()
        lat = str(image_details['Latitude'])
        lon = str(image_details['Longitude'])
        payload = {"lat": lat, "long": lon, "url": url}
        print(payload)
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
                res = self.request_post(url, json.dumps(payload))
                print(res.text)
                if "We recognize dogs" in res.text:
                    bt = Backoffice_trello(url, image_full_details)
                    print(bt.open_trello_ticket())  # above returns json details of the card just created
                    mc = MessageCenter(url, res.text)
                    #mc.send_message("WHATSAPP")
                    mc.send_message("SMS")
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
