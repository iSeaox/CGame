import struct

import packet
from packet_server.packet_server import ServerPacketEnum

import game.content.map.map as map

class ServerInitTransferPacket(packet.GenericPacket):

    def __init__(self, connection_code=None, entities=None, server_map=None):
        self.__side = 0
        self.__id = ServerPacketEnum.SERVER_INIT_TRANSFER_PACKET
        self.__data = 0

        self.__connection_code = connection_code
        self.__map = server_map

    def process(self, handler):
        handler.get_handler().set_ready(True)

    def encode(self) -> bytes:
        return struct.pack("BB", (self.__side << 7) + self.__id.value, self.__connection_code) + self.__map.encode()

    def decode(self, raw_data):
        self.__data = raw_data[1:]
        self.__connection_code = raw_data[1]
        self.__map = map.Map().decode(raw_data[2:8])
        return self

    def get_side(self):
        return self.__side
