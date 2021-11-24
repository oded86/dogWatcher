import sys
import json
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import time
import requests
import concurrent
import concurrent.futures
from image_details import ImageDetails
from backoffice_trello import BackofficeTrello
from message_center import MessageCenter
from recorder import dogRecorder


class MyHandler(PatternMatchingEventHandler):

    def request_post(self, url, payload):
        r = requests.post("http://incontrol-sys.com:8000/dogcatIn", data=payload, headers={'Connection': 'close'})
        # print(r.text)
        return r

    def process(self, event):
        num_workers = 5
        url = event.src_path.replace('../', '')
        url = url.replace('.\\', 'rishon_images/')
        camera_url = 'rtsp://admin:Champi0n%24@2.55.114.241:8554/1'
        image_full_details = ImageDetails(event.src_path).get_full_image_details()
        # print(type(image_full_details))
        # print(str(image_full_details))
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
                    if "behavior: pooping" in res.text:
                        poop_flag = True
                    else:
                        poop_flag = False

                    bt = BackofficeTrello(url, image_full_details, poop_flag)
                    card = bt.open_trello_ticket()
                    # print(card)
                    if poop_flag:
                        rc = dogRecorder(camera_url, 10, card['id'])
                        video_file = rc.record_movie()
                        bt.add_attachment_to_ticket(video_file, card['id'])

                    # mc = MessageCenter(url, res.text)
                    # mc.send_message("WHATSAPP")
                    # mc.send_message("SMS")
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
