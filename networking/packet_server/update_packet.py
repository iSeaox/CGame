from enum import Enum

import struct
import networking.packet as packet
from networking.packet_server.packet_server import ServerPacketEnum

MOVE_PACKET = 0

class ServerEntityUpdatePacket(packet.GenericPacket):
    def __init__(self, type=None, entity=None):
        self.__side = 0
        self.__id = ServerPacketEnum.SERVER_ENTITY_UPDATE_PACKET
        self.__data = 0
        self.__type = type
        self.__entity = entity
        self.__instance_id = None
        if(self.__entity != None):
            self.__instance_id = self.__entity.get_instance_id()

        self.__args = None

    def process(self, handler):
        if(self.__type == MOVE_PACKET):
            self.__entity = handler.get_handler().get_player()
            print(self.__entity.get_position())
            self.__entity.set_position(self.__args)

    def encode(self):
        temp = struct.pack("B", (self.__side << 7) + self.__id.value)
        temp += struct.pack("I B",self.__instance_id, self.__type)

        if(self.__type == MOVE_PACKET):
            temp += struct.pack("dd", self.__entity.get_position()[0], self.__entity.get_position()[1])

        return temp

    def decode(self, raw_data):
        self.__data = raw_data[1:]
        self.__instance_id = struct.unpack("I", raw_data[1:5])
        self.__type = raw_data[5]

        if(self.__type == MOVE_PACKET):
            self.__args = struct.unpack("dd", raw_data[6:22])

        return self

    def get_side(self):
        return self.__side
