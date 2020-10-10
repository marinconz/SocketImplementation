import socket 
import constants 

#Se crea el socket
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#Funcion Main
def main():
    print("===============================")
    print("Servidor corriendo...")
    print("IP Addr:",constants.SERVER_ADDRESS)
    print("Port:", constants.PORT)
    create_server_socket()

# Funcion para iniciar el proceso del servidor
def create_server_socket():
    tuple_connection = (constants.SERVER_ADDRESS, constants.PORT)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(tuple_connection)
    server_socket.listen(constants.BACKLOG)
    print('El Socket esta escuchando...', server_socket.getsockname())

    #Ciclo para crear nuevas conexiones
    client_connection, client_address = server_socket.accept()
    while True:
        data_received = client_connection.recv(constants.RECV_BUFFER_SIZE)
        remote_string = str(data_received.decode(constants.ENCODING_FORMAT))
        remote_command = remote_string.solit()
        command = remote_command[0]
        print(f'Data recibida de ' {client_address[0]}:{client_address[1]})
        print(command)
        if(command == constants.HELO):
            response = '100 OK\n'

