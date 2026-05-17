# thread_broadcast.py
import Servidor
import threading
import time
import json
from typing import Dict
from dados.classes.mapa import Mapa
from Servidor.Maquina.lista_clientes import ListaClientes
from dados.classes.jogador import Jogador

import socket

class ThreadBroadcast(threading.Thread):
    """Classe ThreadBroadcast
    Envia o estado do jogo para o BroadcastEmissor, através do socket udp dos clientes.
    :param: lista_clientes - lista de clientes.
    :param: mapa - mapa do jogo (vindo da máquina)
    :param: jogador 1 - primeiro jogador (vindo da máquina)
    :param: jogador 2 - segundo jogador (vindo da máquina)
    :param: intervalo - tempo entre broadcasts (0.01 para garantir que o estado do jogo é atualizado com mais frequencia do que a framerate
    :param: runnning - se o broadcast está a correr
    :param: udp_socket - socket do broadcast"""
    def __init__(self, lista_clientes: ListaClientes, mapa:Mapa, jogador1:Jogador,jogador2:Jogador, intervalo: float = 10):
        super().__init__(daemon=True)
        self.lista_clientes = lista_clientes
        self.mapa= mapa
        self.jogador1 = jogador1
        self.jogador2=jogador2
        self.intervalo = intervalo
        self.running = True
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #-----

    def run(self):
        print("ThreadBroadcast ativa")
        while self.running:
            try:
                time.sleep(self.intervalo)
                mapa = self.mapa.simplify()
                pontuacao = (self.jogador1.getPontuacao(),self.jogador2.getPontuacao())
                comecar = (self.jogador1.pronto,self.jogador2.pronto)
                self.broadcast_object([mapa,pontuacao,comecar])
            except Exception as e:
                print(f"Erro: {e}")
                continue
        print("ThreadBroadcast terminada")

    def send_object_udp(self, udp_address, obj):
        data = json.dumps(obj).encode('utf-8')
        self.udp_socket.sendto(data, udp_address)

    def broadcast_object(self, obj: Dict) -> None:

        for item in self.lista_clientes.clientes:
            try:
                self.send_object_udp((item[0][0],item[2]), obj)
            except Exception as e:
                print(f"Erro ao enviar para {item[0]}: {e}")