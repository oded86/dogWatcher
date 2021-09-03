import sys
import time
import watchdog
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import time
from threading import Thread

class MyHandler(PatternMatchingEventHandler):

    def process(self, event):
        print "I am being processed"

    def on_modified(self, event):
        print "file modified " + event.src_path
        self.process(event)

    def on_created(self, event):
        print "file created" + event.src_path
        self.process(event)

    def on_moved(self, event):
        print "file moved" + event.src_path
        self.process(event)

    def on_deleted(self, event):
        print "file deleted" + event.src_path
        self.process(event)

if __name__ == '__main__':
    args = sys.argv[1:]  
    observer = Observer()
    observer.schedule(MyHandler(), path=args[0] if args else '.')
    print "Start"
    observer.start()
