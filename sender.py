from time import sleep
import socket, random, json


# try to listen a port---------------------------------------------------------

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:

    try:
    
        server.bind(('localhost', 8089))
    
        print ("\nport is free now, listening...\n")

        break
        
    except OSError as err:

        if err.args[0] == 10048:    # OSError: Only one usage of each socket address (protocol/network address/port) is normally permitted

            print("\nwaiting port to be free...")
            
            sleep(3.5)


server.listen(1)

# generate and send data-------------------------------------------------------

# generate data------------------------

result = []
for i in range(0,random.randint(1,10)):        # choose the number of floating numbers to generate
    x = random.uniform(1, 200)
    result.append(x)
   
encodedResult = json.dumps(result).encode()   # encode parameter list to JSON
print(result)
 

# send data----------------------------

client, address = server.accept()
client.send(encodedResult)                
client.send('\r\n'.encode())                  
 

# read confirmation from reciever.vi and print it-----------

msg = client.recv(1000)

jsonMsg=json.loads(msg)
print(jsonMsg)
print(jsonMsg['Client#'], jsonMsg['Status'], jsonMsg['VarFunction'])
 
 
#-----------------------------------------------------------------------------

server.close()