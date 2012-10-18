# About this document
*Jpwrappa* User Manual 2 October 2012.   
Author: Johan van der Knijff, [KB / National Library of the Netherlands][kb]. 


# What is *jpwrappa*?
*Jpwrappa* is a small Python tool that provides an easy-to-use interface to the *j2kdriver* application that is part of [Aware’s JPEG 2000 SDK][aware]. *Aware*'s encoder is very feature rich, however since all encoding options are provided as command-line arguments, this may result in excessively lengthy command lines. Here's an example:
<pre>
j2kdriver --set-input-image balloon.tif --set-output-type JP2 --set-output-j2k-xform
I97 5 --set-output-j2k-color-xform YES --set-output-j2k-progression-order RPCL --set-
output-j2k-tile-size 1024 1024 --set-output-j2k-codeblock-size 6 6 --set-output-j2k-
channel-precinct-size ALL 0 7 7 --set-output-j2k-channel-precinct-size ALL 1 7 7 --
set-output-j2k-channel-precinct-size ALL 2 7 7 --set-output-j2k-channel-precinct-size
ALL 3 7 7 --set-output-j2k-channel-precinct-size ALL 4 8 8 --set-output-j2k-channel-
precinct-size ALL 5 8 8 --set-output-j2k-layers 8 --set-output-j2k-layer-ratio 0 2560
--set-output-j2k-layer-ratio 1 1280 --set-output-j2k-layer-ratio 2 640 --set-output-
j2k-layer-ratio 3 320 --set-output-j2k-layer-ratio 4 160 --set-output-j2k-layer-ratio
5 80 --set-output-j2k-layer-ratio 6 40 --set-output-j2k-layer-ratio 7 20  --set-
output-j2k-error-resilience ALL  --set-output-jp2-add-metadata-box XML balloon.xmp --
output-file-name balloon.jp2
</pre>

Although it’s entirely possible to call the encoder from a batch file or shell script in the above way, this is not always a practical solution: it is quite hard to keep an overview of what’s going on, and the meaning of most of the arguments is not immediately obvious. Moreover, any modifications of existing sets of options will introduce the risk of something going wrong, and this may go completely unnoticed.

The *jpwrappa* software solves this problem by putting all encoding options in a formatted XML file. These files can be re-used, and may include comments (making them largely self-documenting). The wrapper software simply parses the options in the XML file, uses this information to create the Aware command line, and finally launches the encoder. Optionally metadata from a source image may be extracted from the source image, and embedded as an XML box in the JP2 (this functionality requires [ExifTool][exiftool]).

Using *jpwrappa*, the sequence of command-line arguments in the example above can be reduced to something as simple as this:

`
jpwrappa.py balloon.tif balloon.jp2 –p demoAccesslossy.xml
` 

*Jpwrappa* can either be used as a command-line tool, or as an importable module that can be called from other *Python* scripts.

# Funding
The development of *jpwrappa* was partially funded by the EU FP 7 project SCAPE (SCAlabable Preservation Environments). More information about SCAPE can be found here:

