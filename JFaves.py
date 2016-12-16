import subprocess
import time
import subprocess
import os
import re


def getClipboardData():
    return subprocess.check_output(
        'pbpaste', env={'LANG': 'en_US.UTF-8'}).decode('utf-8')

def setClipboardData(data):
    p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
    p.stdin.write(data)
    p.stdin.close()
    retcode = p.wait()
    
def quoteDaFucker(element):
    element = "\"" + element + "\""
    return element

def filenameNoExt(posixPath):
    fileWithExt = os.path.basename(posixPath)
    fileNoExt = ".".join(fileWithExt.split('.')[:-1])
    return fileNoExt
    

def timeStampDaFucker():
    currentTime = time.strftime('%y%m%d_%I%M%S%p')
    return currentTime

def getSystemDrive(posixPath):
    pipe = subprocess.Popen("""osascript -e 'tell app "finder" to get name of the startup disk'""",
                        stdout=subprocess.PIPE, shell=True)
    startupDisk = (pipe.stdout.read()).split('\n', 1)[0]
    if "/Users" in posixPath:
        posixPath = "/Volumes/%s%s" % (startupDisk, posixPath) 
    else:
        posixPath = posixPath
    return posixPath


def getFileComponents(posixPath):
    '''Returns dirPathOnly, filenameWithExt, fileNameNoExt'''
    dirPathOnly = os.path.dirname(posixPath) + '/'
    filenameWithExt =  os.path.basename(posixPath)
    fileNameNoExt = os.path.splitext(filenameWithExt)[0]
    
    return dirPathOnly, filenameWithExt, fileNameNoExt


def prettySep(userText):
    print '*' * 20
    print userText
    print '*' * 20


def pathTester(destDir):

    if os.path.exists(destDir):
        print "\n%s EXISTS!!!" % destDir
    
    elif destDir.endswith("  ") and not ("\\" in destDir) == True:
        print "\ndestDir ends with a double space"
        if os.path.exists(destDir):
            print "\n%s exists" % destDir
        elif os.path.exists(destDir) == False:
            print "\nWill attempt to remove trailing space"
            destDir = destDir[:-1]
            print "\nlast character is now: " + destDir[-1]
            if os.path.exists(destDir):
                print "%s EXISTS!!!" % destDir
                return destDir

            else:
                print "\n%s is still not a working directory" % destDir
                exit()
    
    elif destDir.endswith("  ") and "\\" in destDir:
        print "destDir contains backslashes and double trailing space"
        print "Removing backslashes and trailing space"
        destDir = destDir[:-1]
        destDir = re.sub(r"\\(?!\\{1})", "", destDir)
        destDir = re.sub(r"\\{2}", r"\\", destDir)
        print "Regex fixed, new destDir = \n%s " % destDir
        if os.path.exists(destDir):
            print "\n%s EXISTS!!!" % destDir
            return destDir
        else:
            print "\n%s is still not a working directory" % destDir
            exit()
    
    elif destDir.endswith(" ") and not ("\\" in destDir) == True:
        print "\ndestDir ends with a space"
        if os.path.exists(destDir):
            print "\n%s exists" % destDir
        elif os.path.exists(destDir) == False:
            print "\nWill attempt to remove trailing space"
            destDir = destDir[:-1]
            print "\nlast character is now: " + destDir[-1]
            if os.path.exists(destDir):
                print "%s EXISTS!!!" % destDir
                return destDir
            else:
                print "\n%s is still not a working directory" % destDir
                exit()
    
    elif destDir.endswith(" ") and "\\" in destDir:
        print "destDir contains backslashes and trailing space"
        print "Removing backslashes and trailing space"
        destDir = re.sub(r"\\(?!\\{1})", "", destDir)
        destDir = re.sub(r"\\{2}", r"\\", destDir)
        if os.path.exists(destDir) == False:
            destDir = destDir[:-1]
       # print "Regex fixed, new destDir = %s " % destDir
        if os.path.exists(destDir):
            print "\n%s EXISTS!!!" % destDir
            return destDir
        else:
            print "\n%s is still not a working directory" % destDir
            exit()
    
    elif "\\" in destDir:
        print "destDir contains backslashes and double trailing space"
        print "Removing backslashes"
        destDir = re.sub(r"\\(?!\\{1})", "", destDir)
        destDir = re.sub(r"\\{2}", r"\\", destDir)
        print "Regex fixed, new destDir = \n%s " % destDir
        if os.path.exists(destDir):
            print "\n%s EXISTS!!!" % destDir
            return destDir
        else:
            print "\n%s is still not a working directory" % destDir
            exit()
    
    else:
        print "\nAs is, the path doesn't seem to exist."
        exit()

self_dir = os.path.dirname(os.path.abspath(__file__)) + '/'