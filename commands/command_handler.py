import time

import networking.packet_server.stop_packet as stop_packet

def command(handler, raw_command, label, args):
    if(label == "stop"):
        handler.sendAll(stop_packet.ServerStopPacket())

        time.sleep(2)
        handler.set_abort()
