import select, socket, os, shutil
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import threading, wave, pyaudio, pickle, struct
import subprocess
from subprocess import call
from pytube import YouTube
from pydub import AudioSegment

from Server import Server
from Client import Client

def main():
    # main - 127.0.0.1 secondary - 0.0.0.0
    host_name = socket.gethostname()
    #IP = socket.gethostbyname(host_name)
    #IP = '10.100.102.28'
    IP = '10.100.102.28'
    print(IP)
    port = 1234

    Improvised_Sound_System = ISS(IP,port)

if __name__ == '__main__':
    main()
