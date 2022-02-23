import socket
import threading
import os
import uuid

import networking.net_exception as net_exception
import networking.packet_handler as packet_handler
import networking.packet_client.connection_packet as connection_packet
import networking.packet_client.player_packet as player_packet

import game.content.map.map as map

import pygame

SERVER_SIDE = 0
CLIENT_SIDE = 1

DATAFILE_PATH = r"./local/client/player_info.data"

def net_listener(client):
    print("[{}] Listening...".format(threading.current_thread()))
    while(client.net_listening()):
        try:
            received_packet = client.get_socket().recvfrom(client.get_buffer_size())
            packet_handler.register_packet_handler(client, received_packet)
        except(Exception):
            pass
class Client:

    def __init__(self, server_access, side):
        self.__side = side
        self.__server_access = server_access
        self.__socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.__net_listener = threading.Thread(name="clinet-listener", target=net_listener, args=(self,), daemon=True)
        self.__net_listening = False;
        self.__buffer_size = 1024
        self.__map = None
        self.__ready = False
        self.__run = True
        print("[{}]".format(threading.currentThread()), "<init> searching for data")
        if(os.path.exists(DATAFILE_PATH)):
            with open(DATAFILE_PATH, "rb") as file:
                self.__client_uuid = file.read()
                if(self.__client_uuid != b''):
                    self.__client_uuid = uuid.UUID(bytes=self.__client_uuid)
                    print("[{}]".format(threading.currentThread()), "<init>", "data found: uuid -> {}".format(self.__client_uuid))
                else:
                    self.__client_uuid = None
        else:
            self.__client_uuid = None

        self.__player_entity = None


    def start(self, name):
        if(self.__side == SERVER_SIDE): raise net_exception.WrongSideException("Denied access: Server side can't use this method")
        self.__net_listening = True;
        self.__net_listener.start()
        if(self.__client_uuid == None):
            self.__socket.sendto(connection_packet.ClientInitPacket(user=name, code=0x80).encode(), self.__server_access)
        else:
            self.__socket.sendto(connection_packet.ClientInitPacket(user=name, code=0x0, guuid=self.__client_uuid).encode(), self.__server_access)

    def render(self, screen):
        screen.fill(self.__map.get_background())
        floor = pygame.Surface((1280, self.__map.get_floor_height()))
        floor.fill((0, 0, 0))
        floor.set_alpha(50)
        screen.blit(floor, (0, 720 - floor.get_height()))

        self.__player_entity.get_displayer().render(screen)

    def game_loop(self):
        while(not(self.__ready)): pass

        pygame.init()
        clock = pygame.time.Clock()
        #d_info = pygame.display.Info()
        #screen = pygame.display.set_mode((d_info.current_w, d_info.current_h))
        screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("CGame")

        while(self.__run):
            #print(clock.get_fps())
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__run = False
                    break
                elif(event.type == pygame.KEYDOWN):
                    pos = self.__player_entity.get_position()
                    new_pos = (pos[0] + 1, pos[1])
                    self.__player_entity.set_position(new_pos)
                    self.__socket.sendto(player_packet.ClientPlayerMovePacket(player=self.__player_entity).encode(), self.__server_access)

            self.render(screen)

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

    def store_player_info(self):
        if(not(os.path.exists(DATAFILE_PATH))):
            open(DATAFILE_PATH, "x").close()

        with open(DATAFILE_PATH, "rb+") as file:
            file.write(self.__client_uuid.bytes)

    def get_net_listener(self):
        return self.__net_listener

    def get_buffer_size(self):
        return self.__buffer_size

    def get_socket(self):
        return self.__socket

    def net_listening(self):
        return self.__net_listening

    def set_map(self, new_map):
        self.__map = new_map

    def get_map(self):
        return self.__map

    def set_net_listening(self, nl):
        self.__net_listening = nl

    def set_ready(self, value):
        self.__ready = value

    def set_run(self, value):
        self.__run = value

    def set_uuid(self, player_uuid):
        self.__client_uuid = player_uuid

    def get_uuid(self):
        return self.__client_uuid

    def set_player_entity(self, entity):
        self.__player_entity = entity

    def get_player(self):
        return self.__player_entity
