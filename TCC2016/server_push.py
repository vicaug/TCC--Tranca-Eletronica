# -*- coding: utf-8 -*-
import socket
import thread
import sys
import traceback

# Protocolos do servidor para o cliente:
# a,name              --> usuario "name" entrou na sala.
# b,name              --> usuario "name" saiu da sala.
# c,name,msg          --> usuario "name" mandou uma mensagem a todos na sala.
# d,name,msg          --> usuario "name" lhe mandou uma mensagem privada.
# f,user1,user2,user3 --> O servidor lhe mandou uma lista de usuarios conectados.
# e,msg               --> O servidor lhe mandou uma mensagem de controle.

# Protocolos do cliente para o servidor:

# Sua primeira mensagem ao servidor deve conter o seu RA. Ele
# serah considerado o seu login.

# c,msg --> Voce esta mandando uma mensagem para todos na sala.
# d,user,msg -->  Voce esta mandando uma mensagem para o um usuario apenas.


HOST = '192.168.1.100'
#HOST  = '192.168.0.110'     # Endereco IP do Servidor: Conectado ao
                             # android
#HOST = '177.220.20.159'
#HOST = '177.220.20.159'
                            
#HOST = '127.0.0.1'     # Endereco IP do Servidor

#HOST = '177.220.20.88' # Endereco IP do Servidor. Fornecido pela FT

PORT = 8888            # Porta que o Servidor esta

#CLIENTS = [None for i in range(1000)]
CLIENTS = {}
count=0
    
def find_slot() :
    for i in range(len(CLIENTS)) :
        if not CLIENTS[i] : 
            return i
    return -1
    
def send_broadcast_message(msg,  sender) :
    print("Broadcast: (%s) -> %s" % (sender, msg))
    global count
    count = count + 1
    print("vou entrar no for")
    for key in CLIENTS.keys() :
        print("key, sender", key, sender)
        try :
            if key != sender :
                CLIENTS[key].send("%s\t%s: %s \n" % (count, sender, msg))
        except  :
            traceback.print_exc()
            print("foi pro except")
            pass


def conectado(con, cliente):

    print("Aguardando nome")
    ## A primeira mensagem tem que ser um nome
    name = ""
    try :        
        name  = con.recv(1024).rstrip()
    except :
        pass

    print("Nome Obtido: %s" % name)
    
    if  name in CLIENTS :
        try :
            con.send ("O Seu nome de usuário já foi escolhido por outra pessoa \n")
            print("O Seu nome de usuário %s foi escolhido por outra pessoa \n" % name)
            con.close()
            thread.exit()
            return
        except :
            return       
    else :
        CLIENTS[name] = con
        sala = ",".join(CLIENTS.keys())

    while True :
        try :
            msg = con.recv(1024).rstrip()
            if not msg: break
            send_broadcast_message(msg, name) 
        except  :
            traceback.print_exc()

    if name in CLIENTS :
        del CLIENTS[name]
    
    print '----- Finalizando conexao do cliente', name

    try :
        con.close()
        thread.exit()
    except :
        pass




print("Listening")
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

orig = (HOST, PORT)
tcp.bind(orig)
tcp.listen(1)

while True :
    try :
        print("Entrando na Espera")
        con, cliente = tcp.accept()
        print("----------- Incoming Transmission")
        thread.start_new_thread(conectado, tuple([con, cliente]))
    except :
        pass

tcp.close()


