class EstadoJogo:
    """Classe EstadoJogo
    Esta classe é usada como meio de envio de dados para os clientes através de broadcast guardando três valores
    principais:
    self.value: o mapa atual do jogo, em formato de lista de strings.
    self.score: a pontuação dos jogadores, na forma de um tuplo de inteiros.
    self.começar: o estado de início do jogo de cada jogador, na forma de um tuplo de inteiros."""

    def __init__(self):
        #valores iniciais de zero para ambos os tuplos, e um mapa inicial de exemplo.
        self.value=  [['[X]', '[▵]', '[▫]', '[X]', '[X]', '[XXXXX]', '[X]', '[X]', '[▫]', '[▵]', '[X]'],
                     ['[⛶]', '[ ]', '[ ]', '[ ]', '[ ]', '[A:▵▵▵]', '[ ]', '[ ]', '[ ]', '[ ]', '[⛶]'],
                     ['[◼]', '[ ]', '[11]', '[ ]', '[ ]', '[B:▵▵▵]', '[ ]', '[ ]', '[21]', '[ ]', '[◼]'],
                     ['[⛶]', '[ ]', '[ ]', '[ ]', '[ ]', '[C:▵▵▵]', '[ ]', '[ ]', '[ ]', '[ ]', '[⛶]'],
                     ['[X]', '[◦]', '[▪]', '[X]', '[X]', '[XXXXX]', '[X]', '[X]', '[▪]', '[◦]', '[X]']]
        self.score=(0,0)
        self.comecar=(0,0)

    def update(self,value):
        """update()
        atualiza os valores do estado do jogo com base nos valores fornecidos pelo broadcast."""
        self.value=value[0]
        self.score=value[1]
        self.comecar=value[2]
        