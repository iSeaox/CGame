from enum import Enum

import struct
import networking.packet as packet
from networking.packet_server.packet_server import ServerPacketEnum

MOVE_PACKET = 0

class ServerEntityUpdatePacket(packet.GenericPacket):
    def __init__(self, entity=None):
        self.__side = 0
        self.__id = ServerPacketEnum.SERVER_ENTITY_UPDATE_PACKET
        self.__data = 0
        self.__type = type
        self.__entity = entity
        self.__instance_id = None
        if(self.__entity != None):
            self.__instance_id = self.__entity.get_instance_id()
        self.__property = None

    def process(self, handler):
        handler.get_handler().get_player().decode_property(self.__property)

    def encode(self):
        temp = struct.pack("B", (self.__side << 7) + self.__id.value)
        temp += struct.pack("I",self.__instance_id)
        temp += self.__entity.encode_property()
        return temp

    def decode(self, raw_data):
        self.__data = raw_data[1:]
        self.__instance_id = raw_data[1:5]
        self.__property = raw_data[5:7]
        return self

    def get_side(self):
        return self.__side
