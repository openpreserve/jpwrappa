# -*- mode: python -*-
a = Analysis(['.\jpwrappa\jpwrappa.py'],
             pathex=['.\jpwrappa'],
             hiddenimports=[],
             hookspath=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name=os.path.join('build\\pyi.win32\\jpwrappa', 'jpwrappa.exe'),
          debug=False,
          strip=None,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries +
               [('./license/LICENSE.txt','LICENSE','DATA')],
               [('./doc/jpWrappaUserManual.html','./doc/jpWrappaUserManual.html','DATA')],
               [('./config.xml','./jpwrappa/config.xml','DATA')],
               [('./profiles/default.xml','./jpwrappa/profiles/default.xml','DATA')],
               [('./profiles/demoAccessLossy.xml','./jpwrappa/profiles/demoAccessLossy.xml','DATA')],
               [('./profiles/demoLosslessHarvard.xml','./jpwrappa/profiles/demoLosslessHarvard.xml','DATA')],
               [('./profiles/demoLossyHarvard.xml','./jpwrappa/profiles/demoLossyHarvard.xml','DATA')],
               [('./profiles/demoLossyJpylyzer.xml','./jpwrappa/profiles/demoLossyJpylyzer.xml','DATA')],
               [('./profiles/demoMasterLossless.xml','./jpwrappa/profiles/demoMasterLossless.xml','DATA')],
               [('./profiles/optionsKBAccessLossy.xml','./jpwrappa/profiles/optionsKBAccessLossy.xml','DATA')],
               [('./profiles/optionsKBMasterLossless.xml','./jpwrappa/profiles/optionsKBMasterLossless.xml','DATA')],
               [('./profiles/optionsKBMasterLossless_2014.xml','./jpwrappa/profiles/optionsKBMasterLossless_2014.xml','DATA')],  [('./profiles/optionsKBAccessLossy_2014.xml','./jpwrappa/profiles/optionsKBAccessLossy_2014.xml','DATA')],  
               [('./profiles/optionsKBMasterLightLossy.xml','./jpwrappa/profiles/optionsKBMasterLightLossy.xml','DATA')],               
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name=os.path.join('dist_win32', 'jpwrappa'))
