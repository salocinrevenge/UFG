import pygame

class Camera():
    def __init__(self, mundo, pos) -> None:
        self.mundo = mundo
        self.x = pos[0]
        self.y = pos[1]
        self.screen = None
        self.deslocamento_x = 300
        
    def tick(self):
        if self.screen != None:
            self.deslocamento_x = self.screen.get_width()/2
        self.x = (self.mundo.player1.x + self.mundo.player2.x)/2 - self.deslocamento_x + 128*1.8
    
    def render(self, screen, imagem, pos):
        if self.screen == None:
            self.screen = screen
        screen.blit(imagem, (pos[0]-self.x,pos[1]-self.y))

    def draw_rect(self, screen, rect, cor = (255,255,255)):
        rec_desloc = (rect.x - self.x, rect.y - self.y, rect.width, rect.height)
        pygame.draw.rect(screen, cor, rec_desloc, 2)
        
    
    def input(self, evento):
        pass