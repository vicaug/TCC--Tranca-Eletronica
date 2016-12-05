# -*- coding: utf-8 -*-
#!/usr/bin/env python
import socket
import thread
import sys
import traceback
import time

from wiringx86 import GPIOGalileoGen2 as GPIO

HOST = '192.168.0.2'
#HOST = '177.220.92.156'  # Endereco IP do Servidor: Conectado ao
PORT = 8888            # Porta que o Servidor esta

#CLIENTS = [None for i in range(1000)]
CLIENTS = {}
count=0
Arg1 = ""
Arg2 = ""


def pins_export(msg_porta, mgs_type):

        concat = ("/gpio"+msg_porta)

        pin1export = open("/sys/class/gpio/export","w")
        pin1export.write(str(msg_porta))

        fp1 = open("/sys/class/gpio"+ concat+ "/direction","w")
        #fp1 = open(str(concat))
        #fp1 = open("/direction","w")

        fp1.write(str(mgs_type))
        fp1.close()

def identity_msg_IO(msg):
    if (msg == "temp"):
        temp_command()
        return 0
    else:
        string_split(msg)

def temp_command():
	gpio = GPIO(debug=False)
	analogpin = 14

	gpio.pinMode(analogpin, gpio.ANALOG_INPUT)

	print 'Analog reading from pin %d now...' % analogpin
	try:
    		count = 0
    		while(count < 5):
        		# Read the voltage on pin 14
        		value = gpio.analogRead(analogpin)

    			tempc = (5.0 * value * 100.0)
    			tempc = tempc / 1024
    			value = tempc

        		print 'Leitura: %.2f  celsius'   % value
        		time.sleep(0.5)
        		count = count + 1

	# When you get tired of seeing the led blinking kill the loop with Ctrl-C.
	except KeyboardInterrupt:
    	
    		print '\nCleaning up...'
    	# Do 
    		gpio.cleanup()       

def write_function(value, msg_porta):

	concat = ("/gpio"+msg_porta)

        fp2 = open("/sys/class/gpio"+ concat+ "/value","w")
        #fp2 = open(str(concat))
        #fp2 = open("/value","w")

        fp2.write(str(value))
        fp2.close()
    
def find_slot() :
    for i in range(len(CLIENTS)) :
        if not CLIENTS[i] : 
            return i
    return -1

def string_split(msg):
    msg.split("-")
    msg_comando, msg_porta, mgs_type = msg.split("-")
    pins_export(msg_porta, mgs_type)
    verificar_comando(msg_comando, msg_porta)

def verificar_comando(msg_comando, msg_porta):
    global temp_value
    if (msg_comando == "Ligar"):
        print("Liguei a luz teste")
        write_function(1, msg_porta)
        time.sleep(2)
        return 0
    if(msg_comando == "Desligar"):
        #print("Desliguei a luz")
        write_function(0, msg_porta)
	time.sleep(2)
	return 1

    if(msg_comando == "Atualizar"):
        temp_value = analogRead(msg_porta); 
        return 2


def send_broadcast_message(msg, sender) :
    print("Broadcast: (%s) -> %s" % (sender, msg))

    #string_split(msg)
    identity_msg_IO(msg)


    if(verificar_comando == 0):
    	print("Liguei a luz")

    if(verificar_comando == 1):
    	print("Desliguei a luz")

    if(verificar_comando == 2):
        print(str(temp_value))

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
