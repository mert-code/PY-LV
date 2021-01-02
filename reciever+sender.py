from time import sleep
import socket, random, json

#-----------------------------------------------------------------------------

print ("\n-------------------------------------------\n")

#-----------------------------------------------------------------------------

socket_reciever = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



# RECIEVER--------------------------------------------------------------------

# try to bind to a port-------------------------------------------------------

while True:

    try:
    
        socket_reciever.bind(('localhost', 8088))
        
        break
        
    except OSError as err:

        if err.args[0] == 10048:    # OSError: Only one usage of each socket address (protocol/network address/port) is normally permitted

            print("waiting for input-port to be free...\n")
            
            sleep(3.5)


socket_reciever.listen()
print ("input-port is ready now, listening...\n")
        
#-----------------------------------------------------------------------------
    
# read and print data--------------------

client, address = socket_reciever.accept()
cost_function_bytes = client.recv(10240)

cost_function_json=json.loads(cost_function_bytes)

print ("recieved data:\n")
print(cost_function_json)
print ("\n-------------------------------------------\n")


# send confirmation----------------------

item_count = len(cost_function_json)

confirmation_dict = {'Client#': '2', 'Status': 'Sent', 'CostFunction': item_count}
confirmation_json = json.dumps(confirmation_dict) 

client.send(confirmation_json.encode())       
client.send('\r\n'.encode())

#-----------------------------------------------------------------------------



# SENDER----------------------------------------------------------------------

# try to bind to a port-------------------------------------------------------


while True:

    try:
    
        socket_sender.bind(('localhost', 8089))
    
        break
        
    except OSError as err:

        if err.args[0] == 10048:    # OSError: Only one usage of each socket address (protocol/network address/port) is normally permitted

            print("\nwaiting for output-port to be free...")
            
            sleep(3.5)


socket_sender.listen()
print ("output-port is ready now.\n")

# generate and send data-------------------------------------------------------

# generate data------------------------

result = []
for i in range(0,random.randint(1,10)):        # choose the number of floating numbers to generate
    x = random.uniform(1, 200)
    result.append(x)
   
encodedResult = json.dumps(result).encode()   # encode parameter list to JSON

print("data to send:\n")
print(result)
print ("")
print("data sent.\n")

# send data----------------------------

client, address = socket_sender.accept()
client.send(encodedResult)                
client.send('\r\n'.encode())                  
 

# read confirmation from reciever.vi and print it-----------

msg = client.recv(10240)
msg_json=json.loads(msg)

print ("confirmation from reciever:\n")
print(msg_json)
print ("\n-------------------------------------------\n")
 
 
#-----------------------------------------------------------------------------

socket_reciever.close()
socket_sender.close()

