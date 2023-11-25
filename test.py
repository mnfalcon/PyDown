from urllib.request import urlopen
import urllib.response
from io import BytesIO
from zipfile import ZipFile
import json
import os
import PySimpleGUI as sg
import logging
import threading
import basicLogger
from time import gmtime, strftime

release = json.loads(urlopen("https://api.github.com/repos/mnfalcon/PyDown/releases/latest").read().decode("utf-8"))
version = open('version.txt', 'a+')
print(version == release["tag_name"])
print(float(release["tag_name"].strip("v")) < 0)
url = release["assets"][0]["browser_download_url"]