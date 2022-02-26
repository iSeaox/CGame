import socket
import threading
import os
import uuid

import networking.net_exception as net_exception
import networking.packet_handler as packet_handler

import game.content.map.map as map

import commands.command_handler as command_handler

SERVER_SIDE = 0
CLIENT_SIDE = 1

PLAYER_PROFILE_FILE = r'./local/server/players/registered.data'
PLAYER_DATA_FOLDER = r'./local/server/players/data/'

def net_listener(server):
    print("[{}] Listening...".format(threading.current_thread()))
    while(server.net_listening):
        received_packet = server.get_socket().recvfrom(server.get_buffer_size())
        packet_handler.register_packet_handler(server, received_packet)

class Server:
    def __init__(self, addr, port, side):
        self.__side = side
        self.__address_ip = addr
        self.__port = port
        self.__abort = False
        self.__players = {}
        self.__socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.__socket.bind((self.__address_ip, self.__port))
        self.__net_listener = threading.Thread(name="sernet-listener", target=net_listener, args=(self,), daemon=True)
        self.__net_listening = False;
        self.__buffer_size = 1024
        self.__map = map.Map((0x23, 0xb8, 0x66), 225)

        self.__registered_players = {}
        self.__connected_players = {}

    def start(self):
        if(self.__side == CLIENT_SIDE): raise net_exception.WrongSideException("Denied access: Client side can't use this method")
        print("[{}] <init> loading resources...".format(threading.current_thread().getName()))
        print("[{}] <init> -> registered players".format(threading.current_thread().getName()))
        self.__load_registered_player()
        print("[{}] <init>    {} player found".format(threading.current_thread().getName(), len(self.__registered_players)))


        self.__net_listening = True;
        self.__net_listener.start()

        while(not(self.__abort)):
            raw_command = input()
            splited = raw_command.split(" ")
            command_handler.command(self, raw_command, splited[0], splited[1:])

        self.__socket.close()


    def register_player(self, user, uuid):
        if(not(uuid in self.__registered_players)):
            if(not(os.path.exists(PLAYER_PROFILE_FILE))): open(PLAYER_PROFILE_FILE, "x")
            with open(PLAYER_PROFILE_FILE, "rb+") as file:
                content = file.read()
                if(len(content)):
                    file.write(str.encode("&{}:{}".format(user, uuid)))
                else:
                    file.write(str.encode("{}:{}".format(user, uuid)))

            profile_path = PLAYER_DATA_FOLDER + str(uuid) + ".profile"
            if(not(os.path.exists(profile_path))): open(profile_path, "x")

            self.__registered_players[user] = uuid
            print("[{}] <load> {} has been registered".format(threading.current_thread().getName(), user))

    def __load_registered_player(self):
        if(os.path.exists(PLAYER_PROFILE_FILE)):
            with open(PLAYER_PROFILE_FILE, "rb") as file:
                raw = file.read().decode()
                players = raw.split("&")
                for player in players:
                    temp = player.split(":")
                    self.__registered_players[temp[0]] = uuid.UUID(temp[1])

    def disconnect_player(self, uuid):
        popped = self.__connected_players.pop(uuid)
        print("[{}] <run> {} left the game".format(threading.current_thread(), popped[1].get_name()))

    def sendAll(self, packet):
        for value in self.__connected_players.values():
            self.__socket.sendto(packet.encode(), value[0])

    def get_map(self):
        return self.__map

    def get_socket(self):
        return self.__socket

    def get_buffer_size(self):
        return self.__buffer_size

    def net_listening(self):
        return self.__net_listening

    def get_player_infos(self):
        return self.__players

    def get_player_by_uuid(self, uuid):
        return self.__connected_players[uuid][1]

    def get_player_by_name(self, name):
        for value in self.__connected_players.values():
            if(value[1].get_name() == name):
                return value[1]
        return None

    def get_connected_players(self):
        return self.__connected_players

    def get_registered_players(self):
        return self.__registered_players

    def is_registered_by_name(self, name):
        return (name in self.__registered_players)

    def set_abort(self):
        self.__abort = True
