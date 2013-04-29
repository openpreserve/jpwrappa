#! /usr/bin/env python
#
# 
# Requires Python v. 2.7 OR Python 3.2 or better 
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

import sys
import os
import imp
import argparse
import time
import glob
import subprocess as sub
import etpatch as ET
import shared
scriptPath, scriptName = os.path.split(sys.argv[0])

__version__= "0.1.6"

def main_is_frozen():
    return (hasattr(sys, "frozen") or # new py2exe
            hasattr(sys, "importers") # old py2exe
            or imp.is_frozen("__main__")) # tools/freeze

def get_main_dir():
    if main_is_frozen():
        return os.path.dirname(sys.executable)
    return os.path.dirname(sys.argv[0])
       
def getConfiguration():

    # From where is this script executed?)
    applicationPath=os.path.abspath(get_main_dir())

    # Configuration file
    configFile=shared.addPath(applicationPath,"config.xml")

    # Check if config file exists and exit if not
    shared.checkFileExists(configFile)
    
    # Read contents to bytes object
    configBytes=shared.readFileBytes(configFile)

    # Parse XML tree
    try:
        root=ET.fromstring(configBytes)
    except Exception:
        msg="error parsing " + configFile
        shared.errorExit(msg)
    
    # Create empty element object & add config contents to it
    # A bit silly but allows use of findElementText in etpatch 
    
    config=ET.Element("bogus")
    config.append(root)
    
    j2kDriverApp=config.findElementText("./config/j2kDriverApp")
    exifToolApp=config.findElementText("./config/exifToolApp")
        
    # Default JP2 profile    
    jp2ProfileDefault=os.path.normpath(applicationPath + "/profiles/default.xml")
    
    # Normalise all paths
    j2kDriverApp=os.path.normpath(j2kDriverApp)
    exifToolApp=os.path.normpath(exifToolApp)
    
    # Check if j2kDriverApp and jp2ProfileDefault exist, and exit if not
    shared.checkFileExists(j2kDriverApp)
    shared.checkFileExists(jp2ProfileDefault)
    
    return(j2kDriverApp,exifToolApp,jp2ProfileDefault)

def parseJp2Profile(jp2Profile):
    
    # Read profile contents to bytes object
    profileBytes=shared.readFileBytes(jp2Profile)
    
    # Parse XML tree
    try:
        root = ET.fromstring(profileBytes)
    except Exception:
        msg="error parsing " + jp2Profile
        shared.errorExit(msg)
    
    options=root.find("./aware")
    
    # Initialise 2 lists to store results
    # Earlier version used dictionary, but some Aware options may have more
    # than one occurrence, so that doesn't work!
    # TODO: Why not use element instead?
    optionNames=[]
    optionValues=[]
    
    for node in options.iter():
        # Iter returns child elements as well as element itself!
        if node.tag!="aware":
            optionNames.append(node.tag)
            optionValues.append(node.text)
    
    return(optionNames,optionValues)

def parseCommandLine():
    # Create parser
    parser = argparse.ArgumentParser(description="Compress image(s) to JP2",version=__version__)
 
    # Add arguments
    parser.add_argument('imageIn', action="store", help="input image(s)")
    parser.add_argument('imageOut', action="store", help="output JP2 image (or directory where output images are written)")
    parser.add_argument('-p', action="store", dest="profile", default="", help="JP2 profile")
    parser.add_argument('-s', action="store", dest="suffix", default="", help="suffix added to base name of output images")
    parser.add_argument('-m', action="store_true", dest="flagMetadata", default=False, help="embed metadata from input image (requires ExifTool)")
    parser.add_argument('-l', action="store_true", dest="flagLogging", default=False, help="print XML-formatted log to stdout")
    # Parse arguments
    args=parser.parse_args()
    
    return(args)

def awareInputImageString(fileName):
    iString="--set-input-image " + fileName
    return iString

def awareOutputImageString(fileName):
    oString="--output-file-name " + fileName
    return oString

def awareMetadataString(fileName):
    mString="--set-output-jp2-add-metadata-box XML " + fileName
    return mString

def optionsToString(optionNames,optionValues):

    # Reads lists with all Aware encoding options and return
    # corresponding command-line string

    optionsString=""

    for i in range(len(optionNames)):
        optionName=optionNames[i]
        optionValue=optionValues[i]
        optionsString=optionsString + "--" + optionName + " " + optionValue + " "

    return optionsString

