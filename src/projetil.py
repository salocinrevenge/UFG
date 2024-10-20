import pygame

class ProjetilLateral:
    def __init__(self, x, y, orientacao, path, tamanho = 32, debug = False, dano = 10):
        self.x = x
        self.y = y
        self.orientacao = orientacao
        self.velx = -1 if orientacao == 0 else 1
        self.tempo = 0
        self.vivo = True
        self.imagem = pygame.image.load(path)
        # um quarto do tamanho
        self.imagem = pygame.transform.scale(self.imagem, (tamanho, tamanho))
        self.debug = debug
        self.colision_box = pygame.Rect(self.x, self.y, tamanho, tamanho)
        self.dano = dano

    def atingiu(self):
        self.dano = 0
        self.vivo = False

    def tick(self):
        self.x += self.velx
        self.colision_box.x = self.x
        self.tempo += 1
        if self.tempo > 10000:
            self.vivo = False

    def render(self, screen, camera):
        screen.blit(self.imagem, (self.x - camera.x, self.y - camera.y))
        if self.debug:
            camera.draw_rect(screen, self.colision_box, (255,0,0))

class ProjetilCeu:
    def __init__(self, x, y, orientacao, path):
        self.x = x
        self.y = y
        self.orientacao = orientacao
        self.vely = 10
        self.tempo = 0
        self.vivo = True
        self.path = path
        self.imagem = pygame.image.load(path)

    def tick(self):
        self.y += self.vely
        self.tempo += 1
        if self.tempo > 100:
            self.vivo = False

    def render(self, screen, camera):
        screen.blit(self.imagem, (self.x - camera.x, self.y - camera.y))

class ProjetilArea:
    def __init__(self, x, y, raio, path, raio_crescimento = 0):
        self.x = x
        self.y = y
        self.raio = raio
        self.tempo = 0
        self.vivo = True
        self.raio_crescimento = raio_crescimento
        self.imagem = pygame.image.load(path)

    def tick(self):
        self.raio += self.raio_crescimento
        self.tempo += 1
        if self.tempo > 100:
            self.vivo = False

    def render(self, screen, camera):
        screen.blit(self.imagem, (self.x - camera.x, self.y - camera.y))
        print("pao")
        if self.debug:
            print("be")
            camera.draw_rect(screen, self.colision_box, (255,255,255))