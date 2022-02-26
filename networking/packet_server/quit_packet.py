import struct
import uuid
import threading

import networking.packet as packet
from networking.packet_server.packet_server import ServerPacketEnum

class ServerPlayerQuitPacket(packet.GenericPacket):
    def __init__(self, uuid=None):
        self.__side = 0
        self.__id = ServerPacketEnum.SERVER_PLAYER_QUIT_PACKET
        self.__data = 0
        self.__uuid = uuid

    def process(self, handler):
        player = None
        for p in handler.get_handler().get_connected_players():
            if(p.get_uuid() == self.__uuid):
                player = p
        handler.get_handler().get_connected_players().remove(player)
        print("[{}] <run> {} left the game".format(threading.current_thread().getName(), player.get_name()))

    def encode(self):
        temp = struct.pack("B", (self.__side << 7) + self.__id.value)
        temp += self.__uuid.bytes
        return temp

    def decode(self, raw_data):
        self.__data = raw_data[1:]
        self.__uuid = uuid.UUID(bytes=raw_data[1:])

        return self

    def get_side(self):
        return self.__side
