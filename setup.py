import sys
from constants import PyDownVersion
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
additional_modules = []

build_exe_options = {"includes": additional_modules,
                     "packages": [ "pytube", "logging", "PySimpleGUI", "os", "threading", "time", "basicLogger", "urllib", "json", "io"],
                     "excludes": [],
                     "include_files": []}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(name="PyDown",
      version=str(PyDownVersion),
      description="Python Video-to-MP3 Downloader",
      options={"build_exe": build_exe_options},
      executables=[Executable(script="PyDown.py", base=base), Executable(script="launcher.py", target_name="PyDownLauncher", base=base)])

# From cmd navigate to folder and use 'python setup.py build'