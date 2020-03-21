#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
NAME  : HashCalcMT.py
AUTHOR: Alexandre Fukaya
DATE  : 25/01/2019

DESCRIPTION:
    Multithread hash file calculation script.
    Runs thru a folder structure and calculates the MD5 hash for all files found,
    printing the information on console.
    
DEPENDENCIES:

TODO:

CHANGELOG:
    18/03/2020: 
"""

import os
import threading
import multiprocessing
import hashlib
import time

allFiles = dict()

def getFileHash(root,file):
    filePath = os.path.join(root,file)

    with open(filePath, mode='rb') as f:
        d = hashlib.md5()
        while True:
            buf = f.read(8192)
            if not buf:
                break
            d.update(buf)
    print(root,file,d.hexdigest())
    return d.hexdigest

def processDirectory(root):
    start_time = time.time()
    print('Process starting @ {0}'.format(time.ctime(start_time)))
    for root, subDirs, files in os.walk(root,topdown=True):
        print('Processing files at ',root)
        
        if len(files) == 0:
            print("No file found")
        else:
            try:
                threads = []
                for file in files:
                    thread = threading.Thread(target = getFileHash, args = (root,file))
                    threads.append(thread)
                    thread.start()

                for thread in threads:
                    thread.join()

            except IOError as e:
                print(e.strerror,':',file)
                
    end_time = time.time() 
    duration = end_time - start_time
    print('Process ended @ {0}'.format(time.ctime(end_time)))
    print('Duration: {0} seconds'.format(duration))
    print()

def main():
    root = os.getcwd()
    root = 'D:\\Users\\afukaya\\OneDrive\\Bookshelf'
    #processDirectory_threads(root)
    processDirectory(root)

if __name__ == "__main__":
    main()