import pygame

class Button:
    def __init__(self, y, font_height, label, color, center=True, padding=0, background_color=(0, 0, 0)):
        self.__label = label
        self.__color = color
        self.__background_color = background_color
        self.__y = y
        self.__center = center
        self.__padding = padding

        self.__font = pygame.font.Font(None, font_height)
        self.__active = False

    def render(self, screen):
        if(self.__center):
            alpha_color = (255, 0, 0)
            label_surface = self.__font.render(self.__label, False, self.__color)
            button_surface = pygame.Surface((label_surface.get_width() + self.__padding * 2, label_surface.get_height() + self.__padding * 2))
            button_surface.fill(self.__background_color)
            if(not(self.__active)):
                button_surface.set_alpha(50)

            border = pygame.Rect(0, 0, button_surface.get_width(), button_surface.get_height())
            pygame.draw.rect(button_surface, self.__color, border, 2, border_radius=5)

            button_surface.blit(label_surface, (self.__padding, self.__padding))
            screen.blit(button_surface, (screen.get_width() / 2 - button_surface.get_width() / 2, self.__y))

    def set_label(self, label):
        self.__label = label

    def set_active(self):
        self.__active = True

    def clear_active(self):
        self.__active = False
