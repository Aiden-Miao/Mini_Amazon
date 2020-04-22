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
TOTALL_WHNUM = 1
SPEED = 99999
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

#init, create the socket for world
def init_world():
    WORLD_SOCKET = create_socket(World_address)
        
"""
------------------------world function---------------------
"""
#world handler
def world_handler():
    world_response = recv_message(WORLD_SOCKET, world_amazon.AResponses)
    for errors in world_response.error:
        print("The error is from command: ", errors.originseqnum)
        print("The error is: ", errors.err)
        
    for allack in world_response.acks:
        print("Receivce ack number: ", allack)

    for arrive in world_response.arrived:
        print("purchase more succeed, ready to pack!")
        arrive_handler(arrive)

    for packed in world_response.ready:
        print("order packed, ready to load!")
        packed_handler(packed)

    for loaded in world_response.loaded:
        print("order loaded, ready to let truck go!")
        loaded_handler(loaded)

    if world_response.finished == True:
        print("Close world connection...")
        WORLD_SOCKET.close()

        
#send_world_ack
def send_world_ack(world_response):
    response = world.ACommands()
    response.acks.append(world_response.seqnum)
    send_msg(response, WORLD_SOCKET)
#deal with arrived products    

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

"""
------------------------website function--------------------
"""
#In this function, we keep search in the database, see if there is any order open. If it is open, then we start working on this order
def web_handler():
    print("enter buy on website")
    while(True):
        try:
            cur = conn.cursor()
            cur.execute("SELECT id FROM AmazonWeb_order WHERE is_processed = False;")
            unprocessed_order = cur.fetchall()
            for orders in unprocessed_order:
                order_id = orders[0]
                #update the wharehouse
                whnum = purchase_in_warehouse(amount,order_id)
                cur.execute("UPDATE AmazonWeb_order SET warehouse_id = %s WHERE id =%s",(whnum, unique_id))
                cur.execute("UPDATE AmazonWeb_order SET is_processed = %s",("True"))
                tobuy(order_id)
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error) 
            
#return wh number
def purchase_in_warehouse(amount,order_id):
    num = 1
    return num

#this function purchase more in warehouse
def tobuy(order_id):
    #whnum = order_id % TOTALL_WHNUM
    try:
        cur = conn.cursor()
        cur.execute("SELECT id,products,quantity FROM AmazonWeb_order WHERE id = %s",(order_id))
        row = cur.fetchone()
        order_id = row[0]
        amount = row[2]
        cur.execute("SELECT name,description FROM AmazonWeb_Product WHERE id = %s",(row[1]))
        detail = cur.fetchone()
        name = detail[0]
        description = detail[1]
        command = world_amazon.ACommands()
        command.simspeed = SPEED
        BUY = command.buy.add()
        allproducts = BUY.things.add()
        allproducts.id = order_id
        #maybe description can be the same as name?
        allproducts.description = description
        allpruducts.count = amount
        send_message(WORLD_SOCKET, command)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error) 
"""
#check the availability of a product
def check_availability(orderid, amount):
    try:
        cur = conn.cursor()
        cur.execute("SELECT products FROM ")
"""
    
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
    thread3 = threading.Thread(target = web_handler)
    main()
