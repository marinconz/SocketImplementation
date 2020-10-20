import socket
import sys
import os
from _thread import *
import threading

print_lock = threading.Lock() 
 
DEFAUlT_BUCKET_PATH = './Buckets'
 
path = None
print(str(sys.argv))
 
def checkPath(dir):
   if(not os.path.isdir(dir)):
      os.mkdir(dir)
      return('Creacion exitosa')
   else:
      return('El directorio ya existe')
 
#Verificar existencia de directorio por argumentos, si es invalido se usa el default
if(len(sys.argv) > 1):
   if(os.path.isdir(sys.argv[1])):
      path = sys.argv[1]
   else:
      checkPath(DEFAUlT_BUCKET_PATH)
      path = DEFAUlT_BUCKET_PATH
#Verificar existencia del directorio por defecto
else:
   print('No se especifico la ruta del directorio. Se usara una ruta por defecto')
   checkPath(DEFAUlT_BUCKET_PATH)
   path = DEFAUlT_BUCKET_PATH



 
# Funcion Main
def Main():
   print("===============================")
   print("Servidor corriendo...")
   tuple_connection = ('127.0.0.1', 3000)
   server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   server_socket.bind(tuple_connection)
   server_socket.listen(5)
   print('El Socket esta escuchando...', server_socket.getsockname())

   # Ciclo para crear nuevas conexiones
   while True:
      client_connection, client_address = server_socket.accept()  
      print(f'Nueva conexion detectada', client_address)
      print_lock.acquire()

      create_server_socket(client_connection, client_address)
 
# Funcion para iniciar el proceso del servidor
def create_server_socket(client_connection, client_address):
   
   while True:
      data_received = client_connection.recv(1024)
      remote_string = str(data_received.decode(
         'utf-8'))
      remote_command = remote_string.split()
      print('comando principal: ', remote_command)
      if(len(remote_command) > 1):
         pathWithParam = f'{path}/{remote_command[1]}'
      command = remote_command[0]
      print(f'Data recibida de {client_address[0]}:{client_address[1]}')
 
      #Manejo de variables con y sin parametro extra
      if(command == 'ls' and len(remote_command) == 1):
         response = '\n'.join(os.listdir(path))
         client_connection.sendall(response.encode('utf-8'))
      elif(command == 'ls'):
         try:
            response = ''.join(os.listdir(pathWithParam))
         except OSError:
            response = 'The provided bucket does not exist'
         if(response == ''):
            response = 'The selected bucket is empty'
         client_connection.sendall(response.encode('utf-8'))
      elif(command == 'mkbkt'):
         response = checkPath(pathWithParam)
         client_connection.sendall(response.encode('utf-8'))
      elif(command == 'rm' and len(remote_command) == 2):
         try:
            os.rmdir(pathWithParam)
         except OSError:
            response = 'Deletion of the Bucket has failed'
         else:
            response = 'Successfully deleted the bucket'
         client_connection.sendall(response.encode('utf-8'))
      elif(command == 'rm' and len(remote_command) == 3):
         if(not os.path.exists(f'{pathWithParam}/{remote_command[2]}')):
            response = 'The file does not exist'
         else:
            os.remove(f'{pathWithParam}/{remote_command[2]}')
            response = 'File has been deleted successfully'
         client_connection.sendall(response.encode('utf-8'))
      elif(command == 'upload'):
         print(remote_command)
         remotePath = remote_command[1].split('/')
         fileName = remotePath[len(remotePath) - 1]
         print(fileName)
         file = open(f'{path}/{remote_command[2]}/{fileName}', 'wb')
         stream = client_connection.recv(1024)
         while(True):
            file.write(stream)
            if(file.tell() == int(remote_command[3])):
               break
            stream = client_connection.recv(1024)
         file.close()
         response = 'File transferred successfully'
         client_connection.sendall(response.encode('utf-8'))
      elif (command == 'quit'):
         response = 'Connection terminated'
         client_connection.sendall(response.encode('utf-8'))
         print_lock.release() 
         break
 
         
   print(f'Client {client_address[0]}:{client_address[1]} disconnected')
   client_connection.close()
 
if __name__ == "__main__":
   # execute only if run as a script
   Main()