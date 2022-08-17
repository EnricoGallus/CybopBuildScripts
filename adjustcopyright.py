#!/usr/bin/python
import sys
import os
import fileinput
import re
from datetime import datetime, timedelta

# argument handling
if len(sys.argv) != 3:
    print("you must set two arguments. [this file] [root dir] [version number]")
    exit()

rootdir = sys.argv[1]
version = sys.argv[2]

# filters
fileExtensionFilter = ('.c', '.h', '.cybol', '.sh', '.txt', '.xsd', '.css', '.dtd', '.html', '.py')
fileFilter = ('AUTHORS', 'ChangeLog', 'COPYING', 'INSTALL', 'NEWS', 'README')
folderExclude = ('include', 'tools')

# today
today = datetime.today() # - timedelta(days=1) in case date needs to be adjusted

# tab definition
oldTab = "\t"
newTab = "    "
# copyright defintion
oldCopyright = r"Copyright \(C\) 1999-(\d+). Christian Heller."
newCopyright = "Copyright (C) 1999-" + today.strftime("%Y") + ". Christian Heller."
# version defintion
oldVersion = r"@version CYBOP (\d.+)"
newVersion = "@version CYBOP " + version + " " + today.strftime('%Y-%m-%d')

def changeFileContent(filepath):
    for line in fileinput.input(filepath, inplace=True):
        line = line.replace(oldTab, newTab) # replace tab with spaces
        line = re.sub(oldCopyright, newCopyright, line) # replace to year in copyright
        line = re.sub(oldVersion, newVersion, line) # replace version and today date
        sys.stdout.write (line)

for subdir, dirs, files in os.walk(rootdir):
    dirs[:] = [d for d in dirs if d not in folderExclude]
    for file in files:
        if file.lower().endswith(fileExtensionFilter) or file in fileFilter:
            changeFileContent(subdir + os.sep + file)

