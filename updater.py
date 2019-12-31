import requests, os, shutil, subprocess
from os import listdir
from os.path import isfile, join
from bs4 import BeautifulSoup
#os.environ["GIT_PYTHON_REFRESH"] = "quiet"
import git

def getListOfFiles(dirName):
    # create a list of file and sub directories
    # names in the given directory
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles

path = os.path.realpath(__file__).replace("\\", "/").split("/")
path = "/".join(path[:-1])
print(path)

git.Git(path).clone("https://github.com/xLeon-python/MCBot.git")
print("cloning...")
files_raw = getListOfFiles(path+"/MCBot")

files = []

for i in files_raw:
    files_raw[files_raw.index(i)] = i.replace("\\", "/")
    i = i.replace("\\", "/")
    if "git" in i or "updater.py" in i:
        pass
    else:
        files.append(i)

path = path + "/"
for i in files:
    fr = open(i).read()
    if "updater.py" in i:
        pass
    if "main.py" in i:
        fw = open(path + i.split("/")[-1], "w")
        print("copied file " + i + " to " + path + i.split("/")[-1])
    else:
        fw = open(path + "/".join(i.split("/")[-2:]), "w")
    fw.write(fr)
    fw.close()
    print("copied file " + i + " to " + path + "/".join(i.split("/")[-2:]))

path = path + "MCBot"

directories = [ name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name)) ]
print(directories)
'''
for i in directories:
    if i == ".git":
        pass
    else:
        shutil.rmtree(path + "/" + i)
'''
print(path)
shutil.rmtree(path)
