import threading
import json

class BroadcastReceiver(threading.Thread):
    """Classe BroadcastReceiver
    Segue a lógica presente na estrutura do programa de apoio para o LAB4.
    Utilizando o socket udp do cliente, esta thread recebe os objetos enviados
    pelo BroadcastEmissor, Guardando estes em self.mapa, um objeto da classe EstadoJogo
    :param: udp_socket - socket do cliente
    :param: mapa - estado atual do jogo.
    """
    def __init__(self, udp_socket,mapa_jogo):
        super().__init__(daemon=True)
        self.udp_socket = udp_socket
        self.mapa = mapa_jogo
    def receive_object(self):
        data, addr = self.udp_socket.recvfrom(65535)
        obj = json.loads(data.decode('utf-8'))
        return obj
    def run(self):
        print("Receiver de broadcasts UDP ativa...")
        while True:
            try:
                objeto = self.receive_object()
                self.mapa.update(objeto)
            except Exception as e:
                print(f"Receiver UDP desconectado: {e}")
                break
