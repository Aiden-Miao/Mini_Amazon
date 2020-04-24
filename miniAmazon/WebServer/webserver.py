import world_amazon_pb2 as world_amazon
import world_ups_pb2 as world_ups
import ups_amazon_pb2 as ups_amazon
import threading
import psycopg2
import socket
from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _VarintEncoder
from google.protobuf.internal.encoder import _VarintBytes

#World_address = ("vcm-14419.vm.duke.edu", 23456)
#World_address = ("vcm-12360.vm.duke.edu", 23456)
World_address = ("vcm-12369.vm.duke.edu", 23456)
Ups_address = ("0.0.0.0", 34567)
conn = psycopg2.connect(host = "",database = "postgres", user = "postgres",port = "5432",password="postgres")

WORLD_SOCKET = 0
UPS_SOCKET = 0
WORLD_ID = 0

SEQ = 1
TOTALL_WHNUM = 1
SPEED = 5

"""
--------------------basic function------------------
"""
#send message
def send_msg(message, socket):
    """encode msg ad protobuf varint and sent through socket"""
    print("sending message: ", message)
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
def connect_world(socket):
    connect_msg = world_amazon.AConnect()
    connect_msg.worldid = WORLD_ID
    connect_msg.isAmazon = True

    #init warehouse
    world_msg = connect_msg.initwh.add()
    world_msg.x = 100
    world_msg.y = 100
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO amazonweb_warehouse (x_location, y_location) VALUES (%s, %s)",("100", "100"))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    world_msg.id = create_warehouse()
    
    send_msg(connect_msg,socket)
    response = recv_msg(world_amazon.AConnected, socket)
    if response.result == "connected!":
        print("Amazon Connect to world:" + str(response.worldid) + " succeed!")
    else:
        print("Amazon Connect to world:" + str(response.worldid) + " fails!")
        
#init, create the socket for world and UPS, get the worldid from ups, and connect to the world
def init_world():
    global SEQ
    global WORLD_SOCKET
    global UPS_SOCKET
    global WORLD_ID
    
    WORLD_SOCKET = create_socket(World_address)

    #create the ups socket
    tmp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tmp_socket.bind(Ups_address)
    print("start listening")
    tmp_socket.listen(5)
    print("after listen")
    UPS_SOCKET = tmp_socket.accept()[0]
    print("after accept")
    
    #ask ups for worldid
    command = ups_amazon.AMessages()
    command.initialWorldid.seqnum = SEQ
    SEQPLUS()
    send_msg(command, UPS_SOCKET)

    #get the worldid from ups, can connect to world
    response1 = recv_msg(ups_amazon.UMessages,UPS_SOCKET)
    response = recv_msg(ups_amazon.UMessages,UPS_SOCKET)
    send_ups_ack(response.initialWorldid)
    WORLD_ID = response.initialWorldid.worldid[0]
    #WORLD_ID = 17
    #connect to the world
    connect_world(WORLD_SOCKET)
    """
    #init warehouse
    world_msg = world_amazon.AInitWarehouse()

    world_msg.x = 100
    world_msg.y = 100
   
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO amazonweb_warehouse (x_location, y_location) VALUES (%s, %s)",("100", "100"))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    world_msg.id = create_warehouse()
    print("init warehouse id is:", world_msg.id)
    send_msg(world_msg, WORLD_SOCKET)
    """

#use a mutex for SEQ++:
def SEQPLUS():
    mutex = threading.Lock()
    with mutex:
        global SEQ
        SEQ = SEQ + 1
    
"""
------------------------world function---------------------
"""
#world handler
def world_handler():
    while(1):
        world_response = recv_msg(world_amazon.AResponses,WORLD_SOCKET)
        for errors in world_response.error:
            print("The error is from command: ", errors.originseqnum)
            print("The error is: ", errors.err)
            
        for allack in world_response.acks:
            print("Receive ack number from world: ", allack)
                
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
            break

        
#send_world_ack
def send_world_ack(world_response):
    response = world_amazon.ACommands()
    response.acks.append(world_response.seqnum)
    send_msg(response, WORLD_SOCKET)
    
#deal with arrived products    
def arrive_handler(arrive):
    send_world_ack(arrive)
    try:
        cur = conn.cursor()
        #if products purchase has arrived, then we start processing these orders
        print("in prorgess")
        cur.execute("SELECT id FROM AmazonWeb_order WHERE status = 'in progress';")
        rows = cur.fetchall()
        for row in rows:
            cur.execute("SELECT products_id, quantity, warehouse_id FROM AmazonWeb_order WHERE id = %s;",(row))
            info = cur.fetchone()
            cur.execute("SELECT name, description FROM AmazonWeb_product WHERE id = %s;",([info[0]]))
            detail = cur.fetchone()
            
            command = world_amazon.ACommands()
            #command.simspeed = SPEED
            myorder = command.topack.add()
            myorder.shipid = row[0]
            myorder.whnum = info[2]
            myorder.seqnum = SEQ
            SEQPLUS()
            mythings = myorder.things.add()
            mythings.id = info[0]
            mythings.description = detail[1]
            mythings.count = info[1]
            #send msg to world, ask for start packing
            send_msg(command, WORLD_SOCKET)
            cur.execute("UPDATE AmazonWeb_order SET status = 'packing' WHERE id = %s;", (row))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


#handle packed order: The order is already packed, now we need to update its status to loading, and send load message to world
def packed_handler(packed):
    send_world_ack(packed)
    try:
        #get truck after we already packed the products
        print("the ship id is:", packed.shipid)
        get_truck(packed.shipid)
        cur = conn.cursor()
        cur.execute("UPDATE AmazonWeb_order SET status = 'loading' WHERE id = %s;",([packed.shipid]))
        """
        command = world_amazon.ACommands()
        command.simspeed = SPEED
        load_package = command.load.add()
        cur.execute("SELECT warehouse_id FROM AmazonWeb_order WHERE id = %s;",(packed.shipid))
        whNum = cur.fetchone()[0]
        load_package.whnum = whNum
        load_package.shipid = packed.shipid
        load_package.seqnum = SEQ
        SEQPLUS()
        while(1):
            cur.execute("SELECT trucknum FROM AmazonWeb_truck WHERE warehouse_id = %s;",(whNum))
            row = cur.fetchone()
            if row != None:
                break
        load_package.truckid = row[0]

        #send message to world to start loading
        send(command, WORLDSOCKET)
        """
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

#handle loaded order: The order is already loaded, now we need to send message to ups to deliver the package
def loaded_handler(loaded):
    send_world_ack(loaded)
    try:
        cur = conn.cursor()
        cur.execute("UPDATE AmazonWeb_order SET status = 'loaded' WHERE id = %s;",([loaded.shipid]))
        cur.execute("SELECT warehouse_id,truck_id FROM AmazonWeb_order WHERE id = %s;",([loaded.shipid]))
        row = cur.fetchone()
        whid = row[0]
        truckid = row[1]
        command = ups_amazon.AMessages()
        Deliver = command.delivers.add()
        Deliver.truckid = truckid
        Deliver.worldid = WORLD_ID
        Deliver.seqnum = SEQ
        SEQPLUS()
        #send message for ups to start deliver package
        cur.execute("UPDATE AmazonWeb_order SET status = 'in delivery' WHERE id = %s;",([loaded.shipid]))
        send_msg(command, UPS_SOCKET)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        
        
#send message from amazon to ups and receive response
def AMAZON_to_UPS(message):
    UPS_socket = create_socket(Ups_address)
    send_msg(message, UPS_socket)
    response = recv_msg(ups_amazon.UMessages, UPS_socket)
    UPS_socket.close()
    return response
"""
--------------------------ups function------------------------
"""
#send_ups_ack
def send_ups_ack(ups_response):
    print("send ack back to ups: ack = ",ups_response.seqnum)
    response = ups_amazon.AMessages()
    response.acks.append(ups_response.seqnum)
    send_msg(response, UPS_SOCKET)
    
def ups_handler():
    while(1):
        ups_response = recv_msg(ups_amazon.UMessages,UPS_SOCKET)
        for allacks in ups_response.acks:
            print("Receive ack number from ups: ", allacks)
        for alltruckreadies in ups_response.truckReadies:
            print("truck is ready: ", alltruckreadies.truckid)
            send_ups_ack(alltruckreadies)
            update_truckinfo(alltruckreadies)
            trucks_handler(alltruckreadies)
        for deliveredpackage in ups_response.deliveredpackages:
            print("package delivered: ", deliveredpackage.packageid)
            send_ups_ack(deliveredpackage)
            delivered_handler(deliverpackage)
        """    
        for allaccount in ups_response.accountResult:
            print("receive account result")
            send_ups_ack(allaccount)
        """
        
#This funtion update the truck info in database
def update_truckinfo(alltruckreadies):
    print("UPS truck is ready, id is: ", alltruckreadies.truckid)
    try:
        cur = conn.cursor()
        #get the warehouse id
        print("get the warehouse id for ups")
        cur.execute("SELECT warehouse_id FROM AmazonWeb_order WHERE id = %s;",([alltruckreadies.packageid]))
        row = cur.fetchone()
        whnum = row[0]
        #if the truck record does nor exist, create a new one
        print("check if truck exists")
        cur.execute("SELECT id FROM AmazonWeb_truck WHERE truck_num = %s;",([alltruckreadies.truckid]))
        mytruck = cur.fetchone()
        if mytruck == None:
            cur.execute("INSERT INTO AmazonWeb_truck (truck_num, warehouse_id) VALUES (%s, %s)",(alltruckreadies.truckid, whnum))
        else:
            cur.execute("UPDATE AmazonWeb_truck SET warehouse_id = %s WHERE truck_num = %s;",(whnum,alltruckreadies.truckid))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        
#trucks handler, this function search through the database for the order, update the truck_id inside the order, and load it.
def trucks_handler(alltruckreadies):
    order_id = alltruckreadies.packageid
    try:
        cur = conn.cursor()
        print("enter truck handler")
        cur.execute("SELECT warehouse_id FROM AmazonWeb_order WHERE id = %s;",([order_id]))
        command = world_amazon.ACommands()
        #command.simspeed = SPEED
        load_package = command.load.add()
        row = cur.fetchall()
        whNum = row[0][0]
        print("warehouse number is: ", whNum)
        load_package.whnum = whNum
        print("shipid is: ", order_id)
        load_package.shipid = order_id
        print("SEQ is: ", SEQ)
        load_package.seqnum = SEQ
        SEQPLUS()
        load_package.truckid = alltruckreadies.truckid

        #update order database, set the truck id
        print("update to in deliver")
        cur.execute("UPDATE AmazonWeb_order SET truck_id = %s WHERE id = %s;",(alltruckreadies.truckid, order_id))

        #send message to world to start loading
        print("ask world to start loading")
        send_msg(command, WORLD_SOCKET)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        
#This function request the truck from ups
def get_truck(order_id):
    try:
        print("enter get truck")
        cur = conn.cursor()
        cur.execute("SELECT id, dst_x, dst_y, products_id, quantity, user_id, warehouse_id FROM AmazonWeb_order WHERE id = %s;",([order_id]))
        row = cur.fetchone()
        command = ups_amazon.AMessages()
        gettruck = command.getTrucks.add()
        gettruck.whid = row[6]
        gettruck.packageid = row[0]
        gettruck.x = row[1]
        gettruck.y = row[2]
        
        gettruck.seqnum = SEQ
        SEQPLUS()
        gettruck.worldid = WORLD_ID
        
        #get the user name from django's db
        print("get user name")
        user_id = row[5]
        cur.execute("SELECT username FROM auth_user WHERE id = %s;",([user_id]))
        user = cur.fetchone()
        print("user name is: ",user[0])
        name = user[0]
        print("user name is:", name)
        gettruck.uAccountName = name
        
        #use the product id to get the description from product
        print("get product detail")
        myproduct = gettruck.product.add()
        cur.execute("SELECT description FROM AmazonWeb_product WHERE id = %s;",([row[3]]))
        product_detail = cur.fetchone()
        myproduct.description = product_detail[0]
        myproduct.productid = row[3]
        myproduct.count = row[4]
        
        #send message to request truck
        send_msg(command, UPS_SOCKET)
        print("send truck successfully")
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        
#This function update the order info to delivered
def delivered_handler(packages):
    order_id = packages.packageid
    try:
        cur = conn.cursor()
        cur.execute("UPDATE amazonweb_order SET status = 'delivered' WHERE id = %s;",([order_id]))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error) 
        
