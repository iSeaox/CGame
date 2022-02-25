import os, sys
sys.path.insert(1, os.path.abspath("."))

import time
import uuid
import networking.client as client

server_access = ("172.21.4.123", 20001)

#data = "admin:89e3ef8f-ca2e-4b90-b961-20cfdadb62d1&pierrot:48f7db21-5a05-4a75-9230-c34d3ee72c4a&pedro:4bea40bf-5ae0-4d99-ab12-32fb67a45615&MarCo:1fd6f327-87c4-45cf-a170-0dbcb0d2c722"

game_client = client.Client(server_access, client.CLIENT_SIDE)


game_client.start()
game_client.game_loop()

time.sleep(2)
game_client.get_socket().close()
