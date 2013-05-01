#
# Copyright 2012 The SCAPE Project Consortium
#
# This software is copyrighted by the SCAPE Project Consortium.
# The SCAPE project is co-funded by the European Union under
# FP7 ICT-2009.4.1 (Grant Agreement number 270137).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Various shared functions

import sys
import os

def printWarning(msg):
    msgString=("User warning: " + msg +"\n")
    sys.stderr.write(msgString)

def printInfo(msg):
    # Note: we're using 'stderr' here instead of 'stdout' because 'stdout'
    # is used for XML-formatted logging information
    msgString=(msg + "\n")
    sys.stderr.write(msgString)
 
def errorExit(msg):
    msgString=("Error: " + msg + "\n")
    sys.stderr.write(msgString)
    sys.exit()

def checkFileExists(fileIn):
    # Check if file exists and exit if not
    if os.path.isfile(fileIn)==False:
        msg=fileIn + " does not exist!"
        errorExit(msg)
       
def addPath(pathIn,fileIn):
    # Appends file name (FileIn) to a path definition (pathIn)
    # Result conforms to OS conventions (forward/backard slashes)
    #
    # Example:
    #
    # addpath("d:/whereever","whatever.doc")
    #
    # result: d:\whereever\whatever.doc (Win)
    # result: d:/whereever/whatever.doc (Linux)
    #
    # Using forward slashes in input arguments is always the safest bet
    # (backward slashes may give unpredictable results, so avoid them!)
    #
    result=os.path.normpath(pathIn+ "/" + fileIn)
    return(result)

def isAbsolutePath(pathIn):
    # Returns True if file path appears to be absolute path,
    # False otherwise
    
    if os.path.basename(pathIn) == pathIn:
        result=False
    else:
        result=True
    return(result)

    return(fileData)

def readFileBytes(file):
    # Read file, return contents as a byte object
    
    # Open file
    f = open(file,"rb")
    
    # Put contents of file into a byte object.
    fileData=f.read()
    f.close()
    
    return(fileData)
   
def quoteString(inputString):
    outputString='"'+ inputString + '"'
    return outputString

def constructFileName(fileIn,pathOut,extOut,suffixOut):
    # Construct filename by replacing path by pathOut,
    # adding suffix and extension
    
    fileInTail=os.path.split(fileIn)[1]

    baseNameIn=os.path.splitext(fileInTail)[0]
    baseNameOut=baseNameIn + suffixOut + "." + extOut
    fileOut=addPath(pathOut,baseNameOut)

    return(fileOut)

def toLatin(str):
    # Decode attribute doesn't exist for string objects in Py 3, but is needed
    # to avoid Unicode decode errors writing XML in Py 2.7.
    try:
        return (str.decode("iso-8859-15","strict"))
    except AttributeError:
        return(str)
        
def toUTF8(str):
    # Decode attribute doesn't exist for string objects in Py 3, but is needed
    # to avoid Unicode decode errors writing XML in Py 2.7.
    try:
        return (str.decode("utf-8","strict"))
    except AttributeError:
        return(str)

def removeFile(file):
    try:
        if os.path.isfile(file)==True:
            os.remove(file)
    except Exception:
        msg= "Could not remove " + file
        errorExit(msg)
