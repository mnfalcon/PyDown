from urllib.request import urlopen
import urllib.response
from io import BytesIO
from zipfile import ZipFile
import json
import os
import PySimpleGUI as sg
import basicLogger
import threading
from time import gmtime, sleep, strftime
from constants import PyDownVersion
import subprocess


sg.theme('DarkAmber')
launcherLayout = [
    [sg.Output(size=(141,10), key='log', visible=True)],
    [sg.Text('Download progress'), sg.Text('', key='progressPercentage'), sg.Text('%'), sg.ProgressBar(100, orientation='h', size=(20,20), key='progressBar'), sg.Text(' '*144), sg.Cancel(button_text='Exit', size=(6,1))]
    ]
window = sg.Window('PyDown Launcher', launcherLayout, finalize=True)

while True:
    event, values = window.read(timeout=100)
    if event == sg.WIN_CLOSED or event == 'Exit' or event == sg.WIN_X_EVENT:
        break
    
    try:
        release = json.loads(urlopen("https://api.github.com/repos/mnfalcon/PyDown/releases/latest").read().decode("utf-8"))
        if (float(release["tag_name"].strip("v")) <= PyDownVersion):
            print("Version is already up to date. Skipping...")
            exe = r"PyDown " + release["tag_name"] + "/PyDown.exe"
            threading.Thread(subprocess.check_call([exe])).start()
            window.close()
            break
        url = release["assets"][0]["browser_download_url"]
        with urlopen(url) as Response:
            Length = Response.getheader('content-length')
            BlockSize = 1000000  # default value

            if Length:
                Length = int(Length)
                BlockSize = max(4096, Length // 20)

            BufferAll = BytesIO()
            Size = 0
            while True:
                BufferNow = Response.read(BlockSize)
                if not BufferNow:
                    break
                BufferAll.write(BufferNow)
                Size += len(BufferNow)
                if Length:
                    Percent = int((Size / Length)*100)
                    window["progressBar"].UpdateBar(Percent)
                    window["progressPercentage"].Update(Percent)
            
            zipfile = ZipFile(BufferAll)
            zipfile.extractall(path=".")

    except Exception as exc:
        print(exc)
        time = strftime('%d-%b-%Y', gmtime())
        hour = strftime('%H-%M-%S', gmtime())
        if not os.path.exists('logs'):
            os.makedirs('logs')
        dump = open('logs/{}.txt'.format(time), 'a')
        dump.write('{} | {} \n'.format(hour, exc))
        dump.close()
      
window.close()