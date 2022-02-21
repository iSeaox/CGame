import pygame

import game.entity.entity as entity

class Displayer:

    def __init__(self, obj_to_display):
        self.__object = obj_to_display

    def render(self, display):
        if(isinstance(self.__object, entity.Entity)):
            if(self.__object.get_id() == entity.EntityEnum.PLAYER.value):
                player = pygame.Surface((50, 50))
                player.fill((0, 0, 0))
                display.blit(player, self.__object.get_position())
