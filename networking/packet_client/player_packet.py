import struct
import uuid

import networking.packet as packet
import networking.packet_server.update_packet as update_packet
from networking.packet_client.packet_client import ClientPacketEnum

class ClientPlayerMovePacket(packet.GenericPacket):

    def __init__(self, player=None):
        self.__side = 1
        self.__id = ClientPacketEnum.CLIENT_PLAYER_MOVE_PACKET
        self.__data = 0
        self.__player = player
        self.__uuid = None
        self.__property = None
        if(self.__player != None):
            self.__uuid = self.__player.get_uuid()
        self.__new_postion = None

    def process(self, handler):
        self.__player = handler.get_handler().get_player_by_uuid(self.__uuid)
        self.__player.decode_property(self.__property)
        self.__player.set_position(self.__new_postion)
        handler.get_handler().sendAll(update_packet.ServerEntityUpdatePacket(entity = self.__player))

    def encode(self):
        temp = struct.pack("B", (self.__side << 7) + self.__id.value)
        temp += self.__player.get_uuid().bytes
        temp += self.__player.encode_property()
        temp += struct.pack("dd", self.__player.get_position()[0], self.__player.get_position()[1])
        return temp

    def decode(self, raw_data):
        self.__data = raw_data[1:]
        self.__uuid = uuid.UUID(bytes=raw_data[1:17])
        self.__property = raw_data[17:19]
        self.__new_postion = struct.unpack("dd", raw_data[19:35])
        return self

    def get_side(self):
        return self.__side
