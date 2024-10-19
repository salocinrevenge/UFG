import pygame
from camera import Camera
from personagem import Personagem

class Mundo():
    def __init__(self, objetos) -> None:
        self.camera = Camera(self,(0,0))
        self.fundo = pygame.image.load(f"imgs/{objetos[0].split()[0]}/{objetos[0].split()[1]}/fundo.png")
        self.player1 = Personagem(objetos[1], (0,500), 0)
        self.player2 = Personagem(objetos[2], (600,500), 1)

    def tick(self):
        pass
        self.camera.tick()
        self.player1.tick()
        self.player2.tick()
        
    def input(self, evento):
        self.player1.input(evento)
        self.player2.input(evento)
    
    def render(self, screen):
        self.camera.render(screen, self.fundo, (0,0))
        self.player1.render(screen, self.camera)
        self.player2.render(screen, self.camera)