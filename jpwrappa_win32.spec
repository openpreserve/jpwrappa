# -*- mode: python -*-
a = Analysis(['jpwrappa.py'],
             #pathex=['F:\\johan\\pythonCode\\jpwrappa'],
             pathex=['.'],
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
               [('./profiles/default.xml','./profiles/default.xml','DATA')],
               [('./profiles/demoLosslessHarvard.xml','./profiles/demoLosslessHarvard.xml','DATA')],
               [('./profiles/demoLossyHarvard.xml','./profiles/demoLossyHarvard.xml','DATA')],
               [('./profiles/demoLossyJpylyzer.xml','./profiles/demoLossyJpylyzer.xml','DATA')],
               [('./profiles/demoMasterLossless.xml','./profiles/demoMasterLossless.xml','DATA')],
               [('./profiles/demoAccessLossy.xml','./profiles/demoAccessLossy.xml','DATA')],
               [('./profiles/optionsKBMasterLossless.xml','./profiles/optionsKBMasterLossless.xml','DATA')],
               [('./profiles/optionsKBAccessLossy.xml','./profiles/optionsKBAccessLossy.xml','DATA')],
               a.zipfiles,
               a.zipfiles,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name=os.path.join('dist_win32', 'jpwrappa'))
