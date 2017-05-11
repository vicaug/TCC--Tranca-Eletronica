#! /usr/bin/env python
# -*- coding:utf-8 -*-

#switch em python usando dicionários e funções

#Define as funções
def case_1():
    print 'Numero 1'
def case_2():
    print 'Numero 2'
def case_3():
    print 'Numero 3'
def case_default():
    print 'Numero fora do intervalo'

#cria um dicionário que relaciona cada função com a opção desejada
dict = {1 : case_1, 2 : case_2, 3 : case_3}

def switch(x):
'''
Função que implementa um switch
usando funções e um dicionário
'''
   try:
     dict[x]()
    except:
        case_default()
     
try:
    switch(input('Digite o valor desejado'))
except:
   print 'O valor digitado não é um número'