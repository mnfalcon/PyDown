# PyDown
A simple **windows** app to download YouTube videos

## Libraries used
- PyTube
- PySimpleGUI
- Cx_freeze

# How to use (read further below if you wish to freeze it aka have it as an .exe)
Make sure you've installed PyTube and PySimpleGUI. Have PyDown.py and basicLogger.py in the same folder, run PyDown.py with Python 3.5.

# How to use as an app
### - First you should have installed the above mentioned libraries.
### - From cmd (or command prompt) navigate to the folder where PyDown.py is.
Quick walkthrough: if you need to switch to another drive, use the drive letter followed by ":;". For example, to go to the E drive use "E:;" and move on from there.
Then just use "cd" followed by the folder name/names. Or you can just copy the path from windows explorer and paste it after cd.
### - Once you are in the folder from the command line, use the following command: python setup.py build
This will generate a "build" folder with the .exe file in there and all the required files in there.
### - Make sure the file doesn't trigger a false-positive with your antivirus, otherwise some functionalities won't work because they rely on creating a folder or editing a file name.

# Features
- Download a complete playlist or mix from youtube. Playlists will be downloaded to a subfolder in the download directory. Either as Mp3 or Mp4. There's a tickbox.
- Download a single video as Mp3 or Mp4. You can give a custom name to these single downloads. For now all videos are downloaded at the highest quality. Specially long videos may freeze the app.
- Select download location.
- Progress bar
- Open download directory
- View download history
- Most events are logged into the console. Some exceptions are saved to a log file.

I'm aware this app has a few errors, but at this date of publishing it serves my needs. Comments and suggestions on how to fix something or how to improve it are much appreciated.
