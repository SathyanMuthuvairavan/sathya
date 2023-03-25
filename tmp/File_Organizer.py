#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 16:14:21 2022

@author: viyu
"""
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler

import time

class MyEventHandler(FileSystemEventHandler:
    def on_created(self, event):
        if not event.is_directory:
            with open(event.src_path) as fp:
                fp.read_lines()
            
    

path = "in"

event_handler = MyEventHandler()

observer = Observer()
observer.schedule(event_handler, path, recursive=True)
observer.start()

try:
    while True:
        time.sleep(1)
finally:
    observer.stop()
    observer.join()
     