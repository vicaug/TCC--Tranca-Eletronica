# -*- coding: utf-8 -*-

import socket
import thread
import sys
import traceback
import time

def saveInFile(toSave):
	
	file = open("Client.txt", "w");
	file.write(toSave);
	file.close();


def readFromFile():
	file = open("Client.txt", "r");
	print(file.read() );
	file.close();


#BEGIN CODE
option = "null";

while(option !=0):
	print("|-------------------------|");
	print("|	1 - Salvar        |");
	print("|	2 - Ler           |");
	print("|	3 - Transformar   |");
	print("|-------------------------|");

	option = input("Digite uma opção -> ");

	option = str(option);

	if(option == "1"): 
		nome_cliente = raw_input("Digite o nome do cliente a ser salvo na lista:\n");
		file = open("Client.txt","r");
		lista = file.read();

		if(lista == ""):
			saveInFile(nome_cliente);
			file.close();
		else:
			lista = lista+", "+nome_cliente;
			saveInFile(lista);
			file.close();

	elif(option == "2"):	
		readFromFile();

	elif(option == "3"):
		file = open("Client.txt", "r");
		lista = file.read();
		file.close();

		lista = lista.split(", ");
		
		i=1;
		for client in lista:
			client = str(i) +" - "+client;
			i = i+1; 
			print client;
		
	else:			
		print("Opção não válida !");

