# Check duplicate files
# gets a directory from user and checks for duplicate files
# in the current directory tree.
#
# Need to:
# 1 - Determine how the search path will be given to the script
# 2 - Will the script check the entire tree or just the given folder?
# 3 - Which are the methods to be used in order to determine if a file is 
#     duplicated or not?
#    
#     a - Get MD5 key for the file.
#     b - Check for the file size.
# 4 - How to store the files in order to show them to the user?

import os, hashlib

# Global Variables
allFiles   = dict()
searchRoot = "."

#------------------------------------------------------------------------------
#
# getFileMD5Key
#
# Calculates MD5 Key for a file.
#
#-------------------------------------------------------------------------------
def getFileHash(root,file):
    filePath = root + '\\' + file

    with open(filePath, mode='rb') as f:
        d = hashlib.md5()
        while True:
            buf = f.read(4096)
            if not buf:
                break
            d.update(buf)
    return d.hexdigest()

#-------------------------------------------------------------------------------
#
# processDirectory
#
#
#-------------------------------------------------------------------------------
def processDirectory(root):
    global allFiles
    fileInfo = list()

    for root, subDirs, files in os.walk(root,topdown=True):
        
        print('Processing files at ',root)
        
        if len(files) == 0:
            print("No file found")
        else:
            try:
                for file in files:
                    fileDir  = root
                    fileHash = getFileHash(root,file)
                    fileSize = os.path.getsize(root + '\\' + file)
                    fileInfo = [fileDir,file,fileSize]
                    if not fileHash in allFiles:
                        allFiles[fileHash] = []
                        allFiles[fileHash].append(fileInfo)
                    else:
                        allFiles[fileHash].append(fileInfo)
            except IOError as e:
                print(e.strerror,':',file)

#-------------------------------------------------------------------------------
#
# findDuplicatedFileHasehes
#
#
#-------------------------------------------------------------------------------
def findDuplicatedHashes():
    global allFiles
    global duplicatedHashes

    print('Duplicated Files Found')
    for fileInfo in allFiles:
        if len(allFiles[fileInfo]) > 1 :
            print(fileInfo)
            for file in allFiles[fileInfo] :
                print(file)
            print()
    input('Press Enter to continue')
    
#-------------------------------------------------------------------------------
#
# printAllFiles
#
#
#-------------------------------------------------------------------------------
def printAllFiles():
    print('All Files Found')
    for fileHash in allFiles:
        print(fileHash,allFiles[fileHash])
    input('Press Enter to continue')

#-------------------------------------------------------------------------------
#
# changeDir()
#
#
#-------------------------------------------------------------------------------        
def changeDir():
    global searchRoot
    global allFiles
    
    while True:
        print('Change Current Search Directory\n')
        print('Enter a new directory for search or press Enter to skip')
        
        searchRoot = input('New directory: ')
        if searchRoot == "" :
            print('Skipping')
            break
        else :
            print('New root: ',searchRoot)
            allFiles = {}
            processDirectory(searchRoot)
            break

#-------------------------------------------------------------------------------
#
# refreshFiles()
#
#
#-------------------------------------------------------------------------------        
def refreshFiles():
    global allFiles
    global searchRoot
    
    allFiles = dict()

    print('Refreshing file list for ', searchRoot)
    processDirectory(searchRoot)
    input('Press Enter to continue')

#-------------------------------------------------------------------------------
#
# dumpDuplicatedFiles
#
#
#-------------------------------------------------------------------------------
def dumpDuplicatedFiles():
    global allFiles
    global searchRoot
    
    outFileName  = searchRoot + '\\dupfiles.csv'
    reportHeader = 'FileHash,FileName,Dir'

    print('Dumping Duplicated Files')
    
    try:
        o = open(outFileName, mode='w')
        o.write(reportHeader + '\n')

        for fileInfo in allFiles:
            if len(allFiles[fileInfo]) > 1 :
                for file in allFiles[fileInfo] :
                    o.write(fileInfo + ',' + file[0] + '\\' + file[1] + '\n')
    except IOError as e:
        print('Error: ',e.message,' at ',e.filename)

    input('Press Enter to continue')
        
#-------------------------------------------------------------------------------
#
# main
#
#
#-------------------------------------------------------------------------------        
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
        print('Main Menu:')
        print('1 - Change current dir')
        print('2 - Print all files')
        print('3 - Refresh files')
        print('4 - Find duplicated hashes')
        print('5 - Dump duplicated files')
        print('x - Exit')
        option = input('Choose one option: ')

        if option == '1' :
            changeDir()
            
        elif option == '2' :
            printAllFiles()
            
        elif option == '3' :
            refreshFiles()
            
        elif option == '4' :
            findDuplicatedHashes()

        elif option == '5' :
            dumpDuplicatedFiles()
            
        elif option == 'x' :
            print('Quitting')
            
        else :
            print('Invalid Option')
    
main()
