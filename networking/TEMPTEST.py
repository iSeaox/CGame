import packet
import packet_client.connection_packet as connection_packet
import struct

raw_data = str.encode("Vous avez été banni du jeu")
print(raw_data)
print(len(raw_data))
print(raw_data[27])
