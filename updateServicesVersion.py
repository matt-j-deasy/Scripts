#!/usr/bin/python

import os, sys, fileinput, filecmp, git, subprocess
from git import Repo

# Description
# 
# Iterate through subdirectories searching for build.gradle files.
# Search for build.gradle files with the old version and update to the new version
# Push changed files to their respective repos on a new feature branch specified on cl
#
# Usage Instructions
# Must have the following directory structure
#       -RootDir 
#               -ThisScript.py
#               -services/
#                       -service1
#                       -service2
#                       -etc
#               *NO OTHER GIT PROJECTS IN THIS ROOTDIR
#
# Command line arguments:
#   1: Name of branch to do edits on
#   2: Old Version i.e 1.1.1
#   3: New Version i.e 1.1.2
#
#  *Feature branch must not exist locally or upstream
#
# E.G: thisScript.py feature_branch_name 1.1.1 1.1.2

# Define root directory (where script is called from)
rootDir = os.path.dirname(os.path.abspath(__file__))

# Extract command line args
feature_branch_name = sys.argv[1]
oldversion = sys.argv[2]
newversion = sys.argv[3]

# Define relevant version formatting
versionPreface = "com.aap:web-service-client:"

# Define files to search
relevantFile = 'build.gradle'

# Logging info
print "\n"
print "Root directory: " + str(rootDir)
print "Old version: " + str(oldversion)
print "New version: " + str(newversion)
print "Searching files\n"

# Checkout a new branch from develop in the current directory from develop
def checkout_branch_brom_develop(git, fpath, dname):
        # Get the current repo

        print "\tChecking out new branch: " + feature_branch_name

        git.checkout("develop")
        git.branch(feature_branch_name)
        git.checkout(feature_branch_name)  # checkout local "feature branch"

        return git

#Push the changes in the dname directory to its git repo on a new branch names feature_branch_name
def push_change_to_git( git, repo ):

        print "\t\tEditing file on branch: " + feature_branch_name
        print "\t\tPushing changes upstream on branch: " + feature_branch_name + "\n"

        git.add(relevantFile)
        git.commit('-m', "'Update version in '" + relevantFile)
        repo.git.push("origin", feature_branch_name)
        git.checkout("develop")

        print "\t\tSwitching back to develop branch for this repo"

# Check file for version number
def file_contains_version(fpath):
        #Read in the file
        f = open(fpath, 'r')
        filedata = f.read()
        f.close()

        print("\tSearching file for: " + versionPreface + oldversion)

        # Return false if file contains no old version references
        if(versionPreface + oldversion not in filedata):
                return False

        print "\tFound pattern: " + versionPreface + oldversion 
        return True

# Update old version references in a file at to the new version
# If the old version if detected in the file, checks out a new branch from develop to make the changes
# fpath: Path to file
def edit_file(fpath):

        print '\t\tEditing file: ' + str(fpath) + "\n\t\t\tUpdating version to: " + newversion

        #Read in the file
        f = open(fpath, 'r')
        filedata = f.read()
        f.close()

        #Replace the target version    
        newdata = filedata.replace(versionPreface + oldversion, versionPreface + newversion)

        #Write the file out again
        f = open(fpath,'w')
        f.write(newdata)
        f.close()

def edit_file_update_git():
        #Search through all directories and subdirectories to find relevant files
        for dname, dirs, files, in os.walk(rootDir):

                for fname in files:

                        if fname == relevantFile:

                                fpath = os.path.join(dname, fname)
                                print "Found relevant file at: " + str(fpath)

                                #Ignore the base directory
                                #if(os.path.abspath is not dname and os.path.abspath is not '.git'):

                                        #Edit the file to update the version number
                                if(file_contains_version(fpath)):

                                        # Define the current git repo
                                        repo = Repo(dname)
                                        git = repo.git

                                        checkout_branch_brom_develop(git, fpath, dname)

                                        edit_file(fpath)

                                        push_change_to_git(git, repo)
                                
                                print "\n\n\n"



edit_file_update_git()