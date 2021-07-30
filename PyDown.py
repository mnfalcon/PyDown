from pytube import YouTube, Playlist
import os
import PySimpleGUI as sg
import logging
import threading
import basicLogger
from time import gmtime, strftime

# TO DO: 
# - Custom Logging | Move logger to another file
# - String handling for weird or special characters DONE
# - Save log files for 30 days
# - Download History
# - Radio Button for Playlist (mp3/mp4) DONE
# - Read more on threading
# - Read more on cx_freeze

sg.theme('DarkAmber')
layout = [
    [sg.Text('Output Path: '), sg.InputText(key='outputDisplay', default_text='downloads'), sg.FolderBrowse(key='outputDir', target='outputDisplay'), sg.Button('Reset Output Path',key='Reset'), sg.Button('Download History'), sg.Button('Open Download Directory')],
    [sg.Text('YouTube video URL: '), sg.InputText(key='videoURL'), sg.Button('Clear URL'), sg.Text('Output Name (optional)', tooltip='Use this if there are any weird characters'), sg.InputText(key='custom_name')], 
    [sg.Button('Download MP3'), sg.Button('Download Video'), sg.Button(button_text='Toggle Debug Console', key='debug'), 
    sg.Button('Download Playlist'), sg.Text('as'), sg.Checkbox('MP3', key='checkbox_mp3', default=True, size=(6,6),tooltip='If true, playlist will be downloaded as mp3. Else, as mp4')],
    [sg.Output(size=(141,10), key='log', visible=True)],
    [sg.Text('Download progress'), sg.ProgressBar(100, orientation='h', size=(20,20), key='progressBar'), sg.Text(' '*147), sg.Cancel(button_text='Exit', size=(6,1))]
    ]
window = sg.Window('PyDown', layout, finalize=True)

downloadHistory = open('downloadHistory.txt', 'a')
if not os.path.exists('downloads'):
    os.makedirs('downloads')
    
def removeSpecialChars(string: str):
    return string.translate({ord(i): None for i in ':.\\#%+=\'\"&{@};<>$*!?`|/'})

def setOutput(dir):
    default = '\downloads'
    if dir == 'undefined':
        outputPath = default
        window['outputDir'].update(default)
        window['outputDisplay'].update(default)
        if not os.path.exists(default):
            print('Generating default folder')
            os.makedirs(default)
    else:
        outputPath = dir
    return outputPath

def saveHistory(url, title):
    time = strftime('%a, %d %b %Y %H:%M:%S', gmtime())
    downloadHistory.write('{} | {} : {}\n'.format(time, url, title))

def openDownloadHistory():
    os.startfile('downloadHistory.txt')

def openDownloadDirectory(path):
    os.startfile(path, 'explore')

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining 

    liveprogress = (int)((bytes_downloaded / total_size) * 100)
    window['progressBar'].UpdateBar(liveprogress)

def downloadMP3(url, dir='undefined', outputName=''):
    try:
        print('Starting download...')
        outputPath = setOutput(dir)
        yt = YouTube(url, on_progress_callback=on_progress)
        if outputName != '':
            videoTitle = outputName
        else:
            videoTitle = yt.title
        #removing all special characters not allowed when naming windows files
        fileName = removeSpecialChars(videoTitle)

        yt.streams.get_audio_only().download(output_path=outputPath, filename = fileName, max_retries=10)
        print('YouTube audio downloaded successfully. {} : {} | at {}'.format(fileName, url, outputPath))
    
        mp4File = outputPath + '/' + fileName + '.mp4'
        mp3File = outputPath + '/' + fileName + '.mp3'
        os.rename(mp4File, mp3File)
        print('File renamed successfully.')
    except Exception as e:
        os.remove(mp4File)
        print(e)
    saveHistory(url, fileName)

def downloadVideo(url, dir='undefined', outputName=''):
    print('Starting download...')
    outputPath = setOutput(dir)
    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        if outputName != '':
            videoTitle = outputName
        else:
            videoTitle = yt.title
        fileName = removeSpecialChars(videoTitle)
        yt.streams.get_highest_resolution().download(output_path=outputPath, filename=fileName, max_retries=10)
        print('YouTube video downloaded successfully. {} : {} | at {}'.format(fileName, url, outputPath))
    except Exception as e:
        print(e)
    saveHistory(url, fileName)

def downloadPlaylist(url, bType, dir='undefined'):
    outputPath = setOutput(dir)
    pl = Playlist(url)
    folderName = removeSpecialChars(pl.title)
    outputPath += '/{}'.format(folderName) 
    for url in pl.video_urls:
        if bType:
            threading.Thread(target=downloadMP3(url, outputPath)).start()
        else:
            threading.Thread(target=downloadVideo(url, outputPath)).start()
        window.Refresh()
    print('Playlist has finished downloading.')

def toggleConsole():
    if window['log'].visible == False:
        window['log'].update(visible=True)
    else:
        window['log'].update(visible=False)

while True:
    event, values = window.read(timeout=100)
    outputPath = values['outputDisplay']
    if event == sg.WIN_CLOSED or event == 'Exit' or event == sg.WIN_X_EVENT:
        break
    
    try:
        # outputPath = values['outputDisplay']
        videoURL = values['videoURL']
        if event == 'Download MP3':
            threading.Thread(target=downloadMP3(videoURL, outputPath, values['custom_name'])).start()
        elif event == 'Download Video':
            threading.Thread(target=downloadVideo(videoURL, outputPath, values['custom_name'])).start()
        elif event == 'Download Playlist':
            threading.Thread(target=downloadPlaylist(videoURL, values['checkbox_mp3'], outputPath)).start()
        elif event == 'debug':
            toggleConsole()
        elif event == 'Run':
            logging.info('Running')
        elif event == 'Clear URL':
            window['videoURL']('')
        elif event == 'Reset':
            window['outputDisplay']('downloads')
        elif event == 'Download History':
            threading.Thread(target=openDownloadHistory).start()
        elif event == 'Open Download Directory':
            threading.Thread(target=openDownloadDirectory(outputPath)).start()
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
downloadHistory.close()