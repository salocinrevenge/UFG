import pygame

class Personagem:
    def __init__(self, id) -> None:
        self.id = id
        self.imagens = {}
        self.x = 0
        self.y = 0
        self.changeState("Idle")
    
    def changeState(self, state):
        self.STATE = state
        if state not in self.imagens:
            self.imagens[state] = pygame.image.load(f"imgs/lutadores/{self.id}/{state}.png")
        self.imagem = self.imagens[state]

    def render(self, screen, camera):
        camera.render(screen, self.imagem, (self.x, self.y))