def jp2CreationInfo(jp2ImageOut):
    # Check if output image was created (Aware exit status doesn't really help here),
    # and print info to screen 
    if os.path.isfile(jp2ImageOut)==False:
        jp2Created=False
        shared.printWarning(jp2ImageOut + " not created! \n")
    else:
        shared.printInfo("created output image " + jp2ImageOut + "\n")
        jp2Created=True
    
    return jp2Created 

def launchSubProcess(systemString):
    # Launch subprocess and return exit code, stdout and stderr
    try:
        # Execute command line; stdout + stderr redirected to objects
        # 'output' and 'errors'.
        p = sub.Popen(systemString,stdout=sub.PIPE,stderr=sub.PIPE)
        output, errors = p.communicate()
                
        # Decode to UTF8
        outputAsString=output.decode('utf-8')
        errorsAsString=errors.decode('utf-8')
                
        exitStatus=p.returncode
  
    except Exception:
        # I don't even want to to start thinking how one might end up here ...
        exitStatus=-99
        outputAsString=""
        errorsAsString=""
    
    return exitStatus,outputAsString,errorsAsString

def convertOneImageToJP2(imageIn,imageOut,awareOptionsString,exifToolApp,j2kDriverApp,extractMetadataFlag):

    # Convert one image to JP2. Arguments:
    #
    # imageIn: name of input image
    # imageOut: name of output JP2 image
    # awareOptionsString: text string with Aware options
    # exifToolApp: path to ExifTool executable
    # j2kDriverApp: path to Aware executable
    # extractMetadataFlag: True if metadata extraction is needed, False otherwise

    # Initialise exit status flag + output strings for ExifTool /Aware
    # (in case extractMetadataFlag equals 0)
    exifExitStatus=0
    awareExitStatus=0
    exifStdOut=""
    exifStdErr=""
    awareStdOut=""
    awareStdErr=""
       
    # If output image already exists, delete it! Why this? -->
    # 1. If the conversion proceeds as planned, it will be overwritten anyway, BUT ...
    # 2. If something goes wrong and the image cannot be created, the absence of 
    #    the output image may be the only way to find out about this afterwards
    #    (because we cannot rely on Aware's exit status for this, see below)
    shared.removeFile(imageOut)

    # Absolute path to output image (location also used for temporary file)
    pathOut=os.path.abspath(os.path.split(imageOut)[0])

    # Metadata extraction (optional)

    # Initialise Aware command line option for metadata embedding
    aMetadata=""

    if extractMetadataFlag==True:
        # Generate name for (temporary) xmp file
        fileXMP=shared.constructFileName(imageIn,pathOut,"xmp","")
        
        # If previous run of aWrapper was terminated by the user, a file with this
        # name could still be there (and this would raise an error in ExifTool)
        shared.removeFile(fileXMP)

        # Extract metadata from input image and store result in XMP format
        exifSysString=shared.quoteString(exifToolApp) + " " + imageIn + " -o " + fileXMP
        shared.printInfo("running ExifTool")
        
        exifExitStatus,exifStdOut,exifStdErr=launchSubProcess(exifSysString)
                
        # Generate Aware command line option for metadata embedding
        aMetadata=awareMetadataString(fileXMP)

    # Construct encoder command line 
    aInput=awareInputImageString(imageIn)
    aOutput=awareOutputImageString(imageOut)
    awareSysString=(shared.quoteString(j2kDriverApp) + " " + aInput + " " + awareOptionsString + " " +
                aMetadata + " " + aOutput)

    # Run encoder, but only if ExifTool didn't give any errors.
   
    if exifExitStatus==0:
        shared.printInfo("running Aware j2kdriver ...")
        awareExitStatus,awareStdOut,awareStdErr=launchSubProcess(awareSysString)
    else:
        shared.printWarning(imageIn + " not converted because ExifTool exited with errors! \
        See log file for details.")
        
    # Check if output image was really created and print info to screen
    # (Note that Aware can give exit code 0 even if things go seriously wrong!)
    jp2Created=jp2CreationInfo(imageOut)
    
    if extractMetadataFlag==True and exifExitStatus==0:
        # Clean up temporary file
        os.remove(fileXMP)
       
    # Create element object for storing conversion info
    conversionInfo=ET.Element('image')
    
    # Pre-format all output
    timeStr=time.asctime()  
    imageIn=shared.toUTF8(os.path.abspath(imageIn))
    imageOut=shared.toUTF8(os.path.abspath(imageOut))
    jp2Created=str(jp2Created)
    exifExitStatus=str(exifExitStatus)
    exifStdOut=shared.toUTF8(exifStdOut)
    exifStdErr=shared.toUTF8(exifStdErr)
    awareExitStatus=str(awareExitStatus)
    awareStdOut=shared.toUTF8(awareStdOut)
    awareStdErr=shared.toUTF8(awareStdErr)
    
    # Add to element  
    conversionInfo.appendChildTagWithText("time", timeStr)       
    conversionInfo.appendChildTagWithText("imageIn", imageIn)
    conversionInfo.appendChildTagWithText("imageOut", imageOut)
    conversionInfo.appendChildTagWithText("jp2Created", jp2Created)
    conversionInfo.appendChildTagWithText("exifExitStatus", exifExitStatus)
    conversionInfo.appendChildTagWithText("exifStdOut", exifStdOut)
    conversionInfo.appendChildTagWithText("exifStdErr", exifStdErr)
    conversionInfo.appendChildTagWithText("awareExitStatus", awareExitStatus)
    conversionInfo.appendChildTagWithText("awareStdOut", awareStdOut)
    conversionInfo.appendChildTagWithText("awareStdErr", awareStdErr)
    
    # Return conversion info
    return(conversionInfo)
    
