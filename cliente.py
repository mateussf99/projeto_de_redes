import pygame
import random
import socket
import threading


class bola:

    def __init__(self, x, y, tamanho, direcao):

        self.x = x #posição da bola
        self.y = y #posição da bola
        self.tamanho = tamanho
        self.direcao = direcao
        self.rect = pygame.Rect(self.x, self.y, self.tamanho[0], self.tamanho[1]) #retangulo (posição x,posição y altura e largura do jogador)
        self.velocidade_aleatoria_y = random.randint(1, 4) #vai escolher uma velocidade x aleatoria onde 1> x <= 4

    def movimento(self, velocidade_x, velocidade_y):

        self.rect.x =(self.rect.x + self.direcao * velocidade_x)
        self.rect.y +=  self.velocidade_aleatoria_y * velocidade_y
    
    def anexar(self, superfice):

        pygame.draw.rect(superfice, (230, 230, 230), self.rect)#super, cor, rect
class jogador:

    def __init__(self, x, y, tamanho):
        self.x = x #posição do jogador
        self.y = y #posição do jogador
        self.tamanho = tamanho
        self.rect = pygame.Rect(self.x, self.y, self.tamanho[0], self.tamanho[1]) #retangulo (posição x,posição y, altura e largura do jogador)
    
    def movimentos(self, velocidade):
        
        self.rect.y += velocidade

    def anexar(self, superfice):
        pygame.draw.rect(superfice, (200, 200, 200), self.rect)#superfice, cor, rect

class jogo: #classe para criação da janela

    def  __init__(self):

        self.display = pygame.display.set_mode((900, 500)) #altura e largura do d
        pygame.display.set_caption('Pong') #nome do display
        self.gameloop = True #parametro para deixar o display aberto
        #parte do cliente
        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Internet , protocolo TCP/IP
        self.ip = '127.0.0.1' #ip da maquina de destino
        self.porta = 9999
        ########################################
        self.posicao_y = 250 #posiçãoo de y inicial
        self.jogador_1_x, self.jogador_1_y = 0, 250 #coordenada do jogador 1
        self.jogador_2_x, self.jogador_2_y = 880, 250#coordenada do jogador 2
        self.jogador_tamanho =[20, 80] #tamanho dos jogadores
        self.velocidade_y_1, self.velocidade_y_2 = 0, 0 #velocidade inicial dos jogadores
        self.jogador_1 = jogador(self.jogador_1_x, self.jogador_1_y, self.jogador_tamanho) #iniciando a class jogador1
        self.jogador_2 = jogador(self.jogador_2_x, self.jogador_2_y, self.jogador_tamanho) #iniciando a class jogador2

        self.bola_direcao = [-1, 1]
        self.bola = bola(450, 250, [10, 10], random.choice(self.bola_direcao))  #iniciando a class bola com a posição inicia e o tamanho e a direção
        self.placar_1, self.placar_2 = 0, 0 #iniciando o placar dos jogadores
        self.bola_x, self.bola_y = None, None #posição inicial da bola
        self.bola_lib = False # a bola incialmente esta presa
        self.jogador_1_posicao = 250 #posição inicial do jogador 1
        self.recebimento_dados = False #recebimento de dados inicial é falso
        self.clock = pygame.time.Clock() #controlar o tempo do clock

#loop principal do jogo
    def loop_principal(self):

        self.cliente.connect((self.ip, self.porta))
        self.criar_um_thread(self.receber_dados)#criando a thread para receber os dados



        while self.gameloop: #loop para deixar o display aberto
            for event in pygame.event.get(): #evento para deixar display respondendo
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:#Ao pressionar a tecla ele se movimenta
                    #pressionar as teclas w e s  velocidade/posição muda
                    if event.key == pygame.K_w:
                        self.velocidade_y_2 = -10
                    if event.key == pygame.K_s:
                        self.velocidade_y_2 = 10
                if event.type == pygame.KEYUP: #Ao para de pressionar a tecla ele para o movimenta
                    if event.key == pygame.K_w:
                        self.velocidade_y_2 = 0
                    if event.key == pygame.K_s:
                        self.velocidade_y_2 = 0
            
            if self.recebimento_dados:
                self.bola.rect.x = self.bola_x
                self.bola.rect.y = self.bola_y
                self.jogador_1.rect.y = self.jogador_1_posicao
                self.bola_lib = self.bola_libera
            
                
                

            self.jogador_1.movimentos(self.velocidade_y_1)
            self.jogador_2.movimentos(self.velocidade_y_2)
            posicao_y_jogador_2 = f"{self.jogador_2.rect.y}" #vai converte a posição do jogador2 / cliente para string
            self.cliente.send(posicao_y_jogador_2.encode('utf-8'))#convertendo a string para bytes
            
            self.recebimento_dados = True #recebir os dados posso libera thread

            self.display.fill((40, 40, 40)) #cor de fundo do display
            self.criar_mensagem('media', f"Jogo Ping Pong", [370,50 ,20, 20], (255, 255, 255))#colocando a mensagem na tela
            self.criar_mensagem('grande', f"{self.placar_1}", [340,100 ,20, 20], (255, 255, 255))#colocando o placar do jogador1
            self.criar_mensagem('grande', f"{self.placar_2}", [525,100 ,20, 20], (255, 255, 255))#colocando o placar do jogador2
            self.criar_mensagem('pequena', f" w : Subir", [0,10 ,20, 20], (255, 255, 255))#teclas para jogar
            self.criar_mensagem('pequena', f" S: Descer", [0,25 ,20, 20], (255, 255, 255))#teclas para jogar
            if self.bola_lib == 'False':
                self.criar_mensagem('pequena', f"Esperando o host aperta espaço para começar o jogo", [310,180 ,300, 50], (255, 255, 255))
            
            self.bola.anexar(self.display)#colocando a bola no display
            self.jogador_1.anexar(self.display)#colocando o jogador 1 na tela
            self.jogador_2.anexar(self.display)#colocando o jogador 2 na tela
            pygame.display.flip()
            self.clock.tick(60) #definindo o tempo do clock



#criar mensagem do display 
    def criar_mensagem(self, font, mensagem, mesagem_retangulo, cor):
        
        if font == 'pequena':
            font = pygame.font.Font(None, 20)
        if font == 'media':
            font = pygame.font.Font(None, 30)
        if font == 'grande':
            font = pygame.font.Font(None, 40)
        mensagem = font.render(mensagem, True, cor)
        self.display.blit(mensagem, mesagem_retangulo)
    

    def criar_um_thread(self, alvo):

        thread = threading.Thread(target = alvo)
        thread.daemon = True
        thread.start()#permitira fazer a transaçoes
    
    #recebendo dados do servidor
    def receber_dados(self):
        while True:
           dados_recebidos = self.cliente.recv(128).decode('utf-8') #128 numero de caracteres que recebemos a cada loop e no .decode convertendo de bytes a string
           dados_recebidos = dados_recebidos.split(',')
           #pegando o dado e convertendo
           self.jogador_1_posicao = int(dados_recebidos[0])
           self.bola_x = int(dados_recebidos[1])
           self.bola_y = int(dados_recebidos[2])
           self.placar_1, self.placar_2 = int(dados_recebidos[3]), int(dados_recebidos[4])
           self.bola_libera = dados_recebidos[5]
           


if __name__ == '__main__':

    pygame.init()
    jogo().loop_principal()
    pygame.quit()
