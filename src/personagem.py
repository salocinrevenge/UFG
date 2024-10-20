import pygame
import os
from projetil import ProjetilLateral, ProjetilCeu, ProjetilArea

class Personagem:
    def __init__(self, id, pos, team, debug = False) -> None:
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
        self.tempoAnimMax = {"Idle M": 15, "Andar M": 10, "Soco M": 5, "Chute M": 10, "Defesa M": 1}
        self.danos = {"Soco M": 1, "Chute M": 2}
        self.team = team
        self.colision_box = pygame.Rect(self.x+128, self.y, 128, 384)
        self.pulavel = True
        self.deCostas = False
        self.corrige_horizontal = 0
        self.vida_max = 200
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

        self.projetils_lancados = []

        self.combos = []
        self.maior_combo = 0
        self.lidos = []
        try:
            with open(f"imgs/lutadores/{self.id}/combos.txt") as f:
                combosLidos = f.read().strip().split()
                for i in range(len(combosLidos)):
                    match i%3:
                        case 0:
                            self.combos.append([combosLidos[i]])
                        case 1: 
                            continue
                        case 2:
                            self.combos[-1].append(combosLidos[i])
                            self.maior_combo = max(self.maior_combo, len(combosLidos[i]))

                print(combosLidos)
        except FileNotFoundError:
            pass
        self.debug = debug

    def damage(self, dano):
        if self.defendendo:
            dano = dano//2
        self.vida -= dano
        self.vida = max(0, self.vida)
        self.vida = min(self.vida_max, self.vida)
        if self.vida == 0:
            self.vivo = False

    
    def changeState(self, state):
        self.atack_box = None
        self.anim = 0
        self.STATE = state
        self.defendendo = False
        if state == "Defesa M":
            self.defendendo = True
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

    def verificadorCombo(self):
        for combo in self.combos:
            # converte lidos para string
            lido = ""
            for elem in range(len(self.lidos)):
                letra = self.codificacaoInversa[self.team][self.lidos[elem]]
                if self.orientacao == 0:
                    if letra == "a":
                        letra = "d"
                    elif letra == "d":
                        letra = "a"
                lido += letra

            # print(combo, lido)
            if lido == combo[1]:
                match combo[0]:
                    case '1':
                        self.feiticoFrente()
                    case '2':
                        self.feiticoCeu()
                    case '3':
                        self.feiticoArea()
                    case _:
                        raise Exception("Combo não implementado")
                self.lidos = []

    altura_braco = 75

    def atack_tick(self):
        if self.STATE == "Soco M":
            # cria a hitbox do soco
            if self.anim == 2:
                self.criarAtackHitbox(75, 50, self.altura_braco)

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
        if self.tempoAnim >= self.tempoAnimMax[self.STATE]:
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
        self.verificadorCombo()
    

    controles = {"a": (pygame.K_a, pygame.K_LEFT), "d": (pygame.K_d, pygame.K_RIGHT), "w": (pygame.K_w, pygame.K_UP), "s": (pygame.K_s, pygame.K_DOWN), "f": (pygame.K_f, pygame.K_COMMA), "g": (pygame.K_g, pygame.K_PERIOD), "h": (pygame.K_h, pygame.K_SEMICOLON)}
    todos_controles = ((pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_f, pygame.K_g, pygame.K_h), 
                        (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_COMMA, pygame.K_PERIOD, pygame.K_SEMICOLON))
    
    codificacaoInversa = ({pygame.K_a: "a", pygame.K_d: "d", pygame.K_w: "w", pygame.K_s: "s", pygame.K_f: "f", pygame.K_g: "g", pygame.K_h: "h"},{pygame.K_LEFT: "a", pygame.K_RIGHT: "d", pygame.K_UP: "w", pygame.K_DOWN: "s", pygame.K_COMMA: "f", pygame.K_PERIOD: "g", pygame.K_SEMICOLON: "h"})

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
    
    def soltarDefesa(self):
        self.changeState("Idle M")

    def feiticoFrente(self):
        largura_projetil = 32
        if self.orientacao == 0:
            projetil = ProjetilLateral(self.x+128//2-largura_projetil, self.y+self.altura_braco, self.orientacao, f"imgs/lutadores/{self.id}/projetilLateral.png", largura_projetil, self.debug)
        else:
            projetil = ProjetilLateral(self.x+self.colision_box.width+128+ 128//2, self.y+self.altura_braco, self.orientacao, f"imgs/lutadores/{self.id}/projetilLateral.png", largura_projetil, self.debug)

        self.projetils_lancados.append(projetil)

    def feiticoCeu(self):
        projetil = ProjetilCeu(self.x, self.y, self.orientacao)
        self.projetils_lancados.append(projetil)

    def feiticoArea(self):
        projetil = ProjetilArea(self.x, self.y, self.orientacao)
        self.projetils_lancados.append(projetil)

    def input(self, evento):

        if evento.type == pygame.KEYDOWN:
            if evento.key in self.todos_controles[self.team]:
                self.lidos.append(evento.key)
                if len(self.lidos) > self.maior_combo:
                    self.lidos.pop(0)
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
            if evento.key == self.controles["h"][self.team]:
                self.defender()

        if evento.type == pygame.KEYUP:
            if evento.key == self.controles["a"][self.team]:
                self.velx += self.impulso
                self.changeState("Andar M")
            if evento.key == self.controles["d"][self.team]:
                self.velx += -self.impulso
                self.changeState("Andar M")
            if evento.key == self.controles["s"][self.team]:
                self.levantar()

            if evento.key == self.controles["h"][self.team]:
                self.soltarDefesa()

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
        camera.render(screen, self.imagem[self.anim], (self.x+self.corrige_horizontal, self.y))
        if self.debug:
            camera.draw_rect(screen, self.colision_box, (255,255,0))
            if self.atack_box != None:
                camera.draw_rect(screen, self.atack_box, (255,0,0))
        self.renderGUI(screen)