def imagesToJP2(imagesIn,fileOut,jp2Profile,suffixOut,flagMetadata):
    
    # Convert one or more images to JP2. Arguments:
    #
    # - imagesIn: list of input image(s)
    # - fileOut: name of output JP2 image or directory for writing output images
    # - jp2ProfileName: name of JP2 options profile (e.g. KB_lossless / KB_lossy)
    # - suffixOut: suffix that is added to names of output images (this does NOT
    #     include the file extension, and by default it is an empty text string)
    # - flagMetaData: True if metadata extraction is needed, False otherwise
    #
    # Returns all output images as list

    # Get configuration settings (yields paths to j2kDriverApp and exifToolApp,
    # log file and default JP2profile)
    j2kDriverApp,exifToolApp,profileDefault=getConfiguration()
    
    if flagMetadata==True:
        shared.checkFileExists(exifToolApp)
    
    # Create element object that will hold log info
    log=ET.Element('jpwrappa')
        
    # Use default JP2 profile if profile is not specified 
    if jp2Profile=="":
        jp2Profile=profileDefault
           
    # Does JP2 profile exist?
    shared.checkFileExists(jp2Profile)

    # Parse JP2 profile
    optionNames, optionValues=parseJp2Profile(jp2Profile)

    # Options to text string
    aOptionsAsString=optionsToString(optionNames,optionValues)
    
    # Number of input images
    numberOfImages=len(imagesIn)
    
    # Does fileOut point to a directory?
    fileOutIsDir=os.path.isdir(fileOut)
    
    # If we have multiple input images fileOut should be a directory
    if numberOfImages > 1 and fileOutIsDir==False:
        msg=fileOut + " : expected directory"
        shared.errorExit(msg)
            
    # Create list for storing names of output images
    imagesOut=[]
    
    # Create list of output image names
    if fileOutIsDir==False:
        imagesOut.append(fileOut)
    else:
        for i in range(numberOfImages):
            imageIn=imagesIn[i]
            imageOut=shared.constructFileName(imageIn,fileOut,"jp2", suffixOut)
            imagesOut.append(imageOut)
    
    # Convert all images
    for i in range(numberOfImages):
        
        imageIn=imagesIn[i]
        imageOut=imagesOut[i]
        
        # Convert image
        conversionInfo=convertOneImageToJP2(imageIn,imageOut,aOptionsAsString,exifToolApp,
            j2kDriverApp,flagMetadata)
            
        # Add reference to profile to conversionInfo    
        conversionInfo.appendChildTagWithText("profile", jp2Profile)
        
        # Add as child to log element
        log.append(conversionInfo)
                        
    return(imagesOut,log)

def main():
    # Get input from command line
    args=parseCommandLine()
    imageIn=args.imageIn
    imageOut=args.imageOut
    jp2Profile=args.profile
    suffixOut=args.suffix
    flagMetadata=args.flagMetadata
    flagLogging=args.flagLogging

    # Input image(s) as file list
    imagesIn=glob.glob(imageIn)
        
    # Normalise output images(s) path (may be a directory!) 
    imageOut=os.path.normpath(args.imageOut)
    
    # Normalise profile path (if a profile is provided)
    if jp2Profile != "":    
        jp2Profile=os.path.normpath(jp2Profile)    
       
    # Perform conversion
    imagesOut,log=imagesToJP2(imagesIn,imageOut,jp2Profile,suffixOut,flagMetadata)
    
    if flagLogging==True:
        # Write xml-formatted log to stdout
        sys.stdout.write(log.toxml().decode('ascii'))
    
    
if __name__ == "__main__":
    main()

