#!/usr/bin/env python

import socket, random, time, os

PSI20 = ['Altri', 'BCP', 'Corticeira Amorim', 'CTT', 'EDP', 'Energias de Portugal', 'F.Rama', 'Galp', 'Ibersol', 'Jeronimo Martins', 'Mota-Engil', 'NOS', 'Pharol', 'REN', 'Semapa', 'Sonae', 'Sonae Capital', 'The Navigator Co']

def comunicaServer(msg):
	#cria uma socket
	socketCliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#liga a socket ao server
	socketCliente.connect(('127.0.0.1', 2222))
	#envia uma string ao server
	socketCliente.send(msg)
	#recebe uma resposta do server
	resposta = socketCliente.recv(2048)
	#fecha a socket
	socketCliente.close()
	return resposta

def compra():
	#escolhe aleatoriamente de que empresa vai comprar uma accao
	empresa = random.randint(0, 17)
	#codifica uma mensagem para mandar ao server a perguntar quantas shares da empresa escolhida estao disponiveis para compra
	info = 'info/' + str(empresa)
	#recebe a informacao do server
	nAccoes = round(int(comunicaServer(info))*0.1, 0)
	#escolhe ao acaso o num de shares a comprar
	volume = random.randint(1, nAccoes)
	#codifica uma ordem de compra
	ordem = 'ordem/%i/%i/%i/%i' % (empresa, volume, accao, cliente)
	#recebe a confirmacao de compra do server
	confirmacao = comunicaServer(ordem)  
	#guarda a compra no portfolio
	portfolio.append(confirmacao)
	confirmacao = confirmacao.split('/')
	print 'buy\t-\t' + confirmacao[1] + '\t-\t' + PSI20[int(confirmacao[0])] 
	
def vende():
	tamanhoPortfolio = len(portfolio)-1
	#se existirem posicoes no portfolio
	if tamanhoPortfolio >= 0:
		#escolhe uma posicao ao acaso
		index = random.randint(0, tamanhoPortfolio)
		#codifica uma ordem para vender
		ordem = 'ordem/' + portfolio[index] + '/2/%i' % (cliente) 
		#recebe uma confirmacao de venda do server
		confirmacao = comunicaServer(ordem)
		confirmacao = confirmacao.split('/')
		print 'sell\t-\t' + confirmacao[1] + '\t-\t' + PSI20[int(confirmacao[0])]
		#apanha essa posicao do portfolio
		del portfolio[index]

#atribui uma identidade ao trader		
cliente	= os.getpid()	

portfolio = [] #[empresa/volume, empresa/volume, ...]

while True:
	#escolhe aleatoriamente o que vai fazer
	accao = random.randint(0, 2)
	#0 = neutro
	#1 = compra
	#2 = vende
	
	if accao == 1:
		compra()
	elif accao == 2:
		vende()
	else:
		print 'neutro'
	time.sleep(1)
