import socket
import threading
import os
import uuid

import networking.net_exception as net_exception
import networking.packet_handler as packet_handler

import networking.packet_client.connection_packet as connection_packet
import networking.packet_client.player_packet as player_packet

import game.content.map.map as map
import game.entity.entity as entity

import launcher.launcher as launcher

import pygame

SERVER_SIDE = 0
CLIENT_SIDE = 1

DATAFILE_PATH = r"./local/client/player_profile.data"

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
        self.__launcher_properties = launcher.launch(self)
        self.__client_uuid = None
        if(not(self.__launcher_properties[0])):
            self.__client_uuid = self.__launcher_properties[2]
        self.__user = self.__launcher_properties[1]

        self.__abort_launch = False
        self.__player_entity = None
        self.__connected_players = []


    def start(self):
        if(self.__side == SERVER_SIDE): raise net_exception.WrongSideException("Denied access: Server side can't use this method")
        self.__net_listening = True;
        self.__net_listener.start()



        if(self.__client_uuid == None):
            self.__socket.sendto(connection_packet.ClientInitPacket(user=self.__user, code=0x80).encode(), self.__server_access)
        else:
            self.__socket.sendto(connection_packet.ClientInitPacket(user=self.__user, code=0x0, guuid=self.__client_uuid).encode(), self.__server_access)

    def update(self):
        temp = self.__connected_players.copy()
        temp.append(self.__player_entity)
        for player in temp:
            if(player.is_move_right()):
                player.set_position((player.get_position()[0] + 5, player.get_position()[1]))

            if(player.is_move_left()):
                player.set_position((player.get_position()[0] - 5, player.get_position()[1]))

    def render(self, screen):
        screen.fill(self.__map.get_background())
        floor = pygame.Surface((1280, self.__map.get_floor_height()))
        floor.fill((0, 0, 0))
        floor.set_alpha(50)
        screen.blit(floor, (0, 720 - floor.get_height()))

        self.__player_entity.get_displayer().render(screen)
        for player in self.__connected_players:
            player.get_displayer().render(screen)

    def game_loop(self):
        while(not(self.__ready)):
            if(self.__abort_launch):
                pygame.quit()
                return

        clock = pygame.time.Clock()
        #d_info = pygame.display.Info()
        #screen = pygame.display.set_mode((d_info.current_w, d_info.current_h))
        screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("CGame")

        while(self.__run):
            #print(clock.get_fps())
            if(self.__player_entity != None):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.__run = False
                        self.__socket.sendto(connection_packet.ClientQuitPacket(uuid=self.__player_entity.get_uuid()).encode(), self.__server_access)
                        break
                    elif(event.type == pygame.KEYDOWN):
                        if(event.key == 100):
                            self.__player_entity.set_move(entity.MOVE_RIGHT)
                            self.__socket.sendto(player_packet.ClientPlayerMovePacket(player=self.__player_entity).encode(), self.__server_access)
                        elif(event.key == 113):
                            self.__player_entity.set_move(entity.MOVE_LEFT)
                            self.__socket.sendto(player_packet.ClientPlayerMovePacket(player=self.__player_entity).encode(), self.__server_access)
                    elif(event.type == pygame.KEYUP):
                        if(event.key == 100):
                            self.__player_entity.clear_move(entity.MOVE_RIGHT)
                            self.__socket.sendto(player_packet.ClientPlayerMovePacket(player=self.__player_entity).encode(), self.__server_access)
                        elif(event.key == 113):
                            self.__player_entity.clear_move(entity.MOVE_LEFT)
                            self.__socket.sendto(player_packet.ClientPlayerMovePacket(player=self.__player_entity).encode(), self.__server_access)

                self.update()
                self.render(screen)

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

    def new_profile(self, uuid):
        self.__client_uuid = uuid
        print("[{}] <init> storing the profile: ({}, {}) in memory".format(threading.current_thread().getName(), self.__user, str(self.__client_uuid)))
        if(not(os.path.exists(DATAFILE_PATH))): open(DATAFILE_PATH, "x")
        with open(DATAFILE_PATH, "rb+") as file:
            content = file.read()
            if(len(content)):
                file.write(str.encode("&{}:{}".format(self.__user, self.__client_uuid)))
            else:
                file.write(str.encode("{}:{}".format(self.__user, self.__client_uuid)))
        print("[{}] <init> profile created".format(threading.current_thread().getName()))

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

    def clear_run(self):
        self.__run = False

    def set_uuid(self, player_uuid):
        self.__client_uuid = player_uuid

    def get_uuid(self):
        return self.__client_uuid

    def set_player_entity(self, entity):
        self.__player_entity = entity

    def get_player(self):
        return self.__player_entity

    def set_abort_launch(self):
        self.__abort_launch = True

    def get_connected_players(self):
        return self.__connected_players

    def get_entity_by_instance_id(self, instance_id):
        if(self.__player_entity.get_instance_id() == instance_id):
            return self.__player_entity

        for player in self.__connected_players:
            if(player.get_instance_id() == instance_id):
                return player
