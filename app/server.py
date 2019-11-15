#!/usr/bin/env python

import socket, random

def atualizaPreco():
	#para todas as empresas do indice
	precoPSI20 = 0
	for emp in PSI20:
		emp.precoAtual = round(random.uniform((emp.precoAbertura*0.9), (emp.precoAbertura*1.10)), 4)
		emp.log.write(str(emp.precoAtual) + '\n')
		precoPSI20 += round((emp.precoAtual)*(emp.peso), 4)
	logPSI20.write(str(precoPSI20) + '\n')	
		
class Empresa:
	def __init__(self, nome, nAccoes, preco, peso):
		self.nome = nome
		self.nAccoes = nAccoes
		self.precoAbertura = preco
		self.precoAtual = self.precoAbertura
		self.variacao = ((self.precoAbertura - self.precoAtual)/abs(self.precoAbertura))*100
		self.log = open("%s.txt" % nome, "w")
		self.peso = peso/100

PSI20 = [Empresa('Altri', 234000, 6, 2.03), Empresa('BCP', 46000000, 0.3, 17.04), Empresa('Corticeira Amorim', 39000, 11, 2.62), Empresa('CTT', 1000000, 3, 3.02), Empresa('EDP', 200000, 7, 9.69), Empresa('Energias de Portugal', 9000000, 3, 10.36), Empresa('F.Rama', 21000, 12, 0.24), Empresa('Galp', 2000000, 17, 11.5), Empresa('Ibersol', 2000, 11, 0.93), Empresa('Jeronimo Martins', 607000, 13, 10.55), Empresa('Mota-Engil', 432000, 3, 2.22), Empresa('NOS', 1800000, 4, 9.01), Empresa('Pharol',2000000, 0.3, 0.93), Empresa('REN', 1000000, 2, 4.75), Empresa('Semapa', 14000, 19, 2.77), Empresa('Sonae', 1600000, 1, 5.03), Empresa('Sonae Capital', 400000, 1, 0.5), Empresa('The Navigator Co', 463000,4, 6.81)]

logPSI20 = open("PSI20.txt", "w")

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('127.0.0.1', 2222))
serverSocket.listen(10)

while True:
	#atualiza o preco da accao de todas as empresas
	atualizaPreco()
	
	#aceita a ligacao com o cliente
	link, addr = serverSocket.accept()
	
	#recebe mensagem do cliente
	msg = link.recv(2048)
	
	#server recebe 2 tipos de mensagens com formato:
	#info/*empresa*
	#ordem/*empresa*/*volume*/*accao*/*cliente*
	
	#descodifica a mensagem
	msg = msg.split('/')
	tipo = msg[0]
	empresa = int(msg[1])
	
	#mensagem a pedir informacao da empresa
	if tipo == 'info':
		#envia a informacao
		link.send(str(PSI20[empresa].nAccoes))
	#mensagem a dar uma ordem	
	elif tipo == 'ordem':
		volume = int(msg[2])
		accao = int(msg[3])
		cliente = int(msg[4])
		#ordem de compra
		if accao == 1:
			#retira a empresa o num de shares que o cliente quer comprar
			PSI20[empresa].nAccoes -= volume
			#codifica uma mensagem para enviar ao cliente com o num da empresa e o num de shares compradas (empresa/nAccoes)
			confirmacao = str(empresa) + '/' + str(volume) 
			print str(volume) + ' - ' + str(PSI20[empresa].precoAtual) + ' - ' + PSI20[empresa].nome + ' - buy - ' + str(cliente)	
			#envia essa msg			
			link.send(confirmacao)
		#ordem de venda	
		elif accao == 2:
			#adiciona a empresa o num de shares que o cliente quer vender
			PSI20[empresa].nAccoes += volume
			#codifica uma mensagem para enviar ao cliente com o num da empresa e o num de shares vendidas (empresa/nAccoes)
			confirmacao = str(empresa) + '/' + str(volume)
			print str(volume) + ' - ' + str(PSI20[empresa].precoAtual) + ' - ' + PSI20[empresa].nome + ' - sell - ' + str(cliente)	
			#envia essa msg
			link.send(confirmacao)
			
link.close()	
logPSI20.close()	