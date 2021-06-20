from pytube import YouTube, Playlist
import os
import PySimpleGUI as sg
import logging

# TO DO: 
# - Custom Logging
# - String handling for weird or special characters DONE
# - Save log files for 30 days
# - Download History
# - Radio Button for Playlist (mp3/mp4) DONE

sg.theme('DarkAmber')
layout = [
    [sg.Text('Output Path: '), sg.InputText(key='outputDisplay', default_text='downloads'), sg.FolderBrowse(key='outputDir', target='outputDisplay'), sg.Button('Reset Output Path',key='Reset')],
    [sg.Text('YouTube video URL: '), sg.InputText(key='videoURL'), sg.Button('Clear URL'), sg.Text('Output Name (optional)', tooltip='Use this if there are any weird characters'), sg.InputText(key='custom_name')], 
    [sg.Button('Download MP3'), sg.Button('Download Video'),sg.Cancel(button_text='Exit'), sg.Button(button_text='Toggle Debug Console', key='debug'), 
    sg.Button('Download Playlist'), sg.Checkbox('MP3', key='checkbox_mp3', default=True, size=(6,6),tooltip='If true, playlist will be downloaded as mp3. Else, as mp4')],
    [sg.Output(size=(141,10), key='log', visible=True)]
    ]
window = sg.Window('PyDown', layout)

class Handler(logging.StreamHandler):

    def __init__(self):
        logging.StreamHandler.__init__(self)

    def emit(self, record):
        global buffer
        record = f'{record.name}, [{record.levelname}], {record.message}'
        buffer = f'{buffer}\n{record}'.strip()
        window['log'].update(value=buffer)

log_file = 'run_log.txt'

logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s, %(asctime)s, [%(levelname)s], %(message)s',
    filename=log_file,
    filemode='w')

buffer = ''
ch = Handler()
ch.setLevel(logging.INFO)
logging.getLogger('').addHandler(ch)

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

def downloadMP3(url, dir='undefined', outputName=''):
    try:
        outputPath = setOutput(dir)
        yt = YouTube(url)
        if outputName != '':
            videoTitle = outputName
        else:
            videoTitle = yt.title
        #removing all special characters not allowed when naming windows files
        file_name = removeSpecialChars(videoTitle)

        yt.streams.get_audio_only().download(output_path=outputPath, filename = file_name, max_retries=10)
        print('YouTube audio downloaded successfully. {} : {} | at {}'.format(file_name, url, outputPath))
    
        mp4File = outputPath + '/' + file_name + '.mp4'
        mp3File = outputPath + '/' + file_name + '.mp3'
        os.rename(mp4File, mp3File)
        print('File renamed successfully.')
    except Exception as e:
        os.remove(mp4File)
        print(e)

def downloadVideo(url, dir='undefined', outputName=''):
    outputPath = setOutput(dir)
    try:
        yt = YouTube(url)
        if outputName != '':
            videoTitle = outputName
        else:
            videoTitle = yt.title
        file_name = removeSpecialChars(videoTitle)
        yt.streams.get_highest_resolution().download(output_path=outputPath, filename=file_name, max_retries=10)
        print('YouTube video downloaded successfully. {} : {} | at {}'.format(file_name, url, outputPath))
    except Exception as e:
        print(e)

def downloadPlaylist(url, bType, dir='undefined'):
    outputPath = setOutput(dir)
    pl = Playlist(url)
    folderName = removeSpecialChars(pl.title)
    outputPath += '/{}'.format(folderName) 
    for url in pl.video_urls:
        if bType:
            downloadMP3(url, outputPath)
        else:
            downloadVideo(url, outputPath)

def toggleConsole():
    if window['log'].visible == False:
        window['log'].update(visible=True)
    else:
        window['log'].update(visible=False)

while True:
    event, values = window.read(timeout=10)
    outputPath = values['outputDisplay']
    if event == sg.WIN_CLOSED:
        break
    try:
        videoURL = values['videoURL']
        if event == 'Download MP3':
            downloadMP3(videoURL, outputPath, values['custom_name'])
        elif event == 'Download Video':
            downloadVideo(videoURL, outputPath, values['custom_name'])
        elif event == 'Download Playlist':
            downloadPlaylist(videoURL, values['checkbox_mp3'], outputPath)
        elif event == 'Exit':
            break
        elif event == 'debug':
            toggleConsole()
        elif event == 'Run':
            logging.info('Running')
        elif event == 'Clear URL':
            window['videoURL']('')
        elif event == 'Reset':
            window['outputDisplay']('downloads')        
    except Exception as exc:
        print(exc)      
window.close()
