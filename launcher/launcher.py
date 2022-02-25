import pygame
import threading
import os
import uuid

import networking.client as client

import launcher.content.button as button

name_charset = ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "_")

def launch(client_object):
    print("[{}] <launcher> starting of launcher".format(threading.current_thread().getName()))
    print("[{}] <launcher> searching for relative player data".format(threading.current_thread().getName()))
    profiles_found = __get_stored_player_profile(client.DATAFILE_PATH)
    print("[{}] <launcher> result: {} profile(s) found".format(threading.current_thread().getName(), len(profiles_found)))

    pygame.init()
    pygame.display.set_caption("CGame Launcher")

    screen = pygame.display.set_mode((640, 480))
    input_box = pygame.Rect(640 / 2 - 180, 480 / 2 - 20 - 50, 360, 40)
    font = pygame.font.Font(None, 32)
    value = ""

    valid_button = button.Button(240, 40, "new", (97, 39, 21), padding=10, background_color=(153, 63, 35))

    timer = pygame.time.Clock()
    run = True
    abort = False



    while(run):
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                run = False
                abort = True
                break
            elif(event.type == pygame.KEYDOWN):
                if(event.key == pygame.K_RETURN):
                    run = False
                    break
                elif(event.key == pygame.K_BACKSPACE):
                    value = value[:(len(value) - 1)]
                else:
                    if(event.unicode.lower() in name_charset and len(value) < 20):
                        value += event.unicode


        screen.fill((153, 63, 35))

        user_surface = font.render(value, True, (28, 11, 6))
        pygame.draw.rect(screen, (97, 39, 21), input_box, 2, border_radius=5)
        screen.blit(user_surface, (input_box.x + (input_box.w / 2 - user_surface.get_width() / 2), input_box.y + 8))

        if(len(value) == 0):
            valid_button.clear_active()
        else:
            valid_button.set_active()

        if(value in profiles_found):
            valid_button.set_label("play")
        else:
            valid_button.set_label("new")

        valid_button.render(screen)

        pygame.display.flip()
        timer.tick(20)
    if(not(abort)):
        if(len(value) != 0):
            if(value in profiles_found):
                print("[{}] <launcher> launching with the profile of {} ({})".format(threading.current_thread().getName(), value, profiles_found[value]))
                return (False, value, profiles_found[value])
            else:
                print("[{}] <launcher> initialization of creation of the new profile for".format(threading.current_thread().getName(), value))
                return (True, value)
    else:
        print("[{}] <launcher> the execution of the launcher has been interrupted".format(threading.current_thread().getName()))
        client_object.get_socket().close()
        exit()


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
