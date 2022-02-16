import struct

import networking.packet as packet
from networking.packet_client.packet_client import ClientPacketEnum

import packet_server.transfer_packet as transfer_packet

class ClientInitPacket(packet.GenericPacket):

    def __init__(self):
        self.__side = 1
        self.__id = ClientPacketEnum.CLIENT_INIT_PACKET
        self.__data = 0

    def process(self, handler):
        c_code = 0x80
        ITPacket = transfer_packet.ServerInitTransferPacket(connection_code=c_code, server_map=handler.get_handler().get_map())
        handler.get_handler().get_socket().sendto(ITPacket.encode(), self.get_sender())
        print("send")

    def encode(self) -> bytes:
        return struct.pack("BB", (self.__side << 7) + self.__id.value, 0)

    def decode(self, raw_data):
        self.__data = raw_data[1:]
        return self

    def get_side(self):
        return self.__side
