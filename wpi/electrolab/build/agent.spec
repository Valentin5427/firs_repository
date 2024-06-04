# -*- mode: python -*-
ROOT_PATH = '../..'

from glob import glob
import os

def getTOC(prefix, mask, type_='DATA'):
    global glob
    return [(os.path.join(prefix, os.path.split(filename)[1]), filename, type_) for filename in glob(mask)]


a = Analysis([os.path.join(HOMEPATH,'support/_mountzlib.py'),
				os.path.join(HOMEPATH,'support/useUnicode.py'),
				os.path.join(ROOT_PATH, 'dpframe/uiagentsvc.py'),
				],
             pathex=[ROOT_PATH],
            )

pyz = PYZ(a.pure)

exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name=os.path.join('build/pyi.win32/uiagentsvc', 'agent.exe'),
          debug=False,
          strip=False,
          upx=True,
          console=True )

svc = EXE(name='pythonservice.exe')

coll = COLLECT(exe, svc,
               a.binaries,
               a.zipfiles,
               a.datas,
               getTOC('./tasks', '../tasks/*.tsk', 'DATA'),
               getTOC('.', os.path.join(ROOT_PATH, 'dpframe/agent.cfg'), 'DATA'),
               strip=False,
               upx=True,
               name='dist/agent')
