import os, sys
sys.path.insert(1, os.path.abspath("."))
import time

import networking.server as server

local_ip = "10.70.208.242"
local_port = 20001
buffer_size = 1024

game_server = server.Server(local_ip, local_port, server.SERVER_SIDE)
game_server.start()

while(1):
    pass
