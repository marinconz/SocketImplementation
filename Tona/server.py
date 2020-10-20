import socket
import sys
import os
import time
 
DEFAUlT_BUCKET_PATH = './Buckets'
 
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
path = None
print(str(sys.argv))
 
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
 
 
# Funcion Main
def main():
   print("===============================")
   print("Server is running...")
   createServerSocket()
 
# Funcion para iniciar el proceso del servidor
def createServerSocket():
   tuppleConnection = ('127.0.0.1', 3000)
   serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
   serverSocket.bind(tuppleConnection)
   serverSocket.listen(5)
   print('Soket is listening...', serverSocket.getsockname())
 
   # Ciclo para crear nuevas conexiones
   while True:
      clientConnection, clientAddress = serverSocket.accept()
      print(f'New connection detected', clientAddress)
      while True:
         dataRecieved = clientConnection.recv(1024)
         remoteString = str(dataRecieved.decode(
            'utf-8'))
         remoteCommand = remoteString.split()
         print('Command received: ', remoteCommand)
         if(len(remoteCommand) > 1):
            pathWithParam = f'{path}/{remoteCommand[1]}'
         command = remoteCommand[0]
         print(f'Data recieved from: {clientAddress[0]}:{clientAddress[1]}')
 
         #Manejo de variables con y sin parametro extra
         if(command == 'ls' and len(remoteCommand) == 1):
            response = '\n'.join(os.listdir(path))
            clientConnection.sendall(response.encode('utf-8'))
         elif(command == 'ls'):
            try:
               response = ''.join(os.listdir(pathWithParam))
            except OSError:
               response = 'The provided bucket does not exist'
            if(response == ''):
               response = 'The selected bucket is empty'
            clientConnection.sendall(response.encode('utf-8'))
         elif(command == 'mkbkt'):
            response = checkPath(pathWithParam)
            clientConnection.sendall(response.encode('utf-8'))
         elif(command == 'rm' and len(remoteCommand) == 2):
            try:
               os.rmdir(pathWithParam)
            except OSError:
               response = 'Deletion of the Bucket has failed'
            else:
               response = 'Successfully deleted the bucket'
            clientConnection.sendall(response.encode('utf-8'))
         elif(command == 'rm' and len(remoteCommand) == 3):
            if(not os.path.exists(f'{pathWithParam}/{remoteCommand[2]}')):
               response = 'The file does not exist'
            else:
               os.remove(f'{pathWithParam}/{remoteCommand[2]}')
               response = 'File has been deleted successfully'
            clientConnection.sendall(response.encode('utf-8'))
         elif(command == 'upload' and len(remoteCommand) == 3):
            remotePath = remoteCommand[1].split('/')
            fileName = remotePath[len(remotePath) - 1]
            print('FIle name is: ', fileName)
            file = open(f'{path}/{remoteCommand[2]}/{fileName}', 'wb')
            stream = clientConnection.recv(1024)
            while(True):
               file.write(stream)
               if(file.tell() == int(remoteCommand[3])):
                  break
               stream = clientConnection.recv(1024)
            file.close()
            response = 'File transferred successfully'
            clientConnection.sendall(response.encode('utf-8'))
         elif(command == 'download' and len(remoteCommand) == 3):               
            downoladFile = f'{DEFAUlT_BUCKET_PATH}/{remoteCommand[1]}/{remoteCommand[2]}'
            try:
               file = open(downoladFile, 'rb')
            except:
               response = 'Bucket and file combination does not exist'
               clientConnection.sendall(response.encode('utf-8'))
            else:   
               length = os.path.getsize(downoladFile)
               print('File Length is: ',length)
               clientConnection.sendall(bytes(str(length), 'utf-8'))
               time.sleep(1)
               stream = file.read(1024)
               while (stream):
                  clientConnection.sendall(stream)
                  stream = file.read(1024)
               file.close()
               response = 'File downloaded successfully'
               clientConnection.sendall(response.encode('utf-8'))
         elif (command == 'quit'):
            response = 'Connection terminated'
            clientConnection.sendall(response.encode('utf-8'))
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
            clientConnection.sendall(response.encode('utf-8'))
 
         
      print(f'Client {clientAddress[0]}:{clientAddress[1]} disconnected')
      clientConnection.close()
 
if __name__ == "__main__":
   main()