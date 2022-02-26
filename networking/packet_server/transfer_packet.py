import struct
import uuid
import threading

import networking.packet as packet
from networking.packet_server.packet_server import ServerPacketEnum

import game.content.map.map as map
import game.entity.player as player

class ServerInitTransferPacket(packet.GenericPacket):

    def __init__(self, connection_code=None, entities=None, server_map=None, client_uuid=None, message=None):
        self.__side = 0
        self.__id = ServerPacketEnum.SERVER_INIT_TRANSFER_PACKET
        self.__data = 0
        self.__message = message

        self.__connection_code = connection_code
        self.__map = server_map
        self.__client_uuid = client_uuid

    def process(self, handler):
        if(not(0x80 & self.__connection_code)):
            if(0x40 & self.__connection_code):
                handler.get_handler().set_abort_launch()
                print("[{}] <error> ERROR while connection: {}".format(threading.current_thread(), self.__message))

        else:
            handler.get_handler().set_map(self.__map)
            if(0x20 & self.__connection_code):
                handler.get_handler().new_profile(self.__client_uuid)

            handler.get_handler().set_ready(True)


    def encode(self) -> bytes:
        if(self.__message != None and 0x40 & self.__connection_code and len(self.__message) < 256):
            msg_size = len(self.__message)
        else:
            msg_size = 0
        temp = struct.pack("BB B", (self.__side << 7) + self.__id.value, self.__connection_code, msg_size)
        if(0x20 & self.__connection_code):
            if(self.__client_uuid != None):
                temp += self.__client_uuid

        if(0x40 & self.__connection_code):
            temp += str.encode(self.__message)

        if(0x80 & self.__connection_code):
            temp += self.__map.encode()
        return temp

    def decode(self, raw_data):
        self.__data = raw_data[1:]
        self.__connection_code = raw_data[1]
        msg_size = raw_data[2]

        # piste d'amélioration : le faire avec des offsets du types si y'a uuid j'ajoute 16 à tout sinon j'ajoute 0 un peu comme pour msg_size
        if(0x20 & self.__connection_code):
            self.__client_uuid = uuid.UUID(bytes=raw_data[3:19])
            if(0x40 & self.__connection_code):
                self.__message = raw_data[19:(19 + msg_size)].decode()
            if(0x80 & self.__connection_code):
                self.__map = map.Map().decode(raw_data[(19 + msg_size):(25 + msg_size)])
        else:
            if(0x40 & self.__connection_code):
                self.__message = raw_data[3:(3 + msg_size)].decode()
            if(0x80 & self.__connection_code):
                self.__map = map.Map().decode(raw_data[(3 + msg_size):(9 + msg_size)])
        return self

    def get_side(self):
        return self.__side

PETP_CODE_S = 0x80 # envoie uniquement l'object joueur destiner au client
PETP_CODE_SC = 0xC0 # comme S mais avec les joueurs connectés en plus
PETP_CODE_C = 0x40 # seulement la liste des joueurs connectés
PETP_CODE_NP = 0x20 # uniquement pour envoyer l'object joueurs d'un joueur venant de se connceter

class ServerPlayerEntityTransferPacket(packet.GenericPacket):
    def __init__(self, code=None, player_entity=None, players=[]):
        self.__side = 0
        self.__id = ServerPacketEnum.SERVER_PLAYER_ENTITY_TRANSFER_PACKET
        self.__data = 0
        self.__player_entity = player_entity
        self.__connected_players = players
        self.__code = code

    def process(self, handler):
        if(self.__code == PETP_CODE_SC):
            handler.get_handler().set_player_entity(self.__player_entity)
            to_update = handler.get_handler().get_connected_players()
            for p in self.__connected_players:
                if(not(p in to_update) and p.get_uuid() != self.__player_entity.get_uuid()):
                    to_update.append(p)
        elif(self.__code == PETP_CODE_NP):
            handler.get_handler().get_connected_players().append(self.__player_entity)
            print("[{}] <run> {} join the game".format(threading.current_thread().getName(), self.__player_entity))

    def encode(self):
        temp = struct.pack("B B", (self.__side << 7) + self.__id.value, self.__code)
        if(self.__code == PETP_CODE_S or self.__code == PETP_CODE_NP):
            temp += self.__player_entity.encode()

        elif(self.__code == PETP_CODE_SC):
            temp += self.__player_entity.encode()
            for player in self.__connected_players:
                temp += player.encode()

        elif(self.__code == PETP_CODE_C):
            for player in self.__connected_players:
                temp += player.encode()

        return temp

    def decode(self, raw_data):
        self.__data = raw_data[1:]
        self.__code = raw_data[1]
        c_offset = 2
        if(0x80 & self.__code or 0x20 & self.__code):
            c_offset = 66
            self.__player_entity = player.Player().decode(raw_data[2:66])
        if(0x40 & self.__code):
            index = 0
            while(index < len(raw_data[c_offset:])):
                self.__connected_players.append(player.Player().decode(raw_data[(c_offset + index):(c_offset + index + 64)]))
                index += 64
        return self

    def get_side(self):
        return self.__side

    def get_player_entity(self):
        return self.__player_entity
