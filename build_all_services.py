#!/usr/bin/python

import os, subprocess

rootDir = os.path.dirname(os.path.abspath(__file__))

for item in os.listdir(rootDir):

        if not str(item).startswith(".") and not str(item) == "build_all_services.py":
            fpath = os.path.join(rootDir, item)

            print("First level dir: " + fpath)

            for files in os.listdir(fpath):
            
                print("File in first level dir: " + files)

                if files == 'build_service.sh':

                    os.chdir(fpath)

                    fpath = os.path.join(fpath, files)
                    print ("Attempting to execute script at: " + str(fpath))
                    subprocess.call(fpath)

                    os.chdir(rootDir)