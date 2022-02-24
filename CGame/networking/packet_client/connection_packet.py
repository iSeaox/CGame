import struct
import uuid
import threading

import networking.packet as packet
import networking.packet_server.transfer_packet as transfer_packet
from networking.packet_client.packet_client import ClientPacketEnum
from game.entity.player import Player


class ClientInitPacket(packet.GenericPacket):

    def __init__(self, user=None, code=None, guuid=None):
        self.__side = 1
        self.__id = ClientPacketEnum.CLIENT_INIT_PACKET
        self.__data = 0
        self.__user = user
        self.__uuid = guuid
        self.__code = code

    def process(self, handler):

        temp = Player(name=self.__user, player_uuid=self.__uuid)

        if(0x80 & self.__code):
            c_code = 0xA0
            new_uuid = uuid.uuid4()
            temp.set_uuid(new_uuid)
            ITPacket = transfer_packet.ServerInitTransferPacket(connection_code=c_code, server_map=handler.get_handler().get_map(), client_uuid=new_uuid.bytes)
            print("[{}]".format(threading.currentThread()), "<connection>", "NEW: {} ; uuid -> {}".format(self.__user, new_uuid))
        else:
            c_code = 0x80
            ITPacket = transfer_packet.ServerInitTransferPacket(connection_code=c_code, server_map=handler.get_handler().get_map())
            print("[{}]".format(threading.currentThread()), "<connection>", "{} ; uuid -> {}".format(self.__user, self.__uuid))

        temp.set_position((300.0, 200.0))
        handler.get_handler().get_player_infos()[self.get_sender()] = temp
        print(handler.get_handler().get_player_infos())

        PETPacket = transfer_packet.ServerPlayerEntityTransferPacket(player_entity=temp)

        handler.get_handler().get_socket().sendto(PETPacket.encode(), self.get_sender())
        handler.get_handler().get_socket().sendto(ITPacket.encode(), self.get_sender())


    def encode(self) -> bytes:
        user_bytes = str.encode(self.__user)
        while len(user_bytes) < 20:
            user_bytes += struct.pack("B", 0)
        temp = struct.pack("B B", (self.__side << 7) + self.__id.value, self.__code) + user_bytes
        if(not(0x80 & self.__code)):
            if(self.__uuid == None): raise AttributeError("guuid can't be None with this code")
            temp += self.__uuid.bytes
        return temp

    def decode(self, raw_data):
        self.__data = raw_data[1:]
        self.__code = raw_data[1]

        t_array = []
        for b in raw_data[2:22]:
            if(b == 0):
                break
            t_array.append(b)
        self.__user = bytearray(t_array).decode()

        if(not(0x80 & self.__code)):
            self.__uuid = uuid.UUID(bytes=raw_data[22:38])

        return self

    def get_side(self):
        return self.__side
