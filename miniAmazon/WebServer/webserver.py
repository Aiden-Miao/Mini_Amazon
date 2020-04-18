import world_amazon_pb2
import world_ups_pb2
import AtoU_pb2
import threading
import psycopg2
import socket
from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _VarintEncoder
from google.protobuf.internal.encoder import _VarintBytes


World_address = ("vcm-12360.vm.duke.edu", 23456)
Ups_address = ("vcm-12360.vm.duke.edu", xxxx)




#send message
def send_msg(message, socket):
    """encode msg ad protobuf varint and sent through socket"""
    message_serialized = message.SerializeToString()
    length = message.ByteSize()
    socket.sendall(_VarintBytes(length) + message_serialized)

#recv message
def recv_msg(message_type, socket):
    """recv msg fro the world, and parse it"""
    var_int_buff = []
    while True:
        buf = socket.recv(1)
        var_int_buff += buf
        msg_len, new_pos = _DecodeVarint32(var_int_buff, 0)
        if new_pos != 0:
            break
    whole_message = socket.recv(msg_len)
    message = message_type()
    message.ParseFromString(whole_message)
    print("The response message is:")
    print(message)
    return message

#give a address, open a socket
def create_socket(address):
    test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    test_socket.connect(address)

#connect to world
def connect_world(socket, worldID):
    connect_msg = world_amazon_pb2.AConnect()
    connect_msg.worldid = worldID
    connect_msg.isAmazon = True
    send_msg(connect_msg,socket)
    response = recv_msg(world_amazon_pb2.AConnected, socket)
    if response.result == "connected!":
        print("Amazon Connect to world:" + str(response.worldid) + " succeed!")
    else:
        print("Amazon Connect to world:" + str(response.worldid) + " fails!")


#send message from amazon to ups and receive response
def AMAZON_to_UPS(message):
    UPS_socket = create_socket(Ups_address)
    send_msg(message, UPS_socket)
    response = recv_msg(AtoU_pb2.UtoAResponses, UPS_socket)
    UPS_socket.close()
    return response



        
#Ups connect to world(only for test)
def connect_worldUps(socket, worldID):
    connect_msg = world_ups_pb2.UConnect()
    #connect_msg.worldid = worldID
    connect_msg.isAmazon = False
    send_msg(connect_msg,socket)
    response = recv_msg(world_ups_pb2.UConnected, socket)
    if response.result == "connected!":
        print("UPS Connect to world:" + str(response.worldid) + " succeed!")
    else:
        print("UPS Connect to world:" + str(response.worldid) + " fails!")

#main function. used to test
def main():
    World_add = ("vcm-12360.vm.duke.edu", 23456)
    test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    test_socket.connect(World_add)
    #For test
    World2_add = ("vcm-12360.vm.duke.edu", 12345)
    test_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    test_socket2.connect(World2_add)
    
    #connection = psycopg2.connect(host="vcm-12360.vm.duke.edu",database="postgres",user="postgres",password = "postgres", port="5432")
    connect_worldUps(test_socket2, 1)
    connect_world(test_socket, 1)

if __name__ == "__main__":
    main()
