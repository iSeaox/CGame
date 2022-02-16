class GenericPacket:
    def __init__(self):
        self.__side = None
        self.__data = None
        self.__id = None
        self.__sender = None

    def get_sender(self):
        return self.__sender

    def set_sender(self, sender):
        self.__sender = sender;

    def get_side(self):
        return self.__side

    def get_data(self):
        return self.__data

    def get_id(self):
        return self.__id

    def process(self, handler):
        raise NotImplementedError("Subclass must implemen this abstract method")

    def encode(self):
        raise NotImplementedError("Subclass must implemen this abstract method")

    def decode(self, raw_data):
        raise NotImplementedError("Subclass must implemen this abstract method")
