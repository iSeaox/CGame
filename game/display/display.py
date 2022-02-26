import pygame

import game.entity.entity as entity

class Displayer:

    def __init__(self, obj_to_display):
        self.__object = obj_to_display
        if(isinstance(self.__object, entity.Entity)):
            if(self.__object.get_id() == entity.EntityEnum.PLAYER.value):
                self.__font = pygame.font.Font(None, 20)

    def render(self, display):
        if(isinstance(self.__object, entity.Entity)):
            if(self.__object.get_id() == entity.EntityEnum.PLAYER.value):
                player = pygame.Surface((50, 50))
                player.fill((0, 0, 0))
                display.blit(player, self.__object.get_position())
                user_pos = (self.__object.get_position()[0], self.__object.get_position()[1] - 20)
                text_sur = self.__font.render(self.__object.get_name(), True, (0, 0, 0))
                display.blit(text_sur, user_pos)
