import pygame
from camera import Camera
from personagem import Personagem
from excessoes.std import Std

class Mundo():
    def __init__(self, objetos) -> None:
        self.camera = Camera(self,(0,0))
        self.fundo = pygame.image.load(f"imgs/{objetos[0].split()[0]}/{objetos[0].split()[1]}/fundo.png")
        self.fundo = pygame.transform.scale(self.fundo, (self.fundo.get_width()*3.3, self.fundo.get_height()*3))
        self.player1 = Personagem(objetos[1], (0,500), 0)
        self.player2 = Personagem(objetos[2], (600,500), 1)
        self.vitoria = None
        self.contador_fim = 0
        self.mostrar_press_anything = False

    def tick(self):
        if self.vitoria != None:
            self.contador_fim += 1
            if self.contador_fim > 100:
                self.mostrar_press_anything = True
            return
        self.camera.tick()
        self.player1.tick()
        self.player2.tick()
        self.colisao()
        self.limitar()
        self.orientar()
        if self.player1.vida <= 0:
            self.vitoria = self.player2
        if self.player2.vida <= 0:
            self.vitoria = self.player1

    def limitar(self):
        if self.player1.x < 0:
            self.player1.x = 0
        if self.player2.x < 0:
            self.player2.x = 0
        if self.player1.x > 3000:
            self.player1.x = 3000
        if self.player2.x > 3000:
            self.player2.x = 3000

        if abs(self.player1.x - self.player2.x) > 1800:
            if self.player1.x < self.player2.x:
                self.player1.x += 10
                self.player2.x -= 10
            else:
                self.player1.x -= 10
                self.player2.x += 10

    def orientar(self):
        if self.player1.x < self.player2.x:
            if self.player1.orientacao == 0:
                self.player1.setDeCostas()
            if self.player2.orientacao == 1:
                self.player2.setDeCostas()
        else:
            if self.player1.orientacao == 1:
                self.player1.setDeCostas()
            if self.player2.orientacao == 0:
                self.player2.setDeCostas()
        

    def colisao(self):
        # descobre o vetor de penetracao
        if self.player1.colision_box.colliderect(self.player2.colision_box):
            if self.player1.x < self.player2.x:
                self.player1.x -= 10
                self.player2.x += 10
            else:
                self.player1.x += 10
                self.player2.x -= 10

        if self.player1.atack_box != None and self.player1.atack_box.colliderect(self.player2.colision_box):
            if self.player1.x < self.player2.x:
                self.player2.x += 10
            else:
                self.player2.x -= 10
            self.player1.attack_box = None
            self.player2.damage(self.player1.danos[self.player1.STATE])
        if self.player2.atack_box != None and self.player2.atack_box.colliderect(self.player1.colision_box):
            if self.player1.x < self.player2.x:
                self.player1.x -= 10
            else:
                self.player1.x += 10
            self.player2.attack_box = None
            self.player1.damage(self.player2.danos[self.player2.STATE])

        
    def input(self, evento):
        if self.mostrar_press_anything:
            if evento.type == pygame.KEYDOWN:
                raise Std("Game Over")
        if self.player1 != None:
            self.player1.input(evento)
        if self.player2 != None:
            self.player2.input(evento)

        
    
    def render(self, screen):
        self.camera.render(screen, self.fundo, (-1000,-1600))
        self.player1.render(screen, self.camera)
        self.player2.render(screen, self.camera)

        # Mostra o texto <nome> venceu no meio da tela

        if self.vitoria != None:
            font = pygame.font.Font(None, 72)
            text = font.render(f"{self.vitoria.nome} venceu", True, (255, 255, 255))
            screen.blit(text, (screen.get_width()/2 - text.get_width()/2, screen.get_height()/2 - text.get_height()/2))

            if self.mostrar_press_anything:
                text = font.render("Pressione qualquer tecla", True, (255, 255, 255))
                screen.blit(text, (screen.get_width()/2 - text.get_width()/2, screen.get_height()/2 - text.get_height()/2 + 100))
                text = font.render("para voltar ao menu", True, (255, 255, 255))
                screen.blit(text, (screen.get_width()/2 - text.get_width()/2, screen.get_height()/2 - text.get_height()/2 + 150))