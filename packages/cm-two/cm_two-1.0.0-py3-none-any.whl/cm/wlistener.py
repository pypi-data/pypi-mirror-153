import socket
from time import sleep
import logging
from traceback import format_exc
from cm.configs import config as s
import pickle
import threading


class WListener:
    '''Прослушиватель ком портов, к которым линкуются периферийные
    железки, при создании экземпляра необходимо задать имя железки,
    номер ком-порта, порт'''

    def __init__(self, name='def', comnum='25', port='1488', bs=8, py='N',
                 sb=1, to=1, ip='localhost', ar_ip='localhost'):
        self.name = name
        self.ip = ip
        self.comnum = comnum
        self.port = port
        self.bs = bs
        self.ar_ip = ar_ip
        self.sb = sb
        self.to = to
        self.py = py
        self.smlist = ['0']
        self.status = 'Готов'
        self.addInfo = {'carnum': 'none', 'status': 'none', 'notes': 'none'}
        self.cmInterfaceComms = []
        self.activity = True

    def wlisten_tcp(self):
        try:
            return self.smlist[-1]
        except:
            logging.error(format_exc())

    def scale_reciever(self, scale_ip):
        client = socket.socket()
        while True:
            try:
                self.connect_cps(client, scale_ip)
                self.interact_cps(client)
            except:
                print(format_exc())
                sleep(3)

    def connect_cps(self, client, scale_ip):
        while True:
            try:
                client.connect((scale_ip, s.scale_splitter_port))
                break
            except:
                print('Не удалось подключиться к сереру рассылки '
                      'данных с весового терминала. Повтор ... ')
                sleep(3)

    def interact_cps(self, client):
        while True:
            data = client.recv(1024)
            if not data: break
            data = data.decode(encoding='utf-8')
            self.smlist.append(data)
