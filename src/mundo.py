import pygame
from camera import Camera
from personagem import Personagem

class Mundo():
    def __init__(self, objetos) -> None:
        self.camera = Camera(self,(0,0))
        self.fundo = pygame.image.load(f"imgs/{objetos[0].split()[0]}/{objetos[0].split()[1]}/fundo.png")
        self.fundo = pygame.transform.scale(self.fundo, (self.fundo.get_width()*3.3, self.fundo.get_height()*3))
        self.player1 = Personagem(objetos[1], (0,500), 0)
        self.player2 = Personagem(objetos[2], (600,500), 1)

    def tick(self):
        pass
        self.camera.tick()
        self.player1.tick()
        self.player2.tick()
        self.colisao()
        self.limitar()
        self.orientar()

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
        
    def input(self, evento):
        self.player1.input(evento)
        self.player2.input(evento)
    
    def render(self, screen):
        self.camera.render(screen, self.fundo, (-1000,-1600))
        self.player1.render(screen, self.camera)
        self.player2.render(screen, self.camera)