[http://www.scape-project.eu/][scape]

# License
*Jpwrappa* is licensed under the Apache License, Version 2.0. (the "License"). You may obtain a copy of the License at:

[http://www.apache.org/licenses/LICENSE-2.0][apacheLicense]

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

# Command-line syntax

`
usage: jpwrappa.py [-h] [-v] [-p PROFILE] [-s SUFFIX] [-m] [-l]
                   imageIn imageOut
`

## Positional arguments

- imageIn: input image(s)  
- imageOut: output JP2 image (or directory where output images are written)

## Optional arguments
- -h, --help:show help message and exit    
- -v, --version: show program's version number and exit    
- -p PROFILE: JP2 profile    
- -s SUFFIX: suffix added to base name of output images   
- -m: embed metadata from input image (requires ExifTool)    
- -l: print XML-formatted log to stdout    

## Examples

Convert TIFF to JP2 using the default profile:
`jpwrappa.py balloon.tif balloon.jp2`

As above, but using the *demoAccessLossy* profile:
`jpwrappa.py balloon.tif balloon.jp2 -p demoAccessLossy.xml`

Convert all TIFF images in working directory to JP2, adding suffix *\_test* to output JP2s:
`jpwrappa.py *.tif . -p demoAccessLossy.xml -s _test`

(In this case, *balloon.tif* will be converted to *balloon\_test.jp2*.)

As above, but generate XML-formatted log file:

`jpwrappa.py *.tif . -p demoAccessLossy.xml -s _test -l > log.xml`

# Using *jpwrappa* as an importable Python module
The *jpwrappa* functions can also be imported in (and used by) other Python 
scripts. This involves 2 steps:

1. Import *jpwrappa* in your own script by adding the following line at the top:
`import jpwrappa`

2. Now call the *imagesToJP2* function, which uses the following syntax:

`imagesOut,log=jpwrappa.imagesToJP2(imagesIn,fileOut,jp2Profile,suffixOut,flagMetadata)`

## Arguments
  
- imagesIn: list of input image(s)   
- fileOut: name (including path) of output JP2 image, or directory for writing output images    
- jp2Profile: JP2 profile file   
- flagMetadata: flag that is *True* if metadata are extracted from the input image(s), and *False* otherwise

## Output
- imagesOut: a list object with the names of all generated output images   
- log: an *element* object that contains logging information (can easily be written as XML if needed)


# JP2 profiles
The JP2 profile contains the encoding settings. The minimal example below shows the basic layout of the file:

![](profileDefault.png)
<!-- ![](https://raw.github.com/openplanets/jpwrappa/master/doc/profileDefault.png) -->

So the file's root element is *options*, which has a child element *aware* which contains the encoding options. The naming of these options is based on the naming used in Chapter 9 (‘Command Line Tools’) of the *Aware* manual, using the following naming convention:

**Aware option**:  `--aware-option value`   
**Jpwrappa equivalent**: `<aware-option>value</aware-option>` 

## Examples
**Aware**: `-- set-output-j2k-progression-order RPCL`  
**Jpwrappa**: `<set-output-j2k-progression-order>RPCL</set-output-j2k-progression-order>` 

**Aware**: `--set-output-j2k-xform I97 5`  
**Jpwrappa**: `<set-output-j2k-xform>I97 5</set-output-j2k-xform>` 

Note that the order in which *Aware*'s options are given on the command line influences the results. *Jpwrappa* always uses the exact order that is used in the profile. Note that you can use XML comments to annotate your profiles and make them self-documented.

# Logging
You can generate detailed logging information on each converted image using the *-l* switch. 

Each log entry contains the following information: 

- Log entry creation date and time
- Names of input and output images
- Information on whether the output image was created
- Information on whether metadata extraction was enabled
- A reference to the JP2 profile that was used  
- The exit status of the *Aware* encoder (and *ExifTool*, if metadata extraction was enabled)
- Standard output and standard error output from the *Aware* encoder (and *ExifTool*,if metadata extraction was enabled)

As an example, below is a log entry for an image that could not be converted (in fact this was a zero-byte file):

![](logError.png)

<!-- ![](https://raw.github.com/openplanets/jpwrappa/master/doc/logError.png) -->


# Error handling
Especially in case of the batch processing on multiple images it is important that one or two ‘bad’ input images  do not cause a crash of the whole batch process. Perhaps even more importantly, any errors should be traceable. One problem is that the exit status of the *Aware* j2kdriver application is not a reliable indicator for establishing whether an image was converted successfully. *Jpwrappa* tries to handle any problems with *ExifTool* and/or the j2kdriver application in the following way:

1.	If metadata extraction is enabled, it calls *ExifTool* to extract metadata to an XMP file. If *ExifTool* encounters any problems, *ExifTool* generates an error which is reported in its exit status. This exit status is reported back to *jpwrappa* and added to the log file.
2.	If *ExifTool*’s exit status is not equal to 0 (meaning that *ExifTool* encountered some problem), *jpwrappa* will not call *Aware*’s j2kdriver application. 
3.	If *ExifTool*’s exit status is equal to 0 (meaning that *ExifTool* ran without any problems), *jpwrappa* will call *Aware*’s j2kdriver application to do the conversion.
4.	In order to ensure that the file really was converted, *jpwrappa* performs a final check on the existence of the output JP2 image. Based on the outcome of this, it then  either reports a message to the log file saying that the output image was created, or a warning that it was not created (see example above).
5.	In case *jpwrappa* encounters any of the aforementioned errors while processing one input image,it will simply proceed to the next image (after reporting the relevant message(s) to the log file).

# Environment limitations
Depending on the operating system that is used, there is a limit on the number of characters that can be used in a command line. This is important, as *jpwrappa* works by transforming the information in the options file to a valid *Aware* command line. For Windows XP and more recent, the maximum number of characters equals 8191; for older versions a limit of 2047 characters applies [[1]][ms].  On Linux/Unix systems, the actual value depends on the specific flavour, but in general it will exceed the Windows value by several orders of magnitude.  Just to give an indication: the example command line that is given in the introduction in this User Manual is made up of 1067 characters. So, these limitations are unlikely to cause any major problems, unless extremely long file paths are used for the in- and output files.


 

[apacheLicense]: http://www.apache.org/licenses/LICENSE-2.0
[scape]: http://www.scape-project.eu/
[aware]:http://www.aware.com/imaging/jpeg2000sdk.html
[exiftool]:http://owl.phy.queensu.ca/~phil/exiftool/
[kb]:www.kb.nl
[ms]:http://support.microsoft.com/kb/830473
