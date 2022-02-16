import os, sys
sys.path.insert(1, os.path.abspath("."))

import time
import client

server_access = ("172.21.9.175", 20001)

game_client = client.Client(server_access, client.CLIENT_SIDE)
game_client.start()
game_client.game_loop()

time.sleep(5)
game_client.get_socket().close()
