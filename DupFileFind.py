#! /usr/bin/python3
# -*- coding: utf-8 -*-
""" DupFileFind.py
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

def get_file_hash(root, file):

    """get_file_hash 
    
    Calculates MD5 Key for a file.

    Parameters
    ----------
    root : str
        The path where the file is stored
    file : str
        Name of the file to be processed.

    Returns
    -------
    str
        The MD5 hash for the given file.
    """

    file_path = os.path.join(root, file)

    with open(file_path, mode='rb') as f:
        d = hashlib.md5()
        while True:
            buf = f.read(65536)
            if not buf:
                break
            d.update(buf)
    return d.hexdigest()

def get_file_stats(allfiles):

    """get_file_stats 
    
    Calculate statistics for files found like:
    - Number of files found.
    - Number of duplicate files.
    - Total disk size for all files found.
    - Total disk size for duplicate files found.

    Parameters
    ----------
    allfiles : List
        A List containing allpre processed files.
    """

    allfilessize = 0
    duplicatefound = 0

    for fhash in allfiles:
        files = allfiles[fhash]

        if len(files) > 1:
            duplicatefound += len(files)

        for files in allfiles[fhash]:
            allfilessize += int(files[2])

    print("{0} files processed".format(len(allFiles)))
    print("With {0} Duplicated files found.".format(duplicatefound))
    print("All files size = {0} bytes".format(allfilessize))
 
def process_directory(root):
    """process_directory

    Walks through a given directory tree and finds all duplicated files 
    in that path by calculating and compairing their MD5 hash.

    Parameters
    ----------
    root : string
        The name of the serach starting directory.
    """

    global allFiles

    fileinfo = list()
    start_time = datetime.now()

    for root, subdirs, files in os.walk(root, topdown=True):

        print('Processing files at ', root)

        if len(files) == 0:
            print("No file found")
        else:
            try:
                for file in files:
                    filedir = root
                    filepath = os.path.join(root, file)
                    filehash = get_file_hash(root, file)
                    filesize = os.path.getsize(filepath)
                    fileinfo = [filedir, file, filesize]
                    if filehash not in allFiles:
                        allFiles[filehash] = []
                        allFiles[filehash].append(fileinfo)
                    else:
                        allFiles[filehash].append(fileinfo)
            except IOError as e:
                print(e.strerror, ':', file)

    get_file_stats(allFiles)
    end_time = datetime.now()
    total_time = end_time - start_time
    print("Elapsed Time: ", total_time)

def find_duplicated_hashes():
    """find_duplicated_hashes

    List on console information about all duplicated files found .
    """    
    global allFiles

    print('Duplicated Files Found')
    for fileinfo in allFiles:
        if len(allFiles[fileinfo]) > 1:
            print(fileinfo)
            for file in allFiles[fileinfo]:
                print(file)
            print()
    input('Press Enter to continue')

def print_all_files():
    """print_all_files

    List on console the information about all files found.
    """    
    print('All Files Found')
    for filehash in allFiles:
        print(filehash, allFiles[filehash])
    input('Press Enter to continue')

def change_dir():
    """change_dir

    Allows user to change a different directory for search.
    """    
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
                process_directory(searchRoot)
                break
            else:
                print('Directory not found.')

def refresh_files():
    """refresh_files

    Update the file information for the current directory.
    """    
    global allFiles
    global searchRoot

    allFiles = dict()

    print('Refreshing file list for ', searchRoot)
    process_directory(searchRoot)
    input('Press Enter to continue')

def dump_duplicated_files():
    """dump_duplicated_files

    Create a CSV file with duplicate files information.
    """    
    global allFiles
    global searchRoot

    outfilename = os.path.join(searchRoot, 'dupfiles.csv')
    reportheader = 'FileHash,FileName,Dir'

    print('Dumping Duplicated Files')

    try:
        o = open(outfilename, mode='w')
        o.write(reportheader + '\n')

        for fileinfo in allFiles:
            if len(allFiles[fileinfo]) > 1:
                for file in allFiles[fileinfo]:
                    o.write(fileinfo + ',' + '\"' +
                            file[0] + '\"' + ',' + "\"" + file[1] + "\"" + '\n')
    except IOError as e:
        print('Error: ', e.message, ' at ', e.filename)

    input('Press Enter to continue')

def main():
    """main The main function.

     Draws the user interface and execute its functions.
    """    
    global allFiles

    option = ""

    process_directory(searchRoot)

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
            change_dir()

        elif option == '2':
            print_all_files()

        elif option == '3':
            refresh_files()

        elif option == '4':
            find_duplicated_hashes()

        elif option == '5':
            dump_duplicated_files()

        elif option == 'x':
            print('Quitting')

        else:
            print('Invalid Option')


if __name__ == '__main__':
    main()
