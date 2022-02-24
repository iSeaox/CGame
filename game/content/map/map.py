import struct

class Map:
    def __init__(self, background_color=(0xFF, 0xFF, 0xFF), floor_height=30):
        self.__background_color = background_color
        self.__floor_height = floor_height

    def encode(self):
        return struct.pack("BBBH", self.__background_color[0], self.__background_color[1], self.__background_color[2], self.__floor_height)

    def decode(self, raw_data):
        temp = struct.unpack("BBBH", raw_data)
        self.__background_color = (temp[0], temp[1], temp[2])
        self.__floor_height = temp[3]
        return self

    def get_background(self):
        return self.__background_color

    def get_floor_height(self):
        return self.__floor_height
