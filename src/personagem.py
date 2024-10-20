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
        self.orientacao = 0
        self.changeState("Idle M")
        self.anim = 0
        self.tempoAnim = 0
        self.tempoAnimMax = 15
        self.team = team
        self.colision_box = pygame.Rect(self.x+128, self.y, 128, 384)
        self.pulavel = True
        self.deCostas = False
        self.corrige_horizontal = 0
        self.dano = 1
        self.vida_max = 100
        self.vida = self.vida_max
        # pega o nome do name.txt
        self.nome = "Jogador "+str(self.id)
        try:
            with open(f"imgs/lutadores/{self.id}/name.txt") as f:
                self.nome = f.read().strip()
        except FileNotFoundError:
            pass
        self.nome = self.nome + " " + str(self.team+1)
        self.vivo = True

    def damage(self, dano):
        self.vida -= dano
        self.vida = max(0, self.vida)
        self.vida = min(self.vida_max, self.vida)
        if self.vida == 0:
            self.vivo = False

    
    def changeState(self, state):
        self.atack_box = None
        self.anim = 0
        self.STATE = state
        if state+str(self.orientacao) not in self.imagens:
            self.imagens[state+str(self.orientacao)] = []
            for img in sorted(os.listdir(f"imgs/lutadores/{self.id}/{state}/")):
                if self.orientacao == 0:
                    nova_imagem = pygame.image.load(f"imgs/lutadores/{self.id}/{state}/{img}")
                else:
                    nova_imagem = pygame.transform.flip(pygame.image.load(f"imgs/lutadores/{self.id}/{state}/{img}"), True, False)
                self.imagens[state+str(self.orientacao)].append(nova_imagem)
        self.imagem = self.imagens[state+str(self.orientacao)]

    def setDeCostas(self):
        self.deCostas = True

    def criarAtackHitbox(self, largura_atack_box, altura_atack_box, posy):
        if self.orientacao == 0:
            self.atack_box = pygame.Rect(self.x+128-largura_atack_box, self.y+posy, largura_atack_box, altura_atack_box)
        else:
            self.atack_box = pygame.Rect(self.x+self.colision_box.width+128, self.y+posy, largura_atack_box, altura_atack_box)


    def atack_tick(self):
        if self.STATE == "Soco M":
            # cria a hitbox do soco
            if self.anim == 2:
                self.criarAtackHitbox(75, 50, 75)

            # remove a hitbox do soco
            if self.anim == 3:
                self.atack_box = None

        if self.STATE == "Chute M":
            # cria a hitbox do chute
            if self.anim == 2:
                self.criarAtackHitbox(110, 60, 200)


            # remove a hitbox do chute
            if self.anim == 3:
                self.atack_box = None

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
        if self.deCostas:
            if self.anim == 0:
                self.orientacao = 1 - self.orientacao
                self.corrige_horizontal = 128 - self.corrige_horizontal
                self.deCostas = False
                self.changeState(self.STATE)

        self.atack_tick()

    

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

    def renderGUI(self, screen):
        # desenha a barra de vida la em cima e depende do team
        largura_barra = screen.get_width()/2-20
        altura_barra = screen.get_height()/20
        if self.team == 0:
            # fundo
            pygame.draw.rect(screen, (100,100,100), (10, 10, largura_barra, altura_barra))
            largura_vida = (largura_barra * self.vida)//self.vida_max
            cor = (255-int(255*self.vida/self.vida_max),int(255*self.vida/self.vida_max),0)
            pygame.draw.rect(screen, cor, (10-largura_vida+largura_barra, 10, largura_vida, altura_barra))
            # printa o nome do jogador
            font = pygame.font.Font(None, 48)
            text = font.render(self.nome, True, (255, 255, 255))
            screen.blit(text, (10+10, 10+10))
        else:
            pygame.draw.rect(screen, (100,100,100), (screen.get_width()-10-largura_barra, 10, largura_barra, altura_barra))
            largura_vida = (largura_barra * self.vida)//self.vida_max
            cor = (255-int(255*self.vida/self.vida_max),int(255*self.vida/self.vida_max),0)
            pygame.draw.rect(screen, cor, (screen.get_width()-10-largura_barra, 10, largura_vida, altura_barra))
            # printa o nome do jogador
            font = pygame.font.Font(None, 48)
            text = font.render(self.nome, True, (255, 255, 255))
            screen.blit(text, (screen.get_width()-10-largura_barra + 10, 10+10))



    def render(self, screen, camera):
        debug = True
        camera.render(screen, self.imagem[self.anim], (self.x+self.corrige_horizontal, self.y))
        if debug:
            camera.draw_rect(screen, self.colision_box, (255,255,0))
            if self.atack_box != None:
                camera.draw_rect(screen, self.atack_box, (255,0,0))
        self.renderGUI(screen)
