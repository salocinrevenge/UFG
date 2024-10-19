import pygame
import os
class Personagem:
    def __init__(self, id, pos, team) -> None:
        self.id = id.split()[1]
        self.imagens = {}
        self.x = pos[0]
        self.y = pos[1]
        self.gravidade = 2

        self.velx = 0
        self.vely = 0
        self.impulso = 10
        self.changeState("Idle M")
        self.anim = 0
        self.tempoAnim = 0
        self.tempoAnimMax = 15
        self.team = team
        self.colision_box = pygame.Rect(self.x+128, self.y, 128, 384)
        self.pulavel = True

    
    def changeState(self, state):
        self.anim = 0
        self.STATE = state
        if state not in self.imagens:
            self.imagens[state] = []
            for img in sorted(os.listdir(f"imgs/lutadores/{self.id}/{state}/")):
                self.imagens[state].append(pygame.image.load(f"imgs/lutadores/{self.id}/{state}/{img}"))
        self.imagem = self.imagens[state]

    def tick(self):
        self.x += self.velx
        self.y += self.vely
        self.y = min(500, self.y)
        self.vely += self.gravidade
        self.vely = min(1000, self.vely)

        if self.velx == 0:
            if self.STATE == "Andar M":
                self.changeState("Idle M")
        else:
            if self.STATE == "Idle M":
                self.changeState("Andar M")

        if abs(self.y - 500) < 3:
            self.pulavel = True

        self.colision_box.x = self.x+128
        self.colision_box.y = self.y

        self.tempoAnim += 1
        if self.tempoAnim >= self.tempoAnimMax:
            self.tempoAnim = 0
            self.anim += 1
            if self.anim >= len(self.imagem):
            # if self.anim >= 2:
                self.anim = 0
                if self.STATE == "Soco M" or self.STATE == "Chute M":
                    self.changeState("Idle M")

    # virgula é pygame.K_COMMA
    controles = {"a": (pygame.K_a, pygame.K_LEFT), "d": (pygame.K_d, pygame.K_RIGHT), "w": (pygame.K_w, pygame.K_UP), "s": (pygame.K_s, pygame.K_DOWN), "f": (pygame.K_f, pygame.K_COMMA), "g": (pygame.K_g, pygame.K_PERIOD), "h": (pygame.K_h, pygame.K_SLASH)}


    def agaixar(self):
        pass

    def levantar(self):
        pass

    def saltar(self):
        if self.pulavel:
            self.vely = -45
            self.pulavel = False

    def soco(self):
        self.changeState("Soco M")
    
    def chute(self):
        self.changeState("Chute M")

    def defender(self):
        self.changeState("Defesa M")

    def input(self, evento):

        if evento.type == pygame.KEYDOWN:
            if evento.key == self.controles["a"][self.team]:
                self.velx += -self.impulso
                self.changeState("Andar M")
            if evento.key == self.controles["d"][self.team]:
                self.velx += self.impulso
                self.changeState("Andar M")
            if evento.key == self.controles["w"][self.team]:
                self.saltar()
            if evento.key == self.controles["s"][self.team]:
                self.agaixar()

            if evento.key == self.controles["f"][self.team]:
                self.soco()
            if evento.key == self.controles["g"][self.team]:
                self.chute()
            # if evento.key == self.controles["h"][self.team]:
            #     self.defender()

        if evento.type == pygame.KEYUP:
            if evento.key == self.controles["a"][self.team]:
                self.velx += self.impulso
                self.changeState("Andar M")
            if evento.key == self.controles["d"][self.team]:
                self.velx += -self.impulso
                self.changeState("Andar M")
            if evento.key == self.controles["s"][self.team]:
                self.levantar()

            # if evento.key == self.controles["h"][self.team]:
            #     self.soltarDefesa()

    def render(self, screen, camera):
        debug = True
        if debug:
            camera.render(screen, self.imagem[self.anim], (self.x, self.y), self.colision_box)
        else:
            camera.render(screen, self.imagem[self.anim], (self.x, self.y))
