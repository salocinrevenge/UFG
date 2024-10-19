import pygame

class Botao():
    def __init__(self, x, y, width, height, text, textSize = 36, path = None) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.text = text

        self.rect = pygame.Rect(x, y, width, height)

        self.fonte = pygame.font.Font(None, textSize) 

        self.path = path
        if path:
            try:
                self.img = pygame.image.load(path)
            # se n achar o arquivo
            except FileNotFoundError:
                try:
                    self.img = pygame.image.load("imgs/lutadores/locker_icon.png")
                    text = "Locked"
                except FileNotFoundError as e:
                    print("Arquivos corrompidos, não foi possível carregar a imagem do cadeado")
                    raise e
            self.img = pygame.transform.scale(self.img, (self.width-6, self.height-6))

    def identificaClique(self, pos):
        if self.rect.collidepoint(pos):
            return self.text
        else:
            return False
        
    def render(self, screen):

        if self.rect.collidepoint(pygame.mouse.get_pos()):
            # self.cor = (200, 200, 200)
            self.cor = (90, 180, 90)
        else:
            self.cor = (255, 255, 255)
        # desenha a borda de um retangulo
        pygame.draw.rect(screen, self.cor, self.rect, 3)
        
        if self.path:
            screen.blit(self.img, (self.x+3, self.y+3))
        else:
            # Calcula a posição do texto no centro do botão
            pos_texto = self.rect.centerx - self.fonte.size(self.text)[0] // 2, self.rect.centery - self.fonte.size(self.text)[1] // 2
            
            # Desenha o texto no botão
            screen.blit(self.fonte.render(self.text, True, self.cor), pos_texto)