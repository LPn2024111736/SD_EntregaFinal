""" A inteface agora envolve a utilização do pygame para a visualização do jogo pelo utilizador.
Como muito deste código está em várias funções separadas que dependem umas das outras, comentários
suplementares ao uso exclusivo de docstrings irá ser utilizado"""

import socket
import json
import Cliente
import pygame
import Cliente.interface.broadcast_receiver as broadcast_receiver
from Dados.estadoJogo import EstadoJogo

#pygame.init é necessário para utilizar o pygame
pygame.init()

"""
TILESIZE é o tamanho de cada quadricula. Esta constante é usada para definir certos elementos como:
 1. Tamanho da janela
 2. Posição dos objetos de jogo na tela
 3. Tamanho de elementos visuais que não utilizam imagens (scorebg)
"""
TILESIZE = Cliente.TILESIZE

"""Inicialização de elementos base para o jogo:
1. Tamanho da janela
2. Relógio (pygame.Clock()) utilizado para controlar framerate máxima
3. Fonte utizada para o texto do programa
4. Nome da janela
5. Ícone do jogo na janela
"""
janela = pygame.display.set_mode((TILESIZE * Cliente.SCREEN_WIDTH, TILESIZE * Cliente.SCREEN_HEIGHT))
clock = pygame.Clock()
font = pygame.font.SysFont("Upheaval TT (BRK)", 40)
pygame.display.set_caption("Teamworkshop!")
pygame_icon = pygame.image.load("../Cliente/imagens/icon.png")
pygame.display.set_icon(pygame_icon)

