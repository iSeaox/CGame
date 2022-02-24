from enum import Enum

class ClientPacketEnum(Enum):
    # Transfer Packet
    CLIENT_INIT_PACKET = 0

    # PLayer relative Packet
    CLIENT_PLAYER_MOVE_PACKET = 1
