import pygame
from camera import Camera
from personagem import Personagem

class Mundo():
    def __init__(self, objetos) -> None:
        self.camera = Camera(self,(0,0))
        self.fundo = pygame.image.load(f"imgs/{objetos[0].split()[0]}/{objetos[0].split()[1]}/fundo.png")
        self.player1 = Personagem(objetos[1])
        self.player2 = Personagem(objetos[2])

    def tick(self):
        pass
        self.camera.tick()
        
    def input(self, evento):
        pass
    
    def render(self, screen):
        self.camera.render(screen, self.fundo, (0,0))
        self.player1.render(screen, self.camera)