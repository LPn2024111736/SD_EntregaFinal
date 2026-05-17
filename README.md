# Entrega final

## Elementos do grupo:
- Miguel Albernaz (2024109911)
- Miguel Braz     (2024111736)

## Objetivo do jogo 
- O jogo segue um modelo competitivo, no qual cada jogador tem de realizar o máximo de entregas possíveis mais rapidamente que o seu oponente. 
- O primeiro jogador a fazer 10 pontos ganha, com um ponto correspondendo a uma entrega sucedida. 
- Para completar uma entrega, o jogador tem de colocar 3 objetos sequencialmente num pacote a partir de geradores de objetos, e depois entregar este pacote ao cliente correspondente.

## Interface gráfica
- O jogo utiliza a livraria pygame para dispôr da sua interface gráfica, com gráficos realizados pelos elementos do grupo. 
- A janela pode estar em 3 estados: 
  - A tela inicial em que ambos os jogadores têm de pressionar uma tecla para começar.
  - Uma tela de fim a mostrar quem acabou de ganhar.
  - A tela de jogo, onde realmente acontece a comunicação e demonstração da lógica do jogo.
-Esta interface gráfica está completamente separada da lógica do jogo, sendo acessada apenas pelo cliente. 

## Objetos interativos 
- Jogador: Controlado com WASD (movimento) e E (interação). Jogadores conseguem carregar um objeto de cada vez, incluindo pacotes.
    - O objeto a ser carregado é mostrado visualmente no personagem, indicado pela cor deste.
- Geradores de Objetos: Geram os objetos precisos para completar pacotes.
- Pacotes: Conseguem receber objetos ou ter objetos removidos deles. São entregados a clientes para ganhar pontos.
- Clientes: Interação com clientes enquanto está a ser-se segurado um pacote igual ao seu pedido irá entregar o pacote em troca de pontos.
    - A ordem em que os objetos devem ser inseridos no pacote segue as cores do cliente de cima para baixo.
- Contentores: Servem como contentor de lixo, permitindo eliminar pacotes errados ou objetos obtidos incorretamente.

## Comunicação
- O jogo segue o modelo cliente-servidor, com os clientes enviando comandos por via de sockets para o servidor (ints, strings, objetos), com este alterando o estado de jogo.
- O servidor, por sua vez, irá gerir este estado interno, disponibilizando uma representação visual deste estado para os clientes.
- O jogo necessita de um servidor e dois clientes para funcionar corretamente.
- A informação crucial do jogo é guardada na classe EstadoJogo, a qual contém a pontuação dos jogadores e uma representação simplificada do mapa (array 2d).
- O mapa em si, juntamente com todos os objetos do jogo, são tratados na forma de classes, com métodos utilizados para a interação entre estes.
- O estado do jogo é enviado por meio de broadcast UDP, mandando esta estrutura para ambos os clientes repetidamente para garantir a atualização constante.
- A informação do jogo é guardada utilizando o ficheiro dados.py, que armazena os dois tipos de operações feitos no jogo, movimentações e interações com objetos. 

