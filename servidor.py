# pip install pygame
# pip install thread6
# pip install socket.py
# cxfreeze servidor.py --target-dir ping-pong comando para criar o executavel
import pygame
import random
import math
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

        pygame.draw.rect(superfice, (230, 230, 230), self.rect)#superfice, cor, rect

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
        #parte do servidor
        self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Internet , protocolo TCP/IP
        self.ip = '0.0.0.0'
        self.porta = 9999
        self.cliente_socket = None
        self.endereco = None
        self.servidor.bind((self.ip, self.porta))
        self.servidor.listen(1) #numero máximo de conexões sera 1
        ########################################
        self.posicao_y = 250 #posiçãoo de y inicial
        self.jogador_1_x, self.jogador_1_y = 0, 250 #coordenada do jogador 1
        self.jogador_2_x, self.jogador_2_y = 880, 250#coordenada do jogador 2
        self.jogador_tamanho =[20, 80] #tamanho dos jogadores
        self.velocidade_y_1, self.velocidade_y_2 = 0, 0 #velocidade inicial dos jogadores
        self.jogador_1 = jogador(self.jogador_1_x, self.jogador_1_y, self.jogador_tamanho) #iniciando a class jogador1
        self.jogador_2 = jogador(self.jogador_2_x, self.jogador_2_y, self.jogador_tamanho) #iniciando a class jogador2
        self.rect = pygame.Rect(0, 0, 900, 500) #limite ate onde o retangulo vai
        self.bola_direcao = [-1, 1]
        self.bola = bola(450, 250, [10, 10], random.choice(self.bola_direcao))  #iniciando a class bola com a posição inicia e o tamanho e a direção
        self.bola_libera = False # a bola incialmente esta presa
        self.bola_velocidade_x, self.bola_velocidade_y = 8, 2 
        self.placar_1, self.placar_2 = 0, 0 #iniciando o placar dos jogadores
        self.clock = pygame.time.Clock() #controlar o tempo do clock

#loop principal do jogo
    def loop_principal(self):
        self.criar_um_thread(self.espera_conexao)

        while self.gameloop: #loop para deixar o display aberto
            for event in pygame.event.get(): #evento para deixar display respondendo
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:#Ao pressionar a tecla ele se movimenta
                    #pressionar as seta cima baixo velocidade/posição muda 
                    if event.key == pygame.K_w:
                        self.velocidade_y_1 = -10
                    if event.key == pygame.K_s:
                        self.velocidade_y_1 = 10
                    #Ao para de pressionar a tecla espaço ele libera a bola
                    if event.key == pygame.K_SPACE:
                        self.bola_libera = True
                #Ao para de pressionar a tecla ele para o movimenta
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        self.velocidade_y_1 = 0
                    if event.key == pygame.K_s:
                        self.velocidade_y_1 = 0

            

            self.jogador_1.movimentos(self.velocidade_y_1)
            self.jogador_2.rect.y = int(self.posicao_y)
            self.jogador_2.movimentos(self.velocidade_y_2)
            
            if self.bola_libera: #se o jogo começar o movimento da bola sera definido
                self.bola.movimento(self.bola_velocidade_x, self.bola_velocidade_y)
            
            #checando se tem colisão entre a bola e jogador 1 ou a bola e jogador 2
            if self.jogador_1.rect.colliderect(self.bola.rect) or self.jogador_2.rect.colliderect(self.bola.rect): 
                self.bola_velocidade_x = self.mudar_direcao_bola(self.bola_velocidade_x, 0)
                self.bola_velocidade_y = self.mudar_direcao_bola(self.bola_velocidade_y, 60)
                self.bola.velocidade_aleatoria_y = random.randint(1, 7) # mudando a velocidade a cada colisão

            #checando se tem colisão entre a bola e a parte superio e inferio da tela
            if self.bola.rect.top <= 0 or self.bola.rect.bottom >= 500:
                self.bola_velocidade_y = self.mudar_direcao_bola(self.bola_velocidade_y, 0)
            
            #checando se alguns dos jogadores pontuou
            if self.bola.rect.right >=900:
                self.bola.rect.x, self.bola.rect.y = 450, 250
                self.placar_1 += 1
                self.bola_libera = False
            if self.bola.rect.left <= 0:
                self.bola.rect.x, self.bola.rect.y = 450, 250
                self.placar_2 += 1
                self.bola_libera = False
            
            self.jogador_1.rect.clamp_ip(self.rect) #colocando limite ate onde o retangulo vai
            self.jogador_2.rect.clamp_ip(self.rect) #colocando limite ate onde o retangulo vai
            self.bola.rect.clamp_ip(self.rect)#colocando limite ate onde a bola vai
            dados_enviados = f"{self.jogador_1.rect.y},{self.bola.rect.x},{self.bola.rect.y},{self.placar_1},{self.placar_2},{self.bola_libera}" #resolver isso
            
            # checando se nosso cliente esta conectado ao servidor
            if self.cliente_socket is not None:
                self.cliente_socket.send(dados_enviados.encode('utf-8'))# se estiver mandamos os dados para ele em forma de bytes

            self.display.fill((40, 40, 40)) #cor de fundo do display
            self.criar_mensagem('media', f"Jogo Ping Pong", [370,50 ,20, 20], (255, 255, 255))#colocando a mensagem na tela
            self.criar_mensagem('grande', f"{self.placar_1}", [340,100 ,20, 20], (255, 255, 255))#colocando o placar do jogador1
            self.criar_mensagem('grande', f"{self.placar_2}", [525,100 ,20, 20], (255, 255, 255))#colocando o placar do jogador2
            self.criar_mensagem('pequena', f" w : Subir", [0,10 ,20, 20], (255, 255, 255))#teclas para jogar
            self.criar_mensagem('pequena', f" S: Descer", [0,25 ,20, 20], (255, 255, 255))#teclas para jogar
            if self.bola_libera is False:
                self.criar_mensagem('pequena', f"Aperte espaço para começar o jogo", [330,180 ,300, 50], (255, 255, 255))
            self.bola.anexar(self.display)#colocando a bola no display
            self.jogador_1.anexar(self.display)#colocando o jogador 1 na tela
            self.jogador_2.anexar(self.display)#colocando o jogador 2 na tela
            pygame.display.flip()
            self.clock.tick(60) #definindo o tempo do clock


#mudar direção da bola quando ouver colisão
    def mudar_direcao_bola(self, velocidade, angulo):

        velocidade = -(velocidade * math.cos(angulo))

        return velocidade
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
    
    def espera_conexao(self):
        
        self.cliente_socket, self.endereco = self.servidor.accept()
        self.receber_dados()
    
    def receber_dados(self):
        #resolver isso
        while True:
            self.posicao_y = self.cliente_socket.recv(128).decode('utf-8')#128 numero de caracteres que recebemos a cada loop e no .decode convertendo de bytes a string

    def criar_um_thread(self, alvo):

        thread = threading.Thread(target=alvo)
        thread.daemon = True
        thread.start()#permitira fazer a transaçoes



if __name__ == '__main__':

    pygame.init()
    jogo().loop_principal()
    pygame.quit()
