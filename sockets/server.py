#importar la libreria de sockets
import socket
import sys
import os
import time
#importar Hilos
import threading 

 
DEFAUlT_BUCKET_PATH = './Buckets'

path = None
print(str(sys.argv))

# Funcion Main
def Main():
   print("===============================")
   print("Server is running...")
   serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
   tuppleConnection = ('127.0.0.1', 3000)
   serverSocket.bind(tuppleConnection)
   # Ciclo para crear nuevas conexiones
   while True:
      serverSocket.listen(1)
      print('Socket is listening...', serverSocket.getsockname())
      #Establecer conexion con el cliente
      clientConnection, clientAddress = serverSocket.accept()
      # Empezar un nuevo hilo
      nuevo_cliente=ClientThread(clientConnection,clientAddress)
      nuevo_cliente.start()

   serverSocket.close()

class ClientThread(threading.Thread):
   def __init__(self,clientConnection,clientAddress):
      threading.Thread.__init__(self)
      self.csocket = clientConnection
      self.address = clientAddress
      print ("New connection added: ", clientAddress)

   def run(self):
      print ("Connection from : ", self.address)
      #self.csocket.send(bytes("Hi, This is from Server..",'utf-8'))
      while True:
         dataRecieved = self.csocket.recv(1024)
         remoteString = str(dataRecieved.decode(
            'utf-8'))
         remoteCommand = remoteString.split()
         print('Command received: ', remoteCommand)
         if(len(remoteCommand) > 1):
            pathWithParam = f'{path}/{remoteCommand[1]}'
         command = remoteCommand[0]
         print(f'Data recieved from: {self.address[0]}:{self.address[1]}')

         #Manejo de variables con y sin parametro extra

         #comando para listar los directorios
         if(command == 'ls' and len(remoteCommand) == 1):
            response = '\n'.join(os.listdir(path))
            self.csocket.sendall(response.encode('utf-8'))
         #comando para listar los archivos de un directorio en especifico
         elif(command == 'ls'):
            try:
               response = ''.join(os.listdir(pathWithParam))
            except OSError:
               response = 'The provided bucket does not exist'
            if(response == ''):
               response = 'The selected bucket is empty'
            self.csocket.sendall(response.encode('utf-8'))
         #comando para crear un nuevo directorio
         elif(command == 'mkbkt'):
            response = checkPath(pathWithParam)
            self.csocket.sendall(response.encode('utf-8'))
         elif(command == 'rm' and len(remoteCommand) == 2):
            try:
               os.rmdir(pathWithParam)
            except OSError:
               response = 'Deletion of the Bucket has failed'
            else:
               response = 'Successfully deleted the bucket'
            self.csocket.sendall(response.encode('utf-8'))
         #comando para eliminar un directorio  
         elif(command == 'rm' and len(remoteCommand) == 3):
            if(not os.path.exists(f'{pathWithParam}/{remoteCommand[2]}')):
               response = 'The file does not exist'
            else:
               os.remove(f'{pathWithParam}/{remoteCommand[2]}')
               response = 'File has been deleted successfully'
            self.csocket.sendall(response.encode('utf-8'))
         #comando para subir un archivo al servidor (parte servidor)
         elif(command == 'upload' and len(remoteCommand) == 4):
            print(remoteCommand[1])
            remotePath = remoteCommand[1].split('/')
            print(remotePath)
            fileName = remotePath[len(remotePath) - 1]
            print('FIle name is: ', fileName)
            file = open(f'{path}/{remoteCommand[2]}/{fileName}', 'wb')
            stream = self.csocket.recv(1024)
            while(True):
               file.write(stream)
               if(file.tell() == int(remoteCommand[3])):
                  break
               stream = self.csocket.recv(1024)
            file.close()
            response = 'File transferred successfully'
            self.csocket.sendall(response.encode('utf-8'))
         #comando para descargar un archivo de un directorio (parte servidor)
         elif(command == 'download' and len(remoteCommand) == 3):               
            downoladFile = f'{DEFAUlT_BUCKET_PATH}/{remoteCommand[1]}/{remoteCommand[2]}'
            try:
               file = open(downoladFile, 'rb')
            except:
               response = 'Bucket and file combination does not exist'
               self.csocket.sendall(response.encode('utf-8'))
            else:   
               length = os.path.getsize(downoladFile)
               print('File Length is: ',length)
               self.csocket.sendall(bytes(str(length), 'utf-8'))
               time.sleep(1)
               stream = file.read(1024)
               while (stream):
                  self.csocket.sendall(stream)
                  stream = file.read(1024)
               file.close()
               response = 'File downloaded successfully'
               self.csocket.sendall(response.encode('utf-8'))
         #comando para finalizar la conexión
         elif (command == 'quit'):
            response = 'Connection terminated'
            self.csocket.sendall(response.encode('utf-8'))
            break
         else:
            response = '''Invalid Command, please insert one of the following: 
   - Create bucket `mkbkt bucketName` 
   - Remove bucket `rm bucketName`
   - List buckets `ls`
   - Listfiles from bucket `ls bucketName`
   - Upload files from client to a server bucket `upload fileName bucketName` or `upload filePath bucketName`
   - Download file from server buckt to client `download bucketName fileName`
   - Remove file from bucket `rm bucketName FileName`'''
            self.csocket.sendall(response.encode('utf-8'))
 
         
      print(f'Client {self.address[0]}:{self.address[1]} disconnected')

def checkPath(dir):
   if(not os.path.isdir(dir)):
      os.mkdir(dir)
      return('Creation was successful')
   else:
      return('Directory already exists')
 
#Verificar existencia de directorio por argumentos, si es invalido se usa el default
if(len(sys.argv) > 1):
   if(os.path.isdir(sys.argv[1])):
      path = sys.argv[1]
   else:
      checkPath(DEFAUlT_BUCKET_PATH)
      path = DEFAUlT_BUCKET_PATH
#Verificar existencia del directorio por defecto
else:
   print('Rute was not specified. A default one will be used')
   checkPath(DEFAUlT_BUCKET_PATH)
   path = DEFAUlT_BUCKET_PATH
 
 
 
if __name__ == "__main__":
   Main()