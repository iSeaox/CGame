import struct

from enum import Enum

class EntityEnum(Enum):
    PLAYER = 0

class Entity:
    NEXT_INSTANCE_ID = 0

    def __init__(self):
        self.__position = (0.0, 0.0)
        self.__id = 0
        self.__instance_id = Entity.NEXT_INSTANCE_ID
        Entity.NEXT_INSTANCE_ID += 1
        self.__displayer = None

    def decode_header(self, raw_header):
        temp_data = struct.unpack("HI dd", raw_header)
        self.__id = temp_data[0]
        self.__instance_id = temp_data[1]
        self.__position = (temp_data[2], temp_data[3])

        return self

    def get_encode_header(self):
        return struct.pack("HI dd", self.get_id(), self.get_instance_id(), self.get_position()[0], self.get_position()[1])

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
