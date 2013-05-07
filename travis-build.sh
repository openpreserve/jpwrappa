#!/bin/sh 
python Makespec.py --onefile ./jpwrappa/jpwrappa.py
python pyinstaller.py jpwrappa.spec
