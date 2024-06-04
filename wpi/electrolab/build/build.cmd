rem pyrcc4 ico_64.qrc -o ico_64_rc.py
python C:\pyinstaller-1.5.1\Build.py integration.spec
python C:\pyinstaller-1.5.1\Build.py wpt.spec
python C:\pyinstaller-1.5.1\Build.py wpm.spec
python C:\pyinstaller-1.5.1\Build.py wpi.spec
python C:\pyinstaller-1.5.1\Build.py export1c.spec

iscc.exe electrolab.iss