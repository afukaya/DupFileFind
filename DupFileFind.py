#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
NAME  : DupFileFind.py
AUTHOR: Alexandre Fukaya
DATE  : 25/01/2019

DESCRIPTION:
    Check duplicate files gets a directory from user and checks for duplicate 
    files in the current directory tree.
    
DEPENDENCIES:

TODO:
    1 - Determine how the search path will be given to the script
    2 - Will the script check the entire tree or just the given folder?
    3 - Which are the methods to be used in order to determine if a file is 
        duplicated or not? 
            a - Get MD5 key for the file.
            b - Check for the file size.
    4 - How to store the files in order to show them to the user?

CHANGELOG:
20230326 - Changed the buffer size at getFileHash function from 4096 to 65536.
D:\\Users\\afukaya\\OneDrive\\Photo
30151 files processed
All files size = 94613329033 bytes
Elapsed Time:  0:17:53.580061

Default Buffer
30151 files processed
All files size = 94613329033 bytes
Elapsed Time:  0:21:05.416608

"""

import os
import hashlib
import concurrent.futures

from pathlib import Path
from datetime import datetime

# Global Variables
# allFiles: This dictionary stores all files found at searchRoot as bellow.
#           | Variable | Type   | Description |
#           |:---------|:-------|:------------|
#           | fileHash | String | Store the MD5 hash for all files found. This is the dictionary key. |
#           | fileDir  | String | The path for the file file. |
#           | file     | String | File name. |
#           | fileSize | String | The size in bytes for the file.

allFiles = dict()
searchRoot = Path(".")

# ------------------------------------------------------------------------------
#
# getFileMD5Key
#
# Calculates MD5 Key for a file.
#
# -------------------------------------------------------------------------------


def getFileHash(root, file):
    filePath = os.path.join(root, file)

    with open(filePath, mode='rb') as f:
        d = hashlib.md5()
        while True:
            buf = f.read(65536)
            if not buf:
                break
            d.update(buf)
    return d.hexdigest()

# -------------------------------------------------------------------------------
#
# getFileStats
#
# Calculate statistics for files found.
#  - Number of files found.
#  - Number of duplicate files.
#  - Total disk size for all files found.
#  - Total disk size for duplicate files found.
#
# -------------------------------------------------------------------------------


def getFileStats(allfiles):
    allfiles_size = 0
    duplicatedfiles_found = 0

    for fhash in allfiles:
        files = allfiles[fhash]

        if len(files) > 1:
            duplicatedfiles_found += len(files)

        for files in allfiles[fhash]:
            allfiles_size += int(files[2])

    print("{0} files processed".format(len(allFiles)))
    print("All files size = {0} bytes".format(allfiles_size))
    return

# -------------------------------------------------------------------------------
#
# processDirectory
#
#
# -------------------------------------------------------------------------------


def processDirectory(root):

    global allFiles

    fileInfo = list()
    start_time = datetime.now()

    for root, subDirs, files in os.walk(root, topdown=True):

        print('Processing files at ', root)

        if len(files) == 0:
            print("No file found")
        else:
            try:
                for file in files:
                    fileDir = root
                    filePath = os.path.join(root, file)
                    fileHash = getFileHash(root, file)
                    fileSize = os.path.getsize(filePath)
                    fileInfo = [fileDir, file, fileSize]
                    if not fileHash in allFiles:
                        allFiles[fileHash] = []
                        allFiles[fileHash].append(fileInfo)
                    else:
                        allFiles[fileHash].append(fileInfo)
            except IOError as e:
                print(e.strerror, ':', file)

    getFileStats(allFiles)
    end_time = datetime.now()
    total_time = end_time - start_time
    print("Elapsed Time: ", total_time)

# -------------------------------------------------------------------------------
#
# findDuplicatedFileHasehes
#
#
# -------------------------------------------------------------------------------


def findDuplicatedHashes():
    global allFiles

    print('Duplicated Files Found')
    for fileInfo in allFiles:
        if len(allFiles[fileInfo]) > 1:
            print(fileInfo)
            for file in allFiles[fileInfo]:
                print(file)
            print()
    input('Press Enter to continue')

# -------------------------------------------------------------------------------
#
# printAllFiles
#
#
# -------------------------------------------------------------------------------


def printAllFiles():
    print('All Files Found')
    for fileHash in allFiles:
        print(fileHash, allFiles[fileHash])
    input('Press Enter to continue')

# -------------------------------------------------------------------------------
#
# changeDir()
#
#
# -------------------------------------------------------------------------------


def changeDir():
    global searchRoot
    global allFiles

    while True:
        print('Change Current Search Directory\n')
        print('Enter a new directory for search or press Enter to skip')

        searchRoot = input('New directory: ')
        if searchRoot == "":
            print('Skipping')
            break
        else:
            p = Path(searchRoot)
            if p.exists():
                print('New root: ', searchRoot)
                allFiles = {}
                processDirectory(searchRoot)
                break
            else:
                print('Directory not found.')

# -------------------------------------------------------------------------------
#
# refreshFiles()
#
#
# -------------------------------------------------------------------------------


def refreshFiles():
    global allFiles
    global searchRoot

    allFiles = dict()

    print('Refreshing file list for ', searchRoot)
    processDirectory(searchRoot)
    input('Press Enter to continue')

# -------------------------------------------------------------------------------
#
# dumpDuplicatedFiles
#
#
# -------------------------------------------------------------------------------


def dumpDuplicatedFiles():
    global allFiles
    global searchRoot

    outFileName = os.path.join(searchRoot, 'dupfiles.csv')
    reportHeader = 'FileHash,FileName,Dir'

    print('Dumping Duplicated Files')

    try:
        o = open(outFileName, mode='w')
        o.write(reportHeader + '\n')

        for fileInfo in allFiles:
            if len(allFiles[fileInfo]) > 1:
                for file in allFiles[fileInfo]:
                    o.write(fileInfo + ',' + '\"' +
                            file[0] + '\"' + ',' + "\"" + file[1] + "\"" + '\n')
    except IOError as e:
        print('Error: ', e.message, ' at ', e.filename)

    input('Press Enter to continue')

# -------------------------------------------------------------------------------
#
# main
#
#
# -------------------------------------------------------------------------------


def main():
    global allFiles

    option = ""

    processDirectory(searchRoot)

    while option != 'x':

        print()
        print('#---------------------------------------------------------#')
        print('#                                                         #')
        print('#                 Duplicate File Manager                  #')
        print('#                                                         #')
        print('#---------------------------------------------------------#')
        print()
        print('Current Dir: {0}'.format(searchRoot))
        print()
        print('Main Menu:')
        print('1 - Change current dir')
        print('2 - Print all files')
        print('3 - Refresh files')
        print('4 - Find duplicated hashes')
        print('5 - Dump duplicated files')
        print('x - Exit')
        option = input('Choose one option: ')

        if option == '1':
            changeDir()

        elif option == '2':
            printAllFiles()

        elif option == '3':
            refreshFiles()

        elif option == '4':
            findDuplicatedHashes()

        elif option == '5':
            dumpDuplicatedFiles()

        elif option == 'x':
            print('Quitting')

        else:
            print('Invalid Option')


if __name__ == '__main__':
    main()
