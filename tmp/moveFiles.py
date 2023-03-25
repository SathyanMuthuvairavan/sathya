#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 11:54:54 2022

@author: viyu
"""

# pip install watchdogs

import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os


class Handler(FileSystemEventHandler):
    print ("Calling the Handler")
    def on_modified(self,event):
        for filename in os.listdir(directory_to_track):
            src=directory_to_track+'/'+filename
            dest=directory_dest+'/'+filename
            os.rename(src,dest)
            
directory_to_track='/Users/viyu/Downloads/pythonProject/in'
directory_dest='/Users/viyu/Downloads/pythonProject/out'
        

# Storing the observer and event into an object. 
observer=Observer() 
event_executer=Handler()

observer.schedule(event_executer, directory_to_track, recursive=True)
observer.start()
print ("Calling the Handler")


try:
    while True:
        time.sleep(10)
        print ("timer")
except KeyboardInterrupt:
    observer.stop()


observer.join()