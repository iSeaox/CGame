import os, sys
sys.path.insert(1, os.path.abspath("."))

import time
import uuid
import networking.client as client

server_access = ("172.21.9.118", 20001)

game_client = client.Client(server_access, client.CLIENT_SIDE)

game_client.start("admin")
game_client.game_loop()

time.sleep(5)
game_client.get_socket().close()
