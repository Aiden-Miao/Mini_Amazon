import world_amazon_pb2
import world_ups_pb2
import threading
import psycopg2
import socket
from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _VarintEncoder
from google.protobuf.internal.encoder import _VarintBytes
    
#send message
def send_msg(message, socket):
    """encode msg ad protobuf varint and sent through socket"""
    message_serialized = message.SerializeToString()
    length = message.ByteSize()
    socket.sendall(_VarintBytes(length) + message_serialized)

#recv message
def recv_msg(message_type, socket):
    """recv msg fro the world, and parse it"""
    data = b''
    while True:
        data += socket.recv(1)
        try:
            size = _DecodeVarint32(data,0)[0]
        except IndexError:
            continue
        break
    data = socket.recv(size)
    message = message_type()
    message.ParseFromString(data)
    print("The response message is:", message)
    return message

#connect to world
def connect_world(socket, worldID):
    connect_msg = world_amazon_pb2.AConnect()
    connect_msg.worldid = worldID
    connect_msg.isAmazon = True
    send_msg(connect_msg,socket)
    response = recv_msg(world_amazon_pb2.AConnected, socket)
    if response.result is "connected!":
        print("Connect to world:" + str(response.worldid) + " succeed!")
    else:
        print("Connect to world:" + str(response.worldid) + " fails!")
        
#main function. used to test
def main():
    World_add = ("vcm-12360.vm.duke.edu", 23456)
    test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    test_socket.connect(World_add)
    #connection = psycopg2.connect(host="vcm-12360.vm.duke.edu",database="postgres",user="postgres",password = "postgres", port="5432")
    connect_world(test_socket, 1)

if __name__ == "__main__":
    main()
