import select, socket, os, shutil
from tkinter import *
import threading, wave, pyaudio, pickle, struct
from pytube import YouTube
from pydub import AudioSegment
#duration, import contextlib

from Server import Server
from threading import Thread

class Client:

    def __init__(self,IP,port):
        self.IP = IP
        self.port = port
        self.count = 0
        self.Client = self.Start_Client()

    def Start_Client(self):
        print("start")
        Thread(target=self.Window).start()
        Thread(target=self.Execute_Client()).start()

    def Window(self):
        window = Tk()
        window.geometry("1000x600")
        window.configure(bg="#ffffff")
        canvas = Canvas(
            window,
            bg="#ffffff",
            height=600,
            width=1000,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        canvas.place(x=0, y=0)

        background_img = PhotoImage(file=f"background_play.png")
        background = canvas.create_image(
            500.0, 300.0,
            image=background_img)

        # with contextlib.closing(wave.open(self.file_path, 'r')) as f:
        #     frames = f.getnframes()
        #     rate = f.getframerate()
        #     duration = frames / float(rate) * 1000
        #     print(duration)

        window.resizable(False, False)
        window.after(10000, lambda: window.destroy())
        window.mainloop()

    def Execute_Client(self):
        # create socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_address = (self.IP, self.port - 1)
        client_socket.connect(socket_address)
        print("CLIENT CONNECTED TO", socket_address)
        data = b""
        payload_size = struct.calcsize("Q")
        print(client_socket)
        frame = None

        length = client_socket.recv(4).decode()
        str_number = client_socket.recv(int(length)).decode()
        PC_number = int(str_number)
        print("pc: ", PC_number)

        length = client_socket.recv(4).decode()
        channels_number = client_socket.recv(int(length)).decode()
        print(channels_number)

        # channels=2,
        p = pyaudio.PyAudio()
        CHUNK = 1024
        # channels=2 before but now 1 because we separated the channels
        stream = p.open(format=p.get_format_from_width(2),
                        channels=int(channels_number),
                        rate=44100,
                        output=True,
                        frames_per_buffer=CHUNK)

        while len(str(frame)) != 3:
            try:
                while len(data) < payload_size:
                    recv = client_socket.recv(4 * 1024)
                    if not recv:
                        break
                    data = data + recv
                packed_message_size = data[:payload_size]
                data = data[payload_size:]
                message_size = struct.unpack("Q", packed_message_size)[0]
                while len(data) < message_size:
                    data = data + client_socket.recv(4 * 1024)
                frame_data = data[:message_size]
                data = data[message_size:]
                frame = pickle.loads(frame_data)
                stream.write(frame)
                self.count = self.count + 1
            except:
                 break

        client_socket.close()
        print('Audio closed')
        os._exit(1)

