import struct
import uuid
import threading

import networking.packet as packet
import networking.packet_server.transfer_packet as transfer_packet
import networking.packet_server.quit_packet as quit_packet
from networking.packet_client.packet_client import ClientPacketEnum

from game.entity.player import Player

class ClientQuitPacket(packet.GenericPacket):
    def __init__(self, uuid=None):
        self.__side = 1
        self.__id = ClientPacketEnum.CLIENT_QUIT_PACKET
        self.__data = 0
        self.__uuid = uuid

    def process(self, handler):
        handler.get_handler().disconnect_player(self.__uuid)
        handler.get_handler().sendAll(quit_packet.ServerPlayerQuitPacket(uuid=self.__uuid))

    def encode(self):
        return struct.pack("B", (self.__side << 7) + self.__id.value) + self.__uuid.bytes

    def decode(self, raw_data):
        self.__data = raw_data[1:]
        self.__uuid = uuid.UUID(bytes=self.__data)
        return self

    def get_side(self):
        return self.__side

class ClientInitPacket(packet.GenericPacket):

    def __init__(self, user=None, code=None, guuid=None):
        self.__side = 1
        self.__id = ClientPacketEnum.CLIENT_INIT_PACKET
        self.__data = 0
        self.__user = user
        self.__uuid = guuid
        self.__code = code

    def process(self, handler):

        temp = Player(name=self.__user, player_uuid=self.__uuid, server=True)

        if(0x80 & self.__code):
            if(not(handler.get_handler().is_registered_by_name(self.__user))):
                c_code = 0xA0
                new_uuid = uuid.uuid4()
                temp.set_uuid(new_uuid)
                handler.get_handler().register_player(temp.get_name(), temp.get_uuid())

                ITPacket = transfer_packet.ServerInitTransferPacket(connection_code=c_code, server_map=handler.get_handler().get_map(), client_uuid=new_uuid.bytes)
                print("[{}]".format(threading.currentThread()), "<run>", "NEW: {} join the game ({})".format(self.__user, new_uuid))
            else:
                c_code = 0x40
                ITPacket = transfer_packet.ServerInitTransferPacket(connection_code=c_code, message="already registered")
                handler.get_handler().get_socket().sendto(ITPacket.encode(), self.get_sender())
                return
        else:
            if(not(temp.get_uuid() in handler.get_handler().get_connected_players())):
                c_code = 0x80
                ITPacket = transfer_packet.ServerInitTransferPacket(connection_code=c_code, server_map=handler.get_handler().get_map())
                print("[{}]".format(threading.currentThread()), "<run>", "{} join the game ({})".format(self.__user, self.__uuid))
            else:
                c_code = 0x40
                ITPacket = transfer_packet.ServerInitTransferPacket(connection_code=c_code, message="already connected")
                handler.get_handler().get_socket().sendto(ITPacket.encode(), self.get_sender())
                return

        temp.set_position((300.0, 200.0))
        handler.get_handler().sendAll(transfer_packet.ServerPlayerEntityTransferPacket(code=transfer_packet.PETP_CODE_NP, player_entity=temp))

        handler.get_handler().get_connected_players()[temp.get_uuid()] = (self.get_sender(), temp)

        tempCP = handler.get_handler().get_connected_players()
        cp_list = []
        for value in tempCP.values():
            cp_list.append(value[1])

        PETPacket = transfer_packet.ServerPlayerEntityTransferPacket(player_entity=temp, players=cp_list, code=transfer_packet.PETP_CODE_SC)

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
