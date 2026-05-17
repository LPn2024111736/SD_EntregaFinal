import threading
from dados.enums.direcao import Direcao
import Servidor
import json
from time import sleep
import os

class ProcessaCliente(threading.Thread):
    """
    Classe ProcessaCliente:
    Classe utilizada para gerir cada cliente. Utiliza a informação presente na máquina para os clientes a partilharem.
    :param connection: permite conecção entre o servidor e cliente
    :param address: endereço do cliente
    :param dados: o mesmo gestor de dados utilizado pela maquina
    :param clientes: a lista de clientes atual a utilizar as threads
    :param mapa: mapa do jogo, vindo da maquina
    :param jogador1: jogador 1, vindo da maquina
    :param jogador2: jogador 2, vindo da maquina
    """
    def __init__(self, connection, address, dados, clientes, mapa, jogador1, jogador2):
        super().__init__()
        self.connection = connection
        self.address = address
        self.dados = dados
        self.clientes = clientes
        self.mapa = mapa
        self.jogador1 = jogador1
        self.jogador2 = jogador2
        self.udp_port = None


    def receive_int(self, connection, n_bytes):
        data = connection.recv(n_bytes)
        return int.from_bytes(data, byteorder='big', signed=True)

    def send_int(self, connection, value, n_bytes):
        connection.send(value.to_bytes(n_bytes, byteorder="big", signed=True))

    def receive_str(self, connection, n_bytes):
        data = connection.recv(n_bytes)
        return data.decode()

    def send_str(self, connection, value):
        connection.send(value.encode())

    def receive_object(self, connection):
        try:
            size = self.receive_int(connection, Servidor.INT_SIZE)
            data = b""
            while len(data) < size:
                packet = connection.recv(size - len(data))
                if not packet:
                    raise ConnectionError("Ligação perdida")
                data += packet
            return json.loads(data.decode('utf-8'))
        except (MemoryError):
            print("PORRA")

    def send_object(self, connection, obj):
        data = json.dumps(obj).encode('utf-8')
        size = len(data)
        self.send_int(connection, size, Servidor.INT_SIZE)
        connection.sendall(data)

    def run(self):
        """
        enquanto a variavel last_request não for verdadeira, a thread irá  eceber uma mensagem do cliente, identificado
        pelo endereço, a indicar a funcao que deseja. Estas incluiem a operação de início de jogo, de movimento, de
        interação e de conecção do socket udp do cliente.
        """
        print(self.address, "Thread iniciada")
        last_request = False
        while not last_request:
            request_type = self.receive_str(self.connection, Servidor.COMMAND_SIZE)
            if request_type == Servidor.UDP_PORT:
                self.udp_port = self.receive_int(self.connection, Servidor.INT_SIZE)
                print(f"[{self.address}] Porto UDP do cliente recebido: {self.udp_port}")
                self.clientes.connetar(cliente=[self.address, self.connection, self.udp_port])
            isPlayer1 = self.clientes.clientes[0][0] == self.address
            if isPlayer1:
                jogador=self.jogador1
            else:
                jogador=self.jogador2
            if request_type == Servidor.START:
                if jogador.pronto == 1:
                    jogador.pronto = 0
                elif jogador.pronto ==0:
                    jogador.pronto= 1
            if self.jogador1.pronto == 1 and self.jogador2.pronto == 1:
                if request_type == Servidor.UP:
                    self.mapa.move(jogador, Direcao.UP)
                    coords= str(jogador.getPosX()+1) + ","+ str(jogador.getPosY()+1)
                    self.dados.registar_oper(jogador.pID,"Movimento","Cima",coords,self.address)
                elif request_type == Servidor.DOWN:
                    self.mapa.move(jogador, Direcao.DOWN)
                    coords = str(jogador.getPosX()+1) + "," + str(jogador.getPosY()+1)
                    self.dados.registar_oper(jogador.pID,"Movimento", "Baixo", coords, self.address)
                elif request_type == Servidor.LEFT:
                    self.mapa.move(jogador, Direcao.LEFT)
                    coords = str(jogador.getPosX()+1) + "," + str(jogador.getPosY()+1)
                    self.dados.registar_oper(jogador.pID,"Movimento", "Esquerda", coords, self.address)
                elif request_type == Servidor.RIGHT:
                    coords= str(jogador.getPosX()+1) + ","+ str(jogador.getPosY()+1)
                    self.dados.registar_oper(jogador.pID,"Movimento","Direita",coords,self.address)
                    self.mapa.move(jogador, Direcao.RIGHT)
                elif request_type == Servidor.INTERACT:
                    point=self.mapa.interact(jogador)
                    if point:
                        self.dados.registar_oper(jogador.pID,"Interacao","Pontuacao", jogador.pontuacao, self.address)
                    else:
                        self.dados.registar_oper(jogador.pID,"Interacao","Interacao Normal", str(jogador.objeto),self.address)

                if self.jogador1.pontuacao >= 10 or self.jogador2.pontuacao >= 10:
                    vencedor = self.jogador1 if self.jogador1.pontuacao >= 10 else self.jogador2
                    self.jogador1.pronto = 2
                    self.jogador2.pronto = 2
                    print(f"Jogo terminado! Jogador {vencedor.pID} atingiu pontuacao {vencedor.pontuacao}. A fechar servidor...")
                    last_request = True
        with open("dados.json", "w") as f:
            json.dump(self.dados.operacoes,f)
        sleep(0.2)
        self.connection.close()
        print(self.address, "Ligacao fechada")
        os._exit(0)