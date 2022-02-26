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
        self.__new_postion = None
        if(self.__entity != None):
            self.__new_postion = self.__entity.get_position()
            self.__instance_id = self.__entity.get_instance_id()
        self.__property = None

    def process(self, handler):
        player = handler.get_handler().get_entity_by_instance_id(self.__instance_id)
        player.decode_property(self.__property)
        player.set_position(self.__new_postion)

    def encode(self):
        temp = struct.pack("B", (self.__side << 7) + self.__id.value)
        temp += struct.pack("I", self.__instance_id)
        temp += self.__entity.encode_property()
        temp += struct.pack("dd", self.__new_postion[0], self.__new_postion[1])
        return temp

    def decode(self, raw_data):
        self.__data = raw_data[1:]
        self.__instance_id = struct.unpack("I", raw_data[1:5])[0]
        self.__property = raw_data[5:7]
        self.__new_postion = struct.unpack("dd", raw_data[7:23])
        return self

    def get_side(self):
        return self.__side
