import sys
from cx_Freeze import setup, Executable
build_exe_options = {"packages": ["os"]}
base = None
if sys.platform == "win32":
  base = "Win32GUI"
setup(name="text",
      version="0.1",
      description="My GUI application!",
      options={"build_exe": build_exe_options},
      executables=[Executable("D:\Рабочий стол\Python project2\\Result_HV.py", base=base)])





# """
# A simple setup script to create an executable using PyQt5. This also
# demonstrates the method for creating a Windows executable that does not have
# an associated console.
# PyQt5app.py is a very simple type of PyQt5 application
# Run the build process by running the command 'python setup.py build'
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the application
# """
#
# import sys
#
# from cx_Freeze import Executable, setup
#
# try:
#     from cx_Freeze.hooks import get_qt_plugins_paths
# except ImportError:
#     include_files = []
# else:
#     # Inclusion of extra plugins (new in cx_Freeze 6.8b2)
#     # cx_Freeze imports automatically the following plugins depending of the
#     # use of some modules:
#     # imageformats - QtGui
#     # platforms - QtGui
#     # mediaservice - QtMultimedia
#     # printsupport - QtPrintSupport
#     #
#     # So, "platforms" is used here for demonstration purposes.
#     include_files = get_qt_plugins_paths("PyQt5", "platforms")
#
# # base="Win32GUI" should be used only for Windows GUI app
# base = None
# if sys.platform == "win32":
#     base = "Win32GUI"
#
# build_exe_options = {
#     "excludes": ["tkinter"],
#     "include_files": include_files,
#     "zip_include_packages": ["PyQt5"],
# }
#
# bdist_mac_options = {
#     "bundle_name": "Test",
# }
#
# bdist_dmg_options = {
#     "volume_label": "TEST",
# }
#
# executables = [Executable("eik.py", base=None, target_name="eik.py")]
#
# setup(
#     name="simple_PyQt5",
#     version="0.3",
#     description="Sample cx_Freeze PyQt5 script",
#     options={
#         "build_exe": build_exe_options,
#         "bdist_mac": bdist_mac_options,
#         "bdist_dmg": bdist_dmg_options,
#     },
#     executables=executables,
# )