import socket
from threading import Thread
# from python_socket_queryCall import *
from proteus_services_websocket import *
# from resources.genProcess import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind(("192.168.0.221", 8000))
server.bind(("10.1.1.175", 8000))

server.listen()
all_Client = {}

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("10.1.2.173",8001))
# client.connect(("192.168.0.236",8000))
ipaddress = '10.1.1.175,8000'

client.send(ipaddress.encode())


def client_thread(client):
    data = client.recv(10240).decode()
    print(data)

    # ic = IncentiveCalculation()
    # returnStr = ic.getQueryData(data, "true")
    data = getqueryData(data)
    print(data)
    for c in all_Client:
        if c == client:
            client.send(data.encode())

    

while True:
    client, address = server.accept()
    # print("client : ", client)
    # print("Address : ", address)
    name = client.recv(1024).decode()
    all_Client[client] = name

    thread = Thread(target=client_thread, args=(client,))
    thread.start()


    


# while True:
#     serverclient, address = server.accept()
#     print("client : ", client)
#     print("Address : ", address)
#
#     serverclient.send(address.encode())

# while True:
#     thread = Thread(target=client_thread, args=(client,))
#     thread.start()
