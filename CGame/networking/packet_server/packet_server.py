from enum import Enum

class ServerPacketEnum(Enum):
    SERVER_INIT_TRANSFER_PACKET = 0
    SERVER_PLAYER_ENTITY_TRANSFER_PACKET = 1
    
    SERVER_ENTITY_UPDATE_PACKET = 2
