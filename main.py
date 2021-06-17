from pytube import YouTube
import os
#from moviepy.editor import *
import moviepy.editor
import PySimpleGUI as sg
import logging

sg.theme('DarkAmber')
layout = [[sg.Text('Insertar URL en el campo'), sg.InputText()], [sg.Button('Download'), sg.Cancel()], [sg.Output(size=(80,10), key='log')]]
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

def download(url):
    # Using pytube to get lowest resolution video
    yt = YouTube(videoURL)
    yt.streams.get_lowest_resolution().download(filename = yt.title, max_retries=10) #not using .get_audio_only() because moviepy would throw video_fps error
    print('YouTube video audio downloaded successfully')

    mp4File = yt.title + '.mp4'
    mp3File = yt.title + '.mp3'

    # Using moviepy to get the mp4 file and convert it to mp3
    videoClip = moviepy.editor.VideoFileClip(mp4File)
    audioclip = videoClip.audio
    audioclip.write_audiofile(mp3File)
    print('\n********************\nVIDEO FILE CONVERTED TO MP3\n********************')

    # closing and deleting the mp4 file
    audioclip.close()
    videoClip.close()
    os.remove(mp4File)
    print('\n********************\nMP4 FILE DELETED\n********************')

while True:
    event, values = window.read(timeout=10)
    if event == sg.WIN_CLOSED:
        break
    try:
        videoURL = values[0]
        if event == 'Download':
            download(videoURL)
        elif event == 'Cancel':
            break
        elif event == 'Run':
            logging.info('Running...')
    except Exception as exc:
        print(exc)      
window.close()