"""
------------------------website function--------------------
"""
#In this function, we keep search in the database, see if there is any order open. If it is open, then we start working on this order. We use the order id to purchase from world and request truck, then change status to "packing"
def web_handler():
    print("enter buy on website")
    while(1):
        try:
            cur = conn.cursor()
            cur.execute("SELECT id FROM amazonweb_order WHERE is_processed = False AND products_id > 0;")
            unprocessed_order = cur.fetchall()
            for orders in unprocessed_order:
                order_id = orders
                #update the wharehouse
                amount = 0
                whnum = purchase_in_warehouse(amount,order_id)
                print("start set warehouse id")
                cur.execute("UPDATE AmazonWeb_order SET warehouse_id = %s WHERE id =%s;",(whnum, order_id))
                print("order is processed")
                cur.execute("UPDATE AmazonWeb_order SET is_processed = True WHERE id =%s;",([order_id]))
                print("ready to buy")
                tobuy(order_id)
                print("after tobuy order")
                #cur.execute("UPDATE AmazonWeb_order SET status = %s WHERE id =%s;",("packing",unique_id))
                conn.commit()
                cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error) 
            
#return wh number
def purchase_in_warehouse(amount,order_id):
    try:
        cur = conn.cursor()
        cur.execute("SELECT id FROM amazonweb_warehouse;")
        row = cur.fetchall()
        num = row[0][0]
        return num
    except (Exception, psycopg2.DatabaseError) as error:
        print(error) 

#return wh number
def create_warehouse():
    try:
        cur = conn.cursor()
        cur.execute("SELECT id FROM amazonweb_warehouse;")
        row = cur.fetchone()
        num = row[0]
        return num
    except (Exception, psycopg2.DatabaseError) as error:
        print(error) 

#In this function, we purchase more from world and request a truck for our product
def tobuy(order_id):
    #whnum = order_id % TOTALL_WHNUM
    try:
        cur = conn.cursor()
        #get the orderid, productsid, amount and warehouseid
        print("start selecting order tobuy")
        cur.execute("SELECT id, products_id, quantity, warehouse_id FROM AmazonWeb_order WHERE id = %s",([order_id]))
        row = cur.fetchone()
        order_id = row[0]
        amount = row[2]
        #get the name and description from product
        cur.execute("SELECT name,description FROM AmazonWeb_Product WHERE id = %s",([row[1]]))
        detail = cur.fetchone()
        name = detail[0]
        description = detail[1]
        
        command = world_amazon.ACommands()
        #command.simspeed = SPEED
        BUY = command.buy.add()
        BUY.whnum = row[3]
        BUY.seqnum = SEQ
        SEQPLUS()
        allproducts = BUY.things.add()
        allproducts.id = row[1]
        allproducts.description = description
        allproducts.count = amount
        send_msg(command, WORLD_SOCKET)
        print("after purchase more")
        #shouldn'e get truck here, should get truck after packed
        #get_truck(order_id)
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
    """
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
    """
    
if __name__ == "__main__":
    init_world()
    thread1 = threading.Thread(target = world_handler, args = ())
    thread2 = threading.Thread(target = ups_handler, args = ())
    thread3 = threading.Thread(target = web_handler, args = ())
    all_thread =[thread1, thread2, thread3]
    for th in all_thread:
        th.start()
    for th in all_thread:
        th.join()
