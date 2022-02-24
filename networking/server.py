import socket
import threading

import networking.net_exception as net_exception
import networking.packet_handler as packet_handler

import game.content.map.map as map

SERVER_SIDE = 0
CLIENT_SIDE = 1

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
        self.__players = {}
        self.__socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.__socket.bind((self.__address_ip, self.__port))
        self.__net_listener = threading.Thread(name="sernet-listener", target=net_listener, args=(self,), daemon=True)
        self.__net_listening = False;
        self.__buffer_size = 1024
        self.__map = map.Map((0x23, 0xb8, 0x66), 225)

    def start(self):
        if(self.__side == CLIENT_SIDE): raise net_exception.WrongSideException("Denied access: Client side can't use this method")
        self.__net_listening = True;

        self.__net_listener.start()

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
        for player in self.__players.values():
            if(player.get_uuid() == uuid):
                return player
        return None
