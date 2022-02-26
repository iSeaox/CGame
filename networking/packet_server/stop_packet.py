import threading
import struct

import networking.packet as packet
from networking.packet_server.packet_server import ServerPacketEnum

class ServerStopPacket(packet.GenericPacket):
    def __init__(self, message="Server shut down"):
        self.__side = 0
        self.__id = ServerPacketEnum.SERVER_STOP_PACKET
        self.__data = 0
        self.__message = message

    def process(self, handler):
        print("[{}] <close> {}".format(threading.current_thread(), self.__message))
        handler.get_handler().clear_run()

    def encode(self):
        return struct.pack("B", (self.__side << 7) + self.__id.value) + str.encode(self.__message)

    def decode(self, raw_data):
        self.__data = raw_data[1:]
        self.__message = self.__data.decode()
        return self

    def get_side(self):
        return self.__side