#Import de todas as imagens, convert.alpha() é utilizado para imagens com transparência.
background = pygame.image.load("../Cliente/imagens/background.png").convert()
parede = pygame.image.load("../Cliente/imagens/parede.png").convert()
geradorC = pygame.image.load("../Cliente/imagens/gerador_cir.png").convert()
geradorR = pygame.image.load("../Cliente/imagens/gerador_rec.png").convert()
geradorS = pygame.image.load("../Cliente/imagens/gerador_sqr.png").convert()
geradorT = pygame.image.load("../Cliente/imagens/gerador_tri.png").convert()
contentor = pygame.image.load("../Cliente/imagens/contentor.PNG").convert()
contentor0 = pygame.image.load("../Cliente/imagens/contentor_vazio.png").convert()
contentor50 = pygame.image.load("../Cliente/imagens/contentor_incompleto.png").convert()
contentor100 = pygame.image.load("../Cliente/imagens/contentor_cheio.png").convert()
cliente = pygame.image.load("../Cliente/imagens/cliente.png")
clienteC = pygame.image.load("../Cliente/imagens/cliente_cir.png")
clienteR = pygame.image.load("../Cliente/imagens/cliente_ret.png")
clienteS = pygame.image.load("../Cliente/imagens/cliente_sqr.png")
clienteT = pygame.image.load("../Cliente/imagens/cliente_tri.png")
p1UP = pygame.image.load("../Cliente/imagens/p1_up.png").convert_alpha()
p1UPC = pygame.image.load("../Cliente/imagens/p1_up_hold_c.png").convert_alpha()
p1UPR = pygame.image.load("../Cliente/imagens/p1_up_hold_r.png").convert_alpha()
p1UPS = pygame.image.load("../Cliente/imagens/p1_up_hold_s.png").convert_alpha()
p1UPT = pygame.image.load("../Cliente/imagens/p1_up_hold_t.png").convert_alpha()
p1UPE = pygame.image.load("../Cliente/imagens/p1_up_hold_e.png").convert_alpha()
p2UP = pygame.image.load("../Cliente/imagens/p2_up.png").convert_alpha()
p2UPC = pygame.image.load("../Cliente/imagens/p2_up_hold_c.png").convert_alpha()
p2UPR = pygame.image.load("../Cliente/imagens/p2_up_hold_r.png").convert_alpha()
p2UPS = pygame.image.load("../Cliente/imagens/p2_up_hold_s.png").convert_alpha()
p2UPT = pygame.image.load("../Cliente/imagens/p2_up_hold_t.png").convert_alpha()
p2UPE = pygame.image.load("../Cliente/imagens/p2_up_hold_e.png").convert_alpha()
p1DOWN = pygame.image.load("../Cliente/imagens/p1_down.png").convert_alpha()
p1DOWNC = pygame.image.load("../Cliente/imagens/p1_down_hold_c.png").convert_alpha()
p1DOWNR = pygame.image.load("../Cliente/imagens/p1_down_hold_r.png").convert_alpha()
p1DOWNS = pygame.image.load("../Cliente/imagens/p1_down_hold_s.png").convert_alpha()
p1DOWNT = pygame.image.load("../Cliente/imagens/p1_down_hold_t.png").convert_alpha()
p1DOWNE = pygame.image.load("../Cliente/imagens/p1_down_hold_e.png").convert_alpha()
p2DOWN = pygame.image.load("../Cliente/imagens/p2_down.png").convert_alpha()
p2DOWNC = pygame.image.load("../Cliente/imagens/p2_down_hold_c.png").convert_alpha()
p2DOWNR = pygame.image.load("../Cliente/imagens/p2_down_hold_r.png").convert_alpha()
p2DOWNS = pygame.image.load("../Cliente/imagens/p2_down_hold_s.png").convert_alpha()
p2DOWNT = pygame.image.load("../Cliente/imagens/p2_down_hold_t.png").convert_alpha()
p2DOWNE = pygame.image.load("../Cliente/imagens/p2_down_hold_e.png").convert_alpha()
p1LEFT = pygame.image.load("../Cliente/imagens/p1_left.png").convert_alpha()
p1LEFTC = pygame.image.load("../Cliente/imagens/p1_left_hold_c.png").convert_alpha()
p1LEFTR = pygame.image.load("../Cliente/imagens/p1_left_hold_r.png").convert_alpha()
p1LEFTS = pygame.image.load("../Cliente/imagens/p1_left_hold_s.png").convert_alpha()
p1LEFTT = pygame.image.load("../Cliente/imagens/p1_left_hold_t.png").convert_alpha()
p1LEFTE = pygame.image.load("../Cliente/imagens/p1_left_hold_e.png").convert_alpha()
p2LEFT = pygame.image.load("../Cliente/imagens/p2_left.png").convert_alpha()
p2LEFTC = pygame.image.load("../Cliente/imagens/p2_left_hold_c.png").convert_alpha()
p2LEFTR = pygame.image.load("../Cliente/imagens/p2_left_hold_r.png").convert_alpha()
p2LEFTS = pygame.image.load("../Cliente/imagens/p2_left_hold_s.png").convert_alpha()
p2LEFTT = pygame.image.load("../Cliente/imagens/p2_left_hold_t.png").convert_alpha()
p2LEFTE = pygame.image.load("../Cliente/imagens/p2_left_hold_e.png").convert_alpha()
p1RIGHT = pygame.image.load("../Cliente/imagens/p1_right.png").convert_alpha()
p1RIGHTC = pygame.image.load("../Cliente/imagens/p1_right_hold_c.png").convert_alpha()
p1RIGHTR = pygame.image.load("../Cliente/imagens/p1_right_hold_r.png").convert_alpha()
p1RIGHTS = pygame.image.load("../Cliente/imagens/p1_right_hold_s.png").convert_alpha()
p1RIGHTT = pygame.image.load("../Cliente/imagens/p1_right_hold_t.png").convert_alpha()
p1RIGHTE = pygame.image.load("../Cliente/imagens/p1_right_hold_e.png").convert_alpha()
p2RIGHT = pygame.image.load("../Cliente/imagens/p2_right.png").convert_alpha()
p2RIGHTC = pygame.image.load("../Cliente/imagens/p2_right_hold_c.png").convert_alpha()
p2RIGHTR = pygame.image.load("../Cliente/imagens/p2_right_hold_r.png").convert_alpha()
p2RIGHTS = pygame.image.load("../Cliente/imagens/p2_right_hold_s.png").convert_alpha()
p2RIGHTT = pygame.image.load("../Cliente/imagens/p2_right_hold_t.png").convert_alpha()
p2RIGHTE = pygame.image.load("../Cliente/imagens/p2_right_hold_e.png").convert_alpha()
p1on = pygame.image.load("../Cliente/imagens/menu_p1_on.png").convert_alpha()
p1off = pygame.image.load("../Cliente/imagens/menu_p1_off.png").convert_alpha()
p2on = pygame.image.load("../Cliente/imagens/menu_p2_on.png").convert_alpha()
p2off = pygame.image.load("../Cliente/imagens/menu_p2_off.png").convert_alpha()
logo = pygame.image.load("../Cliente/imagens/logo.png")
scorebg = pygame.Surface((TILESIZE * 15, TILESIZE * 1)).convert()
scorebg.fill("black")
win1 = pygame.image.load("../Cliente/imagens/p1_win.png").convert_alpha()
win2 = pygame.image.load("../Cliente/imagens/p2_win.png").convert_alpha()
class Interface:
    """
    Classe Interface:
    Classe utilizada com o objetivo do cliente poder interagir com o servidor. Ao executar a função exeecute() o cliente
    poderá mandar uma mensagem que ira alterar o estado de componentes do servidor.
    param: connection: permite a comunicação com o servidor via rede.
    param: udp_socket: socket udp para outros tipos de comunicação (recessão de broadcasts).
    param: udp_port: porto udp do cliente.
    param: estado_jogo: estrutura de dados utilizada para guardar informações sobre o jogo, atualizada por broadcast.
    """
    def __init__(self):
        self.connection = socket.socket()
        self.connection.connect((Cliente.SERVER_ADDRESS,Cliente.PORT))
        # Socket UDP dedicado para receber broadcasts
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.bind(('', 0))  # porta livre atribuída pelo SO
        self.udp_port = self.udp_socket.getsockname()[1]
        # Informa o servidor de que a seguir será enviado o porto UDP
        self.send_str(self.connection, Cliente.UDP_PORT)
        self.send_int(self.connection, self.udp_port, Cliente.INT_SIZE)
        print(f"Cliente ligado por TCP; à escuta de broadcasts UDP na porta {self.udp_port}")
        self.estado_jogo = EstadoJogo()

    # ----- enviar e receber strings, inteiros e objetos----- #
    def receive_str(self,connect, n_bytes: int) -> str:
        """
        :param n_bytes: The number of bytes to read from the current connection
        :return: The next string read from the current connection
        """
        data = connect.recv(n_bytes)
        return data.decode()

    def send_str(self,connect, value: str) -> None:
        try:
            connect.send(value.encode())
        except Exception as e:
            print("O servidor fechou!")
            self.endscreen()

    def send_int(self,connect:socket.socket, value: int, n_bytes: int) -> None:

        connect.send(value.to_bytes(n_bytes, byteorder="big", signed=True))

    def receive_int(self,connect: socket.socket, n_bytes: int) -> int:

        data = connect.recv(n_bytes)
        return int.from_bytes(data, byteorder='big', signed=True)

    def receive_object(self, connection):
        try:
            size = self.receive_int(connection, Cliente.INT_SIZE)
            data = b""
            while len(data) < size:
                print(len(data))
                packet = connection.recv(size - len(data))
                if not packet:
                    raise ConnectionError("Ligação perdida")
                data += packet
            return json.loads(data.decode('utf-8'))
        except (MemoryError):
            print("O servidor fechou!")
            self.endscreen()
        except (json.decoder.JSONDecodeError):
            print("O servidor fechou!")
            self.endscreen()

    def send_object(self, connection, obj):
        data = json.dumps(obj).encode('utf-8')
        size = len(data)
        self.send_int(connection, size, Cliente.INT_SIZE)
        connection.sendall(data)  # sendall garante envio completo

    """O programa utiliza três funções principais para a utilização do pygame:
    start_screen(): Tela inicial, estado incial que os jogadores irão ver.
    jogo_principal(): O jogo em si, onde os jogadores poderão interagir com a lógica da terceira entrega.
    endscreen(): Tela de fim de jogo, monstrando quem ganhou. A unica interação nesta é fechar o jogo."""

    def endscreen(self):
        """endscreen()
        Esta função é a mais simples das 3. Apenas utiliza um if else com base na pontuação dos jogadores.
        Se o jogador 1 (self.estado_jogo.score[0]) tiver 10 pontos, mostra a primeira, se não, mostra a segunda."""

        while True:
            if self.estado_jogo.score[0] == Cliente.WIN_SCORE:
                janela.blit(win1,(0,0))
            else:
                janela.blit(win2,(0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            #update() atualiza a janela para mostrar o estado atual, cloc.tick(60) controla o intervalo máximo entre estes.
            pygame.display.update()
            clock.tick(60)

    def jogo_principal(self):
        """jogo_principal()
        Esta função contém a lógica de desenho do mapa, utilizando as imagens definidas no início do módulo e a lógica
        da terceira entrega.
        """

        """A variável interact_buffer é um período de tempo em que o jogador não pode interagir. 
        Este é preciso para assegurar a correção da interação.
        Sem esta, o jogador poderia pegar e depositar o seu objeto repetidamente com só um input."""

        interact_buffer = Cliente.INTERACT_BUFFER
        while True:
            #corre a tela de fim se a pontuação de um jogador chegar a 10
            if self.estado_jogo.score[0] == Cliente.WIN_SCORE or self.estado_jogo.score[1] == Cliente.WIN_SCORE:
                self.endscreen()
            if interact_buffer > 0:
                interact_buffer -= 1
            #permite fechar a janela e interagir se o buffer for igual a zero.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and interact_buffer == 0:
                    self.send_str(self.connection, Cliente.INTERACT)
                    interact_buffer = Cliente.INTERACT_BUFFER

                """pygame.key.get_pressed() é uma função essencial do pygame. Esta disponibiliza um dicionário dispondo se
                uma tecla está a ser pressionada atualmente, com estas teclas sendo a chave e o valor sendo o valor 
                booleano correspondendo a esta questão. Verificando se este valor é verdade, podemos realizar o envio
                de ações para processaCliente como feito com a interface antiga."""

                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    self.send_str(self.connection, Cliente.LEFT)
                elif keys[pygame.K_RIGHT]:
                    self.send_str(self.connection, Cliente.RIGHT)
                elif keys[pygame.K_UP]:
                    self.send_str(self.connection, Cliente.UP)
                elif keys[pygame.K_DOWN]:
                    self.send_str(self.connection, Cliente.DOWN)

                y = 0
                #Elementos visuais sem posição condicional, colocados no mesmo local sempre
                p1score = font.render("P1:" + str(self.estado_jogo.score[0]), True, (255, 255, 255))
                p2score = font.render("P2:" + str(self.estado_jogo.score[1]), True, (255, 255, 255))
                janela.blit(background, (0, 0))
                janela.blit(scorebg, (0, 0))
                janela.blit(p1score, (16, 10))
                janela.blit(p2score, (744, 10))

                """ Este for loop contém a lógica para o desenho do mapa, seguindo o seguinte processo:
                    1. Verifica o valor da string (quadricula) atual,
                    2.1. Coloca a imagem correspondente a esta string na posição correspondente (x,y)
                    2.2. Estes valores têm (TILESIZE,TILSIZE*2) adicionados sempre, para colocar-los no local certo
                    3. x e y são incrementados para corresponder ao seu local na matriz."""
                for line in self.estado_jogo.value:
                    x = 0
                    for element in line:
                        match element:
                            case "[X]":
                                janela.blit(parede, (x + TILESIZE * 1, y + TILESIZE * 2))

                            case "[◦]":
                                janela.blit(geradorC, (x + TILESIZE * 1, y + TILESIZE * 2))
                            case "[▫]":
                                janela.blit(geradorS, (x + TILESIZE * 1, y + TILESIZE * 2))
                            case '[▵]':
                                janela.blit(geradorT, (x + TILESIZE * 1, y + TILESIZE * 2))
                            case "[▪]":
                                janela.blit(geradorR, (x + TILESIZE * 1, y + TILESIZE * 2))

                            case "[XXXXX]":
                                janela.blit(parede, (x + TILESIZE * 1, y + TILESIZE * 2))
                            case "[ ]":
                                pass
                            case _ if "[1" in element:
                                if element[2] == "0":
                                    match element[3]:
                                        case "0":
                                            janela.blit(p1UP, (x + TILESIZE * 1, y + TILESIZE * 2))
                                        case "◦":
                                            janela.blit(p1UPC, (x + TILESIZE * 1, y + TILESIZE * 2))
                                        case "▫":
                                            janela.blit(p1UPS, (x + TILESIZE * 1, y + TILESIZE * 2))
                                        case "▪":
                                            janela.blit(p1UPR, (x + TILESIZE * 1, y + TILESIZE * 2))
                                        case "▵":
                                            janela.blit(p1UPT, (x + TILESIZE * 1, y + TILESIZE * 2))
                                        case _:
                                            janela.blit(p1UPE, (x + TILESIZE * 1, y + TILESIZE * 2))


                                elif element[2] == "1":
                                    match element[3]:
                                        case "0":
                                            janela.blit(p1DOWN, (x + TILESIZE * 1, y + TILESIZE * 2))
                                        case "◦":
                                            janela.blit(p1DOWNC, (x + TILESIZE * 1, y + TILESIZE * 2))
                                        case "▫":
                                            janela.blit(p1DOWNS, (x + TILESIZE * 1, y + TILESIZE * 2))
                                        case "▪":
                                            janela.blit(p1DOWNR, (x + TILESIZE * 1, y + TILESIZE * 2))
                                        case "▵":
                                            janela.blit(p1DOWNT, (x + TILESIZE * 1, y + TILESIZE * 2))
                                        case _:
                                            janela.blit(p1DOWNE, (x + TILESIZE * 1, y + TILESIZE * 2))
                                elif element[2] == "2":
                                    match element[3]:
                                        case "0":
                                            janela.blit(p1RIGHT, (x + TILESIZE * 1, y + TILESIZE * 2))
                                        case "◦":
                                            janela.blit(p1RIGHTC, (x + TILESIZE * 1, y + TILESIZE * 2))
                                        case "▫":
                                            janela.blit(p1RIGHTS, (x + TILESIZE * 1, y + TILESIZE * 2))
                                        case "▪":
                                            janela.blit(p1RIGHTR, (x + TILESIZE * 1, y + TILESIZE * 2))
                                        case "▵":
                                            janela.blit(p1RIGHTT, (x + TILESIZE * 1, y + TILESIZE * 2))
                                        case _:
                                            janela.blit(p1RIGHTE, (x + TILESIZE * 1, y + TILESIZE * 2))
                                else:
                                    match element[3]:
                                        case "0":
                                            janela.blit(p1LEFT, (x + TILESIZE * 1, y + TILESIZE * 2))
                                        case "◦":
                                            janela.blit(p1LEFTC, (x + TILESIZE * 1, y + TILESIZE * 2))
                                        case "▫":
                                            janela.blit(p1LEFTS, (x + TILESIZE * 1, y + TILESIZE * 2))
                                        case "▪":
                                            janela.blit(p1LEFTR, (x + TILESIZE * 1, y + TILESIZE * 2))
                                        case "▵":
                                            janela.blit(p1LEFTT, (x + TILESIZE * 1, y + TILESIZE * 2))
                                        case _:
                                            janela.blit(p1LEFTE, (x + TILESIZE * 1, y + TILESIZE * 2))

                            case _ if "[2" in element:
                                if element[2] == "0":
                                    match element[3]:
                                        case "0":
                                            janela.blit(p2UP, (x + TILESIZE * 1, y + TILESIZE * 2))
                                        case "◦":
                                            janela.blit(p2UPC, (x + TILESIZE * 1, y + TILESIZE * 2))
                                        case "▫":
                                            janela.blit(p2UPS, (x + TILESIZE * 1, y + TILESIZE * 2))
                                        case "▪":
                                            janela.blit(p2UPR, (x + TILESIZE * 1, y + TILESIZE * 2))
                                        case "▵":
                                            janela.blit(p2UPT, (x + TILESIZE * 1, y + TILESIZE * 2))
                                        case _:
                                            janela.blit(p2UPE, (x + TILESIZE * 1, y + TILESIZE * 2))


                                elif element[2] == "1":
                                    match element[3]:
                                        case "0":
                                            janela.blit(p2DOWN, (x + TILESIZE * 1, y + TILESIZE * 2))
                                        case "◦":
                                            janela.blit(p2DOWNC, (x + TILESIZE * 1, y + TILESIZE * 2))
                                        case "▫":
                                            janela.blit(p2DOWNS, (x + TILESIZE * 1, y + TILESIZE * 2))
                                        case "▪":
                                            janela.blit(p2DOWNR, (x + TILESIZE * 1, y + TILESIZE * 2))
                                        case "▵":
                                            janela.blit(p2DOWNT, (x + TILESIZE * 1, y + TILESIZE * 2))
                                        case _:
                                            janela.blit(p2DOWNE, (x + TILESIZE * 1, y + TILESIZE * 2))
                                elif element[2] == "2":
                                    match element[3]:
                                        case "0":
                                            janela.blit(p2RIGHT, (x + TILESIZE * 1, y + TILESIZE * 2))
                                        case "◦":
                                            janela.blit(p2RIGHTC, (x + TILESIZE * 1, y + TILESIZE * 2))
                                        case "▫":
                                            janela.blit(p2RIGHTS, (x + TILESIZE * 1, y + TILESIZE * 2))
                                        case "▪":
                                            janela.blit(p2RIGHTR, (x + TILESIZE * 1, y + TILESIZE * 2))
                                        case "▵":
                                            janela.blit(p2RIGHTT, (x + TILESIZE * 1, y + TILESIZE * 2))
                                        case _:
                                            janela.blit(p2RIGHTE, (x + TILESIZE * 1, y + TILESIZE * 2))
                                else:
                                    match element[3]:
                                        case "0":
                                            janela.blit(p2LEFT, (x + TILESIZE * 1, y + TILESIZE * 2))
                                        case "◦":
                                            janela.blit(p2LEFTC, (x + TILESIZE * 1, y + TILESIZE * 2))
                                        case "▫":
                                            janela.blit(p2LEFTS, (x + TILESIZE * 1, y + TILESIZE * 2))
                                        case "▪":
                                            janela.blit(p2LEFTR, (x + TILESIZE * 1, y + TILESIZE * 2))
                                        case "▵":
                                            janela.blit(p2LEFTT, (x + TILESIZE * 1, y + TILESIZE * 2))
                                        case _:
                                            janela.blit(p2LEFTE, (x + TILESIZE * 1, y + TILESIZE * 2))

                            case "[◫]":
                                janela.blit(contentor100, (x + TILESIZE * 1, y + TILESIZE * 2))
                            case "[◧]":
                                janela.blit(contentor50, (x + TILESIZE * 1, y + TILESIZE * 2))
                            case "[◼]":
                                janela.blit(contentor0, (x + TILESIZE * 1, y + TILESIZE * 2))
                            case "[⛶]":
                                janela.blit(contentor, (x + TILESIZE * 1, y + TILESIZE * 2))
                            case _:
                                """Os clientes seguem um logica de desenho ligeiramente diferente. 
                                Como são compostos por 4 imagens (3 componentes e uma imagem para o cliente em si),
                                Estes são vistos em ultimo lugar como wildcard (_), desenhando cada camada individual
                                e depois a imagem principal."""
                                aux = 128 - 24
                                for character in element:
                                    if character == "◦":
                                        janela.blit(clienteC, (x + TILESIZE * 1, y + TILESIZE * 2 - aux))
                                    elif character == "▫":
                                        janela.blit(clienteS, (x + TILESIZE * 1, y + TILESIZE * 2 - aux))
                                    elif character == "▵":
                                        janela.blit(clienteT, (x + TILESIZE * 1, y + TILESIZE * 2 - aux))
                                    elif character == "▪":
                                        janela.blit(clienteR, (x + TILESIZE * 1, y + TILESIZE * 2 - aux))
                                    aux -= 64 / 3
                                janela.blit(cliente, (x + TILESIZE * 1, y + TILESIZE * 2))
                        x += TILESIZE
                    y += TILESIZE
                # update() atualiza a janela para mostrar o estado atual, cloc.tick(60) controla o intervalo máximo entre estes.
                pygame.display.update()
                clock.tick(60)

    def start_menu(self):
        """
        start_menu()
        define a tela inicial do jogo, ambos os jogadores têm de ter selecionado que querem jogar,
        iniciando assim realmente o jogo.
        """

        while True:
            janela.fill((0, 0, 50))
            play_text = font.render("PRESS Z TO START", False, (255, 255, 255))
            janela.blit(logo, (0, 0))
            janela.blit(play_text, (452, 116))

            #imagens de on/off do jogador 1
            if self.estado_jogo.comecar[0]:
                janela.blit(p1on, (0, 128))
            else:
                janela.blit(p1off, (0, 128))

            #imagens de on/off do jogador 1
            if self.estado_jogo.comecar[1]:
                janela.blit(p2on, (444, 128))
            else:
                janela.blit(p2off, (444, 128))
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                #Mudar estado de início pessoal
                if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                    self.send_str(self.connection, Cliente.START)

                #Inicia o jogo se ambos concordarem em começar
                if self.estado_jogo.comecar[0] == 1 and self.estado_jogo.comecar[1] == 1:
                    self.jogo_principal()
             # update() atualiza a janela para mostrar o estado atual, cloc.tick(60) controla o intervalo máximo entre estes.
            pygame.display.update()
            clock.tick(60)

    def execute(self):
            """
            Função que inicializa a janela de interface e o recetor de broadcast do cliente.
            A função start_menu como a primeira para ambos os jogadores terem de estar em concordância
            que o jogo irá começar.
            """
            broadcast = broadcast_receiver.BroadcastReceiver(self.udp_socket, self.estado_jogo)
            broadcast.start()
            self.start_menu()

