import pygame
import threading
import os
import uuid

import networking.client as client

name_charset = ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "_")

def launch(client_object):
    print("[{}] <launcher> starting of launcher".format(threading.current_thread().getName()))
    print("[{}] <launcher> searching for relative player data".format(threading.current_thread().getName()))
    profiles_found = __get_stored_player_profile(client.DATAFILE_PATH)
    print("[{}] <launcher> result: {} profile(s) found".format(threading.current_thread().getName(), len(profiles_found)))

    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    input_box = pygame.Rect(640 / 2 - 125, 480 / 2 - 20, 250, 40)
    font = pygame.font.Font(None, 32)
    value = "simpletest"

    timer = pygame.time.Clock()
    run = True



    while(run):
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                run = False
                break
            elif(event.type == pygame.KEYDOWN):
                if(event.key == pygame.K_RETURN):
                    pass
                elif(event.key == pygame.K_BACKSPACE):
                    value = value[:(len(value) - 1)]
                else:
                    if(event.unicode.lower() in name_charset and len(value) < 20):
                        value += event.unicode


        screen.fill((153, 63, 35))
        user_surface = font.render(value, True, (0, 0, 0))
        pygame.draw.rect(screen, (97, 39, 21), input_box, 2)
        screen.blit(user_surface, (input_box.x + 8, input_box.y + 8))




        pygame.display.flip()
        timer.tick(20)
    pygame.quit()


def __get_stored_player_profile(path) -> dict:
    player_profile = {}
    if(os.path.exists(path)):
        with open(path, "rb") as profile_file:
            raw = profile_file.read().decode()
            profiles = raw.split("&")
            for profile in profiles:
                temp = profile.split(":")
                player_profile[temp[0]] = uuid.UUID(temp[1])
    return player_profile
