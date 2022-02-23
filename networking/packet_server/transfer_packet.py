import struct
import uuid

import networking.packet as packet
from networking.packet_server.packet_server import ServerPacketEnum

import game.content.map.map as map
import game.entity.player as player

class ServerInitTransferPacket(packet.GenericPacket):

    def __init__(self, connection_code=None, entities=None, server_map=None, client_uuid=None):
        self.__side = 0
        self.__id = ServerPacketEnum.SERVER_INIT_TRANSFER_PACKET
        self.__data = 0

        self.__connection_code = connection_code
        self.__map = server_map
        self.__client_uuid = client_uuid

    def process(self, handler):
        if(0x20 & self.__connection_code):
            handler.get_handler().set_uuid(self.__client_uuid)
            handler.get_handler().store_player_info()
        handler.get_handler().set_map(self.__map)
        handler.get_handler().set_ready(True)

    def encode(self) -> bytes:
        temp = struct.pack("BB", (self.__side << 7) + self.__id.value, self.__connection_code)
        if(0x20 & self.__connection_code):
            if(self.__client_uuid != None):
                temp += self.__client_uuid
        temp += self.__map.encode()
        return temp

    def decode(self, raw_data):
        self.__data = raw_data[1:]
        self.__connection_code = raw_data[1]
        if(0x20 & self.__connection_code):
            self.__client_uuid = uuid.UUID(bytes=raw_data[2:18])
            self.__map = map.Map().decode(raw_data[18:24])
        else:
            self.__map = map.Map().decode(raw_data[2:8])
        return self

    def get_side(self):
        return self.__side

class ServerPlayerEntityTransferPacket(packet.GenericPacket):
    def __init__(self, player_entity=None):
        self.__side = 0
        self.__id = ServerPacketEnum.SERVER_PLAYER_ENTITY_TRANSFER_PACKET
        self.__data = 0
        self.__player_entity = player_entity

    def process(self, handler):
        handler.get_handler().set_player_entity(self.__player_entity)

    def encode(self):
        temp = struct.pack("B", (self.__side << 7) + self.__id.value)
        temp += self.__player_entity.encode()
        return temp

    def decode(self, raw_data):
        self.__data = raw_data[1:]
        self.__player_entity = player.Player().decode(raw_data[1:])
        return self

    def get_side(self):
        return self.__side

    def get_player_entity(self):
        return self.__player_entity
