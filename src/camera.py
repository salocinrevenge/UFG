import pygame

class Camera():
    def __init__(self, mundo, pos) -> None:
        self.mundo = mundo
        self.x = pos[0]
        self.y = pos[1]
        
    def tick(self):
        # deslSala = self.target.mundo.deslocamentoSala()
        pass
    
    def render(self, screen, imagem, pos, colisao = None):
        screen.blit(imagem, (pos[0],pos[1]))
        if colisao:
            pygame.draw.rect(screen, (255,0,0), colisao, 2)
        
    
    def input(self, evento):
        pass