import cv2
import time
import sys
import numpy as np


class dogRecorder:
    def __init__(self, video_url, video_length, ticket_id):
        self.video_url = video_url
        self.video_length = video_length
        self.ticket_id = ticket_id

    def record_movie(self):
        vidcap = cv2.VideoCapture(self.video_url)
        if not vidcap:
            print("!!! Failed VideoCapture: invalid parameter!")
        now = time.time()
        future = now + self.video_length
        frame_width = int(vidcap.get(3) * 0.5)
        frame_height = int(vidcap.get(4) * 0.5)
        fourcc = cv2.VideoWriter_fourcc('V', 'P', '0', '9')
        video_file_name = 'outpy_' + str(self.ticket_id) + '.webm'
        out = cv2.VideoWriter(video_file_name, fourcc, 10, (frame_width, frame_height))
        while time.time() < future:
            ret, frame = vidcap.read()
            if ret:
                resized = cv2.resize(frame, (frame_width, frame_height), fx=0, fy=0, interpolation=cv2.INTER_CUBIC)
                out.write(resized)

        # release the capture
        vidcap.release()
        cv2.destroyAllWindows()
        return video_file_name


#rc = dogRecorder('rtsp://admin:Champi0n%24@2.55.114.241:8554/1', 30, 1)
#rc.record_movie()
