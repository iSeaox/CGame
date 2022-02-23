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
        self.__new_position = ()
        self.__uuid = None
        if(self.__player != None):
            self.__uuid = self.__player.get_uuid()
            self.__new_position = self.__player.get_position()

    def process(self, handler):
        self.__player = handler.get_handler().get_player_by_uuid(self.__uuid)
        self.__player.set_position(self.__new_position)
        print(self.__player.get_position())
        handler.get_handler().get_socket().sendto(update_packet.ServerEntityUpdatePacket(entity = self.__player, type=0).encode(), self.get_sender())

    def encode(self):
        temp = struct.pack("B", (self.__side << 7) + self.__id.value)
        temp += self.__player.get_uuid().bytes
        temp += struct.pack("dd", self.__player.get_position()[0], self.__player.get_position()[1])
        return temp

    def decode(self, raw_data):
        self.__data = raw_data[1:]
        self.__uuid = uuid.UUID(bytes=raw_data[1:17])
        self.__new_position = struct.unpack("dd", raw_data[17:33])
        return self

    def get_side(self):
        return self.__side
