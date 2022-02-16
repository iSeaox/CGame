import os, sys
sys.path.insert(1, os.path.abspath("."))
print(sys.path)

import time

import networking.server as server

local_ip = "172.21.9.175"
local_port = 20001
buffer_size = 1024

game_server = server.Server(local_ip, local_port, server.SERVER_SIDE)
game_server.start()

while(1):
    pass
