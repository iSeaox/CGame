import struct
import uuid

import game.entity.entity as entity
import game.display.display as display

class Player(entity.Entity):
    def __init__(self, name=None, player_uuid=None, server=False):
        super().__init__()

        self.__id = entity.EntityEnum.PLAYER.value
        self.__name = name
        self.__player_uuid = player_uuid
        if(not(server)):
            self.__displayer = display.Displayer(self)
        self.__head_angle = 90

    def encode(self) -> bytes:
        temp = self.get_encode_header()

        name_bytes = str.encode(self.__name)
        while len(name_bytes) < 20:
            name_bytes += struct.pack("B", 0)
        temp += name_bytes
        temp += self.__player_uuid.bytes
        temp += struct.pack("H", self.__head_angle)
        return temp

    def decode(self, raw_data):
        self.decode_header(raw_data[0:26])

        t_array = []
        for b in raw_data[26:46]:
            if(b == 0):
                break
            t_array.append(b)
        self.__name = bytearray(t_array).decode()
        self.__player_uuid = uuid.UUID(bytes=raw_data[46:62])
        self.__head_angle = struct.unpack("H", raw_data[62:64])[0]
        return self

    def get_name(self):
        return self.__name

    def get_uuid(self):
        return self.__player_uuid

    def set_uuid(self, new_uuid):
        self.__player_uuid = new_uuid

    def get_displayer(self):
        return self.__displayer
