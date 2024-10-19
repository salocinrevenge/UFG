import pygame
import os
class Personagem:
    def __init__(self, id, pos, team) -> None:
        self.id = id.split()[1]
        self.imagens = {}
        self.x = pos[0]
        self.y = pos[1]

        self.velx = 0
        self.vely = 0
        self.impulso = 10
        self.changeState("Andar M")
        self.anim = 0
        self.tempoAnim = 0
        self.tempoAnimMax = 20
        self.team = team
        self.colision_box = pygame.Rect(self.x+64, self.y, 128, 384)

    
    def changeState(self, state):
        self.STATE = state
        if state not in self.imagens:
            self.imagens[state] = []
            for img in sorted(os.listdir(f"imgs/lutadores/{self.id}/{state}/")):
                self.imagens[state].append(pygame.image.load(f"imgs/lutadores/{self.id}/{state}/{img}"))
        self.imagem = self.imagens[state]

    def tick(self):
        self.x += self.velx
        self.y += self.vely

        self.colision_box.x = self.x+64
        self.colision_box.y = self.y

        self.tempoAnim += 1
        if self.tempoAnim >= self.tempoAnimMax:
            self.tempoAnim = 0
            self.anim += 1
            # if self.anim >= len(self.imagem):
            if self.anim >= 2:
                self.anim = 0

    controles = {"a": (pygame.K_a, pygame.K_LEFT), "d": (pygame.K_d, pygame.K_RIGHT), "w": (pygame.K_w, pygame.K_UP), "s": (pygame.K_s, pygame.K_DOWN)}


    def agaixar(self):
        pass

    def levantar(self):
        pass

    def saltar(self):
        self.vely = -20

    def input(self, evento):

        if evento.type == pygame.KEYDOWN:
            if evento.key == self.controles["a"][self.team]:
                self.velx += -self.impulso
            if evento.key == self.controles["d"][self.team]:
                self.velx += self.impulso
            if evento.key == self.controles["w"][self.team]:
                self.saltar()
            if evento.key == self.controles["s"][self.team]:
                self.agaixar()
        if evento.type == pygame.KEYUP:
            if evento.key == self.controles["a"][self.team]:
                self.velx += self.impulso
            if evento.key == self.controles["d"][self.team]:
                self.velx += -self.impulso
            if evento.key == self.controles["s"][self.team]:
                self.levantar()

    def render(self, screen, camera):
        debug = True
        if debug:
            camera.render(screen, self.imagem[self.anim], (self.x, self.y), self.colision_box)
        else:
            camera.render(screen, self.imagem[self.anim], (self.x, self.y))
