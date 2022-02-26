import time
import threading

import networking.packet_server.stop_packet as stop_packet

def command(handler, raw_command, label, args):
    if(label == "stop"):
        handler.sendAll(stop_packet.ServerStopPacket())

        time.sleep(2)
        handler.set_abort()

    elif(label == "kick"):
        if(len(args) == 1):
            player = handler.get_player_by_name(args[0])
            if(player != None):
                player_access = handler.get_connected_players()[player.get_uuid()][0]
                handler.get_socket().sendto(stop_packet.ServerStopPacket(message="kicked by server").encode(), player_access)
                handler.disconnect_player(player.get_uuid())
            else:
                print("[{}] <error> player not found".format(threading.current_thread().getName()))
        else:
            print("[{}] <error> command usage: kick <user>".format(threading.current_thread().getName()))
