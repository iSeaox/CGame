import struct

from enum import Enum

class EntityEnum(Enum):
    PLAYER = 0

MOVE_RIGHT = 0
MOVE_LEFT = 1

class Entity:
    NEXT_INSTANCE_ID = 0

    def __init__(self):
        self.__position = (0.0, 0.0)
        self.__id = 0
        self.__instance_id = Entity.NEXT_INSTANCE_ID
        Entity.NEXT_INSTANCE_ID += 1
        self.__displayer = None
        self.__move_right = False
        self.__move_left = False

    def encode_property(self) -> bytes:
        temp = 0x0
        if(self.__move_right):
            temp += (1 << 15)
        if(self.__move_left):
            temp += (1 << 14)

        return struct.pack("H", temp)

    def decode_property(self, raw_data) -> bytes:
        raw_prop = struct.unpack("H", raw_data)[0]
        if(0x8000 & raw_prop):
            self.__move_right = True
        else:
            self.__move_right = False

        if(0x4000 & raw_prop):
            self.__move_left = True
        else:
            self.__move_left = False


    def decode_header(self, raw_header):
        temp_data = struct.unpack("HI dd", raw_header[0:24])
        self.__id = temp_data[0]
        self.__instance_id = temp_data[1]
        self.__position = (temp_data[2], temp_data[3])
        self.decode_property(raw_header[24:26])

        return self

    def get_encode_header(self):
        temp = struct.pack("HI dd", self.get_id(), self.get_instance_id(), self.get_position()[0], self.get_position()[1])
        temp += self.encode_property()
        return temp

    def encode(self):
        raise NotImplementedError("Subclass must implement this abstract method")

    def decode(self, raw_data):
        raise NotImplementedError("Subclass must implement this abstract method")

    def get_displayer(self):
        return self.__displayer

    def get_id(self):
        return self.__id

    def get_position(self):
        return self.__position

    def set_position(self, pos):
        self.__position = pos

    def get_instance_id(self):
        return self.__instance_id

    def set_instance_id(self, instance_id):
        self.__instance_id = instance_id

    def set_move(self, direction):
        if(direction == MOVE_RIGHT):
            self.__move_right = True
        elif(direction == MOVE_LEFT):
            self.__move_left = True

    def clear_move(self, direction):
        if(direction == MOVE_RIGHT):
            self.__move_right = False
        elif(direction == MOVE_LEFT):
            self.__move_left = False

    def is_move_right(self):
        return self.__move_right

    def is_move_left(self):
        return self.__move_left
