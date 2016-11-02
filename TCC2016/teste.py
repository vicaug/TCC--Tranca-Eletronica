# -*- coding: utf-8 -*-
#!/usr/bin/env python
import socket
import thread
import sys
import traceback
import time

HOST = '192.168.0.10'  # Endereco IP do Servidor: Conectado ao
PORT = 8888            # Porta que o Servidor esta

#CLIENTS = [None for i in range(1000)]
CLIENTS = {}
count=0

def pins_export():
        pin1export = open("/sys/class/gpio/export","w")
        pin1export.write("24")

        fp1 = open("/sys/class/gpio/gpio21/direction","w")
        fp1.write("out")
        fp1.close()

        pin2export = open("/sys/class/gpio/export","w")
        pin2export.write("39")

        fp3 = open("/sys/class/gpio/gpio39/direction","w")
        fp3.write("out")
        fp3.close()

def write_led(value):
        fp2 = open("/sys/class/gpio/gpio21/value","w")
        fp2.write(str(value))
        fp2.close()

def write_led2(value):
        fp4 = open("sys/class/gpio/gpio39/value","w")
        fp4.write(str(value))
        fp4.close()
    
def find_slot() :
    for i in range(len(CLIENTS)) :
        if not CLIENTS[i] : 
            return i
    return -1
    
def send_broadcast_message(msg,  sender) :
    print("Broadcast: (%s) -> %s" % (sender, msg))
    pins_export()

    if (msg == "ROLALiga"):
        print("Liguei a ROLA")
        write_led(1)
        time.sleep(2)
    if(msg == "ROLADesliga"):
        print("Desliguei a ROLA")
        write_led(0)
	time.sleep(2)
    if(msg =="MSGTROLALiga"):
    	print("Liguei a ROLA")
	write_led(1)
	time.sleep(2)
    if(msg == "MSGTROLADesliga"):
	print("Desliguei a ROLA")
	write_led(0)
	time.sleep(2)

    global count
    count = count + 1
    #print("vou entrar no for")
    for key in CLIENTS.keys() :
        #print("key, sender", key, sender)
        try :
            if key != sender :
                CLIENTS[key].send("%s\t%s: %s \n" % (count, sender, msg))
        except  :
            traceback.print_exc()
            #print("foi pro except")
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
