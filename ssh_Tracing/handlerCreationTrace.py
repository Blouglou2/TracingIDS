#!/usr/bin/env python
# -*- coding : utf-8 -*-

import time  
from watchdog.observers import Observer  
from watchdog.events import PatternMatchingEventHandler  
import sys
from babeltraceReader import *

#########################################################################
# Demon qui attend la création d'un dossier et qui le passe en argument #
# au reader Babeltrace                                                  #
#########################################################################



class MyHandler(PatternMatchingEventHandler):
    patterns = ["*"] # Utile pour definir un patern

    def process(self, event):
        """
        event.event_type 
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        # the file will be processed there
        # print (event.src_path, event.event_type)  # print now only for degug
        if (event.is_directory) :
            path = event.src_path + "/kernel/"
            processTraces(path) # Reader Babeltrace

    # def on_modified(self, event):
    #     self.process(event)

    def on_created(self, event):
        self.process(event)

def main() :
    args = sys.argv[1:]
    observer = Observer()
    observer.schedule(MyHandler(), path=args[0] if args else '.')
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

if __name__ == '__main__':
    main()
