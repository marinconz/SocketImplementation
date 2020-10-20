import socket
import os
import time


DEFAULT_DOWNLOAD_PATH = './Downloads'

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def checkPath(dir):
   if(not os.path.isdir(dir)):
      os.mkdir(dir)
      return('Creacion exitosa')
   else:
      return('El directorio ya existe')
 
def Main():
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
      print(commands)
      if(not os.path.exists(commands[1])):
        print('File does not exist')
      else:
        file = open(commands[1], 'rb')
        length = os.path.getsize(commands[1])
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
    elif(commands[0] == 'download'):
      print(commands)
      checkPath(DEFAULT_DOWNLOAD_PATH)
      clientSocket.send(bytes(commandToSend, 'utf-8'))
      length = clientSocket.recv(1024)
      remoteString = str(length.decode('utf-8'))
      if(remoteString.isdigit()): 
        file = open(f'{DEFAULT_DOWNLOAD_PATH}/{commands[2]}', 'wb')
        stream = clientSocket.recv(1024)
        while(True):
          file.write(stream)
          if(file.tell()==int(remoteString)):
            break
          stream = clientSocket.recv(1024)
        file.close()
        dataReceived = clientSocket.recv(1024)
        print(dataReceived.decode('utf-8'))
      else:
        print(remoteString)
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
   Main()