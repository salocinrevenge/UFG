import pygame

class Choice():
    def __init__(self, posicoes, index, width, height, nome, cor = (255, 0, 0), tamanho = 45):
        self.posicoes = posicoes
        self.index = index
        self.width = width
        self.height = height
        self.nome = nome
        self.cor = cor
        self.tamanho = tamanho

    def render(self, screen):
        pygame.draw.rect(screen, self.cor, pygame.Rect(self.posicoes[self.index][0]-2, self.posicoes[self.index][1]-2, self.width, self.height), 5)
        # desenha um fundo pro nome
        pygame.draw.rect(screen, self.cor, pygame.Rect(self.posicoes[self.index][0]-2, self.posicoes[self.index][1] - 30, self.width, 30))
        # desenha o nome dele em cima
        screen.blit(pygame.font.Font(None, self.tamanho).render(self.nome, True, (255,255,255)), (self.posicoes[self.index][0]+5, self.posicoes[self.index][1] - 30))

    def input(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                self.index -= 1
            if evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                self.index += 1
            if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                self.index -= 3
            if evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                self.index += 3
            if self.index < 0:
                self.index = 0
            if self.index >= len(self.posicoes):
                self.index = len(self.posicoes) - 1