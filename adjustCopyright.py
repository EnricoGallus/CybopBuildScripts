#!/usr/bin/python
import sys
import os
import fileinput
import re
from datetime import datetime

# argument handling
if len(sys.argv) != 3:
    print("you must set two arguments. [this file] [version number] [copyright string]")
    exit()

version = sys.argv[1]
copyright_info = sys.argv[2]

# filters
fileExtensionFilter = ('.c', '.h', '.cybol', '.sh', '.txt', '.xsd', '.css', '.dtd', '.html', '.py', '.in')
fileFilter = ('AUTHORS', 'ChangeLog', 'COPYING', 'INSTALL', 'NEWS', 'README')
folderExclude = ('bin', 'doc', 'examples', 'ide', 'lib', 'tools', 'www')

# copyright definition
oldCopyright = r"Copyright \(C\) 1999-(\d+). Christian Heller."
# version definition
oldVersion = r"@version CYBOP (\d{1})\.(\d{2})\.(\d{1,}) (\d{4})-(\d{2})-(\d{2})"
newVersion = "@version CYBOP " + version + " " + datetime.today().strftime('%Y-%m-%d')


def change_file_content(filepath):
    file_content_read_only = open(filepath, 'r').read()
    if re.findall(oldVersion, file_content_read_only) and re.findall(oldCopyright, file_content_read_only):
        for line in fileinput.input(filepath, inplace=True):
            line = re.sub(oldCopyright, copyright_info, line)  # replace to year in copyright
            line = re.sub(oldVersion, newVersion, line)  # replace version and today date
            sys.stdout.write(line)


for subdir, dirs, files in os.walk(os.path.join(os.path.dirname(__file__), '..', '..')):
    dirs[:] = [d for d in dirs if d not in folderExclude]
    for file in files:
        if file.lower().endswith(fileExtensionFilter) or file in fileFilter:
            change_file_content(subdir + os.sep + file)
