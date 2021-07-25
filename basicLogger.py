import logging

class Handler(logging.StreamHandler):

    def __init__(self):
        logging.StreamHandler.__init__(self)

    def emit(self, record):
        global buffer
        record = f'{record.name}, [{record.levelname}], {record.message}'
        buffer = f'{buffer}\n{record}'.strip()
        window['log'].update(value=buffer)

logFile = 'runLog.txt'

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s], %(name)s, %(asctime)s, %(message)s',
    filename=logFile,
    filemode='w')

buffer = ''
ch = Handler()
ch.setLevel(logging.INFO)
logging.getLogger('').addHandler(ch)

