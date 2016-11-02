# -*- coding: utf-8 -*-
import socket
import thread
import sys

def listen_message(tcp):
    while True :
        msg = tcp.recv (1024);
        if not msg:
            sys.exit()
        print(msg)


HOST = sys.argv[1]
PORT = int(sys.argv[2])
        
#HOST  = '192.168.0.196'     # Endereco IP do Servidor        
#HOST = '127.0.0.1'     # Endereco IP do Servidor
#PORT = 8080            # Porta que o Servidor esta


#HOST  = '192.168.43.59'     # Endereco IP do Servidor
#PORT = 8080            # Porta que o Servidor esta


print(HOST, PORT)

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)
tcp.connect(dest)

thread.start_new_thread(listen_message, tuple([tcp]))

print 'Para sair use CTRL+X\n'
msg = raw_input()

try :
    while msg <> '\x18':
        tcp.send (msg)
        msg = raw_input()
except :
    pass
tcp.close()



# Open /etc/pf.conf in a text editor.
# Add a line like this:

# # Open port 8080 for TCP on all interfaces
# pass in proto tcp from any to any port 8080

# Save the file.
# Load the changes (and test them) with:

# sudo pfctl -vnf /etc/pf.conf

# Reboot
