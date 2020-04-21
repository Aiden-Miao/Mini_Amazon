import world_amazon_pb2 as world_amazon
import world_ups_pb2 as world_ups
#import AtoU_pb2
#import UtoA_pb2
import ups_amazon_pb2 as ups_amazon
import threading
import psycopg2
import socket
from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _VarintEncoder
from google.protobuf.internal.encoder import _VarintBytes


World_address = ("vcm-12369.vm.duke.edu", 23456)
Ups_address = ("0.0.0.0", 34567)
conn = psycopg2.connect(host = "vcm-12360.vm.duke.edu",database = "postgres", user = "postgres",port = "5433")
global WORLD_SOCKET
global Seq

"""
--------------------basic function------------------
"""
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
    return test_socket

#connect to world
def connect_world(socket, worldID):
    connect_msg = world_amazon.AConnect()
    connect_msg.worldid = worldID
    connect_msg.isAmazon = True
    send_msg(connect_msg,socket)
    response = recv_msg(world_amazon.AConnected, socket)
    if response.result == "connected!":
        print("Amazon Connect to world:" + str(response.worldid) + " succeed!")
    else:
        print("Amazon Connect to world:" + str(response.worldid) + " fails!")
        
"""
------------------------world function---------------------
"""
#send_world_ack
def send_world_ack(world_response):
    response = world.ACommands()
    response.acks.append(world_response.seqnum)
    send_msg(response, WORLD_SOCKET)
    
#Purchase the product
def purchase_product(purchasemore):
    print("start puchasing product")
    send_world_ack(purchasemore)
    try:
        cur = conn.cursor
#pack the product
def pack_product(whNum, product):
    command = world_amazon.ACommands()
    pack_msg = command.topack.add()
    product = pack_msg.things.add()
    send_msg(command, WORLD_SOCKET)

#send message from amazon to ups and receive response
def AMAZON_to_UPS(message):
    UPS_socket = create_socket(Ups_address)
    send_msg(message, UPS_socket)
    response = recv_msg(ups_amazon.UMessages, UPS_socket)
    UPS_socket.close()
    return response

#init, create the socket for world
def init_world():
    WORLD_SOCKET = create_socket(World_address)

"""
------------------------website function--------------------
"""
def buy_on_website():
    print("enter buy on website")

#main function. used to test
def main():
    #amazon first creates the socket,then UPS connect to it. UPS connect to world then send worldid to amazon
    #amazon use this worldid to connect to the world
    test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    test_socket.bind(Ups_address)
    print("start listening")
    test_socket.listen(5)
    print("after listen")
    ups_socket = test_socket.accept()[0]
    print("after accept")
    response = recv_msg(UtoA_pb2.UMessages,ups_socket)
    world_socket = create_socket(World_address)
    print(response.connectWorld.worldid[0])
    connect_world(world_socket, response.connectWorld.worldid[0])
    
if __name__ == "__main__":
    thread1 = threading.Thread(target = world_handler, args = (,))
    thread2 = threading.Thread(target = ups_handler, args = (,))
    thread3 = threading.Thread(target = world_handler, args = (,))
    main()
