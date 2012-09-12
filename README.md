#jpwrappa

## About
_Jpwrappa_ is a simple Python wrapper around the command-line tool of [Aware's JPEG 2000 SDK][1]. It is useful *only* if you have a copy of this software.  *Jpwrappa*'s development was partially supported by the [SCAPE][4] Project. The SCAPE project is co-funded by the European Union under FP7 ICT-2009.4.1 (Grant Agreement number 270137).

Note that this wrapper is in its early stages, and any operational use is strongly discouraged at this stage. All *JP2* profiles that are included with this software are provided for illustrative/demonstration purposes only!

## Command line use

#### Usage
<pre>
jpwrappa.py [-h] [-v] [-p PROFILE] [-s SUFFIX] [-m] [-l]  
            imageIn imageOut
</pre>

#### Positional arguments

`imageIn`: input image(s)  
`imageOut`: output JP2 image (or directory where output images are written)

#### Optional arguments

`-h, --help` : show this help message and exit  
`-v, --version` : show program's version number and exit  
`-p PROFILE` : JP2 profile  
`-s SUFFIX` : suffix added to base name of output images  
`-m` : embed metadata from input image as XML box (requires ExifTool)  
`-l` : print XML-formatted log to stdout  


#### Examples

`jpwrappa.py rubbish.tif rubbish.jp2`

Convert one image to *JP2* using Aware's default settings.

`jpwrappa.py rubbish.tif rubbish.jp2 -p demoLosslessHarvard.xml`

Convert one  image to *JP2* using settings/options defined in profile *demoLosslessHarvard.xml*. 

`jpwrappa.py rubbish.tif rubbish.jp2 -p demoLosslessHarvard.xml -l >log.xml`

Same as above, but generate XML-formatted log that is directed to file *log.xml*.

`jpwrappa.py *.tif . -p demoLosslessHarvard.xml`

Convert all images in current directory with extension *.tif* to *JP2*. Output names are automatically generated from the *TIFF* base names; can be optionally tweaked using `-s` option.

## Documentation

Will follow.
   

[1]: http://www.aware.com/imaging/jpeg2000sdk.html
[4]: http://www.scape-project.eu/