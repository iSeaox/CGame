import threading
import server
import client
import packet

from packet_client.packet_client import ClientPacketEnum
import packet_client.connection_packet as connection_packet

from packet_server.packet_server import ServerPacketEnum
import packet_server.transfer_packet as transfer_packet
#cd ./Desktop/DEV-python/pygame/networking/


def get_packet_object(raw_data):
    if(0x80 & raw_data[0]):
        # client side
        packet_id = ~0x80 & raw_data[0]
        if(packet_id == ClientPacketEnum.CLIENT_INIT_PACKET.value):
            return connection_packet.ClientInitPacket().decode(raw_data)
    else:
        # server side
        packet_id = ~0x80 & raw_data[0]
        if(packet_id == ServerPacketEnum.SERVER_INIT_TRANSFER_PACKET.value):
            return transfer_packet.ServerInitTransferPacket().decode(raw_data)

n_clpacket_handler = 0
n_srpacket_handler = 0
def register_packet_handler(csentity, packet):
    global n_clpacket_handler
    global n_srpacket_handler
    if(type(csentity) == server.Server):
        ServerPacketHandler(csentity, packet).start()
        n_srpacket_handler += 1
    elif(type(csentity) == client.Client):
        ClientPacketHandler(csentity, packet).start()
        n_clpacket_handler += 1

class ClientPacketHandler(threading.Thread):
    def __init__(self, client, packet):
        global n_clpacket_handler
        threading.Thread.__init__(self, name="clpacket-handler-{}".format(str(n_clpacket_handler)))
        self.__client = client
        self.__packet = packet

    def run(self):
        packet_object = get_packet_object(self.__packet[0])
        packet_object.set_sender(self.__packet[1])
        if(packet_object.get_side() == 0):
            packet_object.process(self)

        print("[{}]".format(threading.current_thread()), "<{}>".format(packet_object.get_sender()), "-> {}".format(packet_object.__class__.__name__))

    def get_handler(self):
        return self.__client

class ServerPacketHandler(threading.Thread):
    def __init__(self, server, packet):
        global n_srpacket_handler
        threading.Thread.__init__(self, name="srpacket-handler-{}".format(str(n_srpacket_handler)))
        self.__server = server
        self.__packet = packet

    def run(self):
        packet_object = get_packet_object(self.__packet[0])
        packet_object.set_sender(self.__packet[1])

        if(packet_object.get_side() == 1):
            packet_object.process(self)
        print("[{}]".format(threading.current_thread()), "<{}>".format(packet_object.get_sender()), "-> {}".format(packet_object.__class__.__name__))
    def get_handler(self):
        return self.__server
