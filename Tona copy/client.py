import socket
import os
import time
   
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
def main():
  print('Client is running')
  clientSocket.connect(('127.0.0.1', 3000))
  localTouple = clientSocket.getsockname()
  print('Connected to the server from', localTouple)
  print('Enter quit to exit')
  print('Input commands')
  commandToSend = input()
 
  while commandToSend != 'quit':
    commands = commandToSend.split()
   
    if(commandToSend == ''):
      print('Please input a valid command')
      commandToSend = input()
    elif(commands[0] == 'upload'):
      if(not os.path.exists(commands[1])):
        print('File does not exist')
      else:
        file = open(commands[1], 'rb')
        length = os.path.getsize(commands[1])
        print(length)
        clientSocket.send(bytes(f'{commandToSend} {length}', 'utf-8'))
        time.sleep(1)
        stream = file.read(1024)
        while(stream):
          clientSocket.send(stream)
          stream = file.read(1024)
        file.close()
        dataReceived = clientSocket.recv(1024)
        print(dataReceived.decode('utf-8'))
        commandToSend = input()
 
    else:
      clientSocket.send(bytes(commandToSend, 'utf-8'))
      dataReceived = clientSocket.recv(1024)
      print(dataReceived.decode('utf-8'))
      commandToSend = input()
  clientSocket.send(bytes(commandToSend, 'utf-8'))
  dataReceived = clientSocket.recv(1024)
  print(dataReceived.decode('utf-8'))
  clientSocket.close()
 
 
if __name__ == "__main__":
   # execute only if run as a script
   main()