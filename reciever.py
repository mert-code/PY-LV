from time import sleep
import socket, json


# try to listen a port---------------------------------------------------------

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:

    try:
    
        server.bind(('localhost', 8088))
    
        print ("\nport is free now, listening...\n")

        break
        
    except OSError as err:

        if err.args[0] == 10048:    # OSError: Only one usage of each socket address (protocol/network address/port) is normally permitted

            print("\nwaiting port to be free...")
            
            sleep(3.5)


server.listen()

#-----------------------------------------------------------------------------
    
# read and print data--------------------

client, address = server.accept()
CostFunction = client.recv(1000)

jsonCostFunction=json.loads(CostFunction)
print(jsonCostFunction)


# send confirmation----------------------

item_count = len(jsonCostFunction)

confirmation = {'Client#': '2', 'Status': 'Sent', 'CostFunction': item_count}
confirmation_json = json.dumps(confirmation) 

client.send(confirmation_json.encode())       
client.send('\r\n'.encode())

#-----------------------------------------------------------------------------

server.close()