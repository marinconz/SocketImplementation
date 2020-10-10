import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 12345 

s.bind(('', port))         
print ("socket binded to %s" %(port) )
   
s.listen(5)      
print ("socket is listening")

while True: 
  
   # Establish connection with client. 
   c, addr = s.accept()      
   print ('Got connection from', addr )
  
   c.send(b'Thank you for connecting') 

   c.close() 

   