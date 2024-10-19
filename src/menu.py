import pygame
from botao import Botao
from mundo import Mundo
from excessoes.std import Std

class Menu():
    def __init__(self) -> None:
        self.criaBotoesMenuPrincipal()
        self.criaBotoesMenuJogar()
        self.STATE:str = "Menu"
        self.mundo = None
        self.fonte_padrao = pygame.font.Font(None, 200)

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
        self.botoesMenuJogar.append(Botao(150, 100, 128, 128, "Cenario 1", path = "imgs/cenario/1/icon.png"))
        self.botoesMenuJogar.append(Botao(350, 100, 128, 128, "Cenario 2", path = "imgs/cenario/2/icon.png"))
        self.botoesMenuJogar.append(Botao(550, 100, 128, 128, "Cenario 3", path = "imgs/cenario/3/icon.png"))

        self.botoesMenuJogar.append(Botao(150, 400, 128, 128, "Jogador 1", path = "imgs/lutadores/1/icon.png"))
        self.botoesMenuJogar.append(Botao(350, 400, 128, 128, "Jogador 2", path = "imgs/lutadores/2/icon.png"))
        self.botoesMenuJogar.append(Botao(550, 400, 128, 128, "Jogador 3", path = "imgs/lutadores/3/icon.png"))

        self.botoesMenuJogar.append(Botao(150, 600, 128, 128, "Jogador 4", path = "imgs/lutadores/4/icon.png"))
        self.botoesMenuJogar.append(Botao(350, 600, 128, 128, "Jogador 5", path = "imgs/lutadores/5/icon.png"))
        self.botoesMenuJogar.append(Botao(550, 600, 128, 128, "Jogador 6", path = "imgs/lutadores/6/icon.png"))
        self.botoesMenuJogar.append(Botao(50, 800, 100, 50, "Voltar", textSize = 36))

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
        if self.STATE == "Mundo":
            try:
                self.mundo.input(evento)
            except Std as e:
                print(e.message)
            