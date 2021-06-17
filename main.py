from PySimpleGUI.PySimpleGUI import ProgressBar
from pytube import YouTube, Playlist
import os
import moviepy.editor
import PySimpleGUI as sg
import logging

sg.theme('DarkAmber')
layout = [
    [sg.Text('Output Path: '), sg.InputText(key='outputDisplay', default_text='downloads'), sg.FolderBrowse(key='outputDir', target='outputDisplay')],
    [sg.Text('YouTube video URL: '), sg.InputText()], 
    [sg.Button('Download MP3'),sg.Button('Download Video'),sg.Cancel(button_text='Exit')], 
    [sg.Output(size=(80,10), key='log')]]
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

def downloadMP3(url, dir='undefined'):
    outputPath = setOutput(dir)
    # Using pytube to get lowest resolution video
    yt = YouTube(url)
    yt.streams.get_lowest_resolution().download(output_path=outputPath, filename = yt.title, max_retries=10) #not using .get_audio_only() because moviepy would throw video_fps error when converting
    print('YouTube video audio downloaded successfully')
    filler = '*'*80
    
    mp4File = outputPath + '\\' + yt.title + '.mp4'
    mp3File = outputPath + '\\' + yt.title + '.mp3'

    # Using moviepy to get the mp4 file and convert it to mp3
    videoClip = moviepy.editor.VideoFileClip(mp4File)
    audioclip = videoClip.audio
    audioclip.write_audiofile(mp3File)
    print('\n', filler, '\nVIDEO FILE CONVERTED TO MP3\n', filler)

    # closing and deleting the mp4 file
    audioclip.close()
    videoClip.close()
    os.remove(mp4File)
    print('\n', filler, '\nMP4 FILE DELETED. Your song |', yt.title, '| is ready :)\n', filler)

def downloadVideo(url, dir='undefined'):
    outputPath = setOutput(dir)
    yt = YouTube(videoURL)
    yt.streams.get_highest_resolution().download(output_path=outputPath, filename=yt.title, max_retries=10)
    print('YouTube video downloaded successfully')

while True:
    event, values = window.read(timeout=10)
    if event == sg.WIN_CLOSED:
        break
    try:
        videoURL = values[0]
        if event == 'Download MP3':
            outputPath = values['outputDisplay']
            downloadMP3(videoURL, outputPath)
        elif event == 'Download Video':
            outputPath = values['outputDisplay']
            downloadVideo(videoURL, outputPath)
        elif event == 'Exit':
            break
        elif event == 'Run':
            logging.info('Running...')
            
    except Exception as exc:
        print(exc)      
window.close()
