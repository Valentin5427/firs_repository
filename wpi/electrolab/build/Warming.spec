# -*- mode: python -*-
ROOT_PATH = '../..'
    
from glob import glob
import os

def getTOC(prefix, mask, type_='DATA'):
    global glob
    return [(os.path.join(prefix, os.path.split(filename)[1]), filename, type_) for filename in glob(mask)]


a = Analysis([os.path.join(HOMEPATH,'support/_mountzlib.py'), 
				os.path.join(HOMEPATH,'support/useUnicode.py'), 
				os.path.join(ROOT_PATH, 'electrolab/gui/Warming.py'),
				],
             pathex=[ROOT_PATH],
             hookspath=[os.path.join(SPECPATH, 'hooks/Warming')]
            )

pyz = PYZ(a.pure)

exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name=os.path.join('build/pyi.win32/Warming', 'Warming.exe'),
          debug=False,
          strip=False,
          upx=True,
          console=False )

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               getTOC('.', '../gui/*.json', 'DATA'),
               getTOC('.', '../gui/*.cfg', 'DATA'),
               getTOC('./ui', '../gui/ui/*.ui', 'DATA'),
               getTOC('./ui', '../gui/ui/ico_rc.py', 'PYMODULE'),
               getTOC('./ui', '../gui/ui/ico_64_rc.py', 'PYMODULE'),
               getTOC('.', '../dependencies/*.*', 'DATA'),
               getTOC('./rpt', '../gui/rpt/*.fr3', 'DATA'),
               getTOC('./rpt', '../gui/rpt/*.xls', 'DATA'),
               getTOC('./rpt', '../gui/rpt/*.xml', 'DATA'),
               strip=False,
               upx=True,
               name='dist/Warming')