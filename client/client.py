"""
    @author brandon
    entry point for the connection
"""
import pickle
import socket
import random

from packets.packet import Packet


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 4444))
    packet = Packet(opcode=1)
    print("connected")
    client.send(pickle.dumps(packet))
    print("sent packet with opcode 14")
    client.close()


if __name__ == '__main__':
    main()
