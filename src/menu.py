import pygame
from botao import Botao
from mundo import Mundo
from excessoes.std import Std
from choice import Choice

class Menu():
    def __init__(self) -> None:
        self.criaBotoesMenuPrincipal()
        self.criaBotoesMenuJogar()
        self.STATE:str = "Menu"
        self.mundo = None
        self.fonte_padrao = pygame.font.Font(None, 200)
        self.selection = [None, None, None]

    def tick(self):
        if self.STATE == "Lutar":
            try:
                self.mundo.tick()
            except Std as e:
                print(e.message)
        if self.STATE == "Sair":
            raise Std("Sair")

    def render(self, screen):
        if self.STATE == "Menu":
            screen.blit(self.fonte_padrao.render("UFG", True, (255,0,0)), (screen.get_rect().center[0] - 150, 50))
            for botao in self.botoesMenuPrincipal:
                botao.render(screen)
            return
        if self.STATE == "Jogar":
            for botao in self.botoesMenuJogar:
                botao.render(screen)
            for choice in self.selecao:
                choice.render(screen)
            return

        
    def criarMundo(self):
        self.mundo = Mundo()

    def criaBotoesMenuPrincipal(self):
        self.botoesMenuPrincipal = []
        self.botoesMenuPrincipal.append(Botao(200, 250, 400, 100, "Jogar", textSize = 72))
        self.botoesMenuPrincipal.append(Botao(200, 400, 400, 100, "Criar jogador", textSize = 72))
        self.botoesMenuPrincipal.append(Botao(200, 550, 400, 100, "Criar mapa", textSize = 72))
        self.botoesMenuPrincipal.append(Botao(200, 700, 400, 100, "Sair", textSize = 72))

    def criaBotoesMenuJogar(self):
        self.botoesMenuJogar = []
        posicoes = [(150, 100), (350, 100), (550, 100), (150, 400), (350, 400), (550, 400), (150, 600), (350, 600), (550, 600)]
        self.botoesMenuJogar.append(Botao(*posicoes[0], 128, 128, "Cenario 1", path = "imgs/cenario/1/icon.png"))
        self.botoesMenuJogar.append(Botao(*posicoes[1], 128, 128, "Cenario 2", path = "imgs/cenario/2/icon.png"))
        self.botoesMenuJogar.append(Botao(*posicoes[2], 128, 128, "Cenario 3", path = "imgs/cenario/3/icon.png"))

        self.botoesMenuJogar.append(Botao(*posicoes[3], 128, 128, "Jogador 1", path = "imgs/lutadores/1/icon.png"))
        self.botoesMenuJogar.append(Botao(*posicoes[4], 128, 128, "Jogador 2", path = "imgs/lutadores/2/icon.png"))
        self.botoesMenuJogar.append(Botao(*posicoes[5], 128, 128, "Jogador 3", path = "imgs/lutadores/3/icon.png"))

        self.botoesMenuJogar.append(Botao(*posicoes[6], 128, 128, "Jogador 4", path = "imgs/lutadores/4/icon.png"))
        self.botoesMenuJogar.append(Botao(*posicoes[7], 128, 128, "Jogador 5", path = "imgs/lutadores/5/icon.png"))
        self.botoesMenuJogar.append(Botao(*posicoes[8], 128, 128, "Jogador 6", path = "imgs/lutadores/6/icon.png"))
        self.botoesMenuJogar.append(Botao(50, 800, 100, 50, "Voltar", textSize = 36))
        self.selecao = []
        self.selecao.append(Choice(posicoes[:3], 0, 132, 132, "Cenario", cor = (0, 200, 0)))
        self.selecao.append(Choice(posicoes[3:], 0, 132, 132, "Jogador 1", cor = (200, 0, 0), tamanho = 36))
        self.selecao.append(Choice(posicoes[3:], 0, 132, 132, "Jogador 2", cor = (0, 0, 200), tamanho = 36))

    def input(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.STATE == "Menu":
                for botao in self.botoesMenuPrincipal:
                    clique = botao.identificaClique(evento.pos)
                    if clique:
                        self.STATE = clique
            if self.STATE == "Jogar":
                for botao in self.botoesMenuJogar:
                    clique = botao.identificaClique(evento.pos)
                    if clique:
                        if clique == "Voltar":
                            self.STATE = "Menu"
                            return
                        if clique == "Cenario 1" and self.selection[0] == None:
                            self.selecao[0].index = 0
                            self.selection[0] = clique

        if evento.type == pygame.KEYDOWN:
            if self.STATE == "Jogar":
                if evento.key == pygame.K_RETURN or evento.key == pygame.K_SPACE:
                    if self.selection[0] == None:
                        if self.botoesMenuJogar[self.selecao[0].index].text == "Locked":
                            return
                        self.selection[0] = self.selecao[0].index
                        # corta a cor pela metade
                        self.selecao[0].cor = (self.selecao[0].cor[0]//2, self.selecao[0].cor[1]//2, self.selecao[0].cor[2]//2)

                if evento.key == pygame.K_g:
                    if self.selection[1] == None:
                        if self.botoesMenuJogar[self.selecao[1].index+3].text == "Locked":
                            return
                        self.selection[1] = self.selecao[1].index
                        self.selecao[1].cor = (self.selecao[1].cor[0]//2, self.selecao[1].cor[1]//2, self.selecao[1].cor[2]//2)
                    
                # se clicou .
                if evento.key == pygame.K_PERIOD:
                    if self.selection[2] == None:
                        if self.botoesMenuJogar[self.selecao[2].index+3].text == "Locked":
                            return
                        self.selection[2] = self.selecao[2].index
                        self.selecao[2].cor = (self.selecao[2].cor[0]//2, self.selecao[2].cor[1]//2, self.selecao[2].cor[2]//2)
                    
                if evento.key == pygame.K_ESCAPE:
                    for i in range(len(self.selection)-1,-1,-1):
                        if self.selection[i] != None:
                            self.selection[i] = None
                            self.selecao[i].cor = (self.selecao[i].cor[0]*2, self.selecao[i].cor[1]*2, self.selecao[i].cor[2]*2)
                            break
                    
                for i, choice in enumerate(self.selecao):
                    if self.selection[i] == None:
                        if i == 0:
                            choice.input(evento)
                            break
                        if evento.key in (pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_w) and i == 1:
                            choice.input(evento)
                        if evento.key in (pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_UP) and i == 2:
                            choice.input(evento)
        if self.STATE == "Mundo":
            try:
                self.mundo.input(evento)
            except Std as e:
                print(e.message)
            