import pygame

class Mundo():
    def __init__(self) -> None:
        pass

    def tick(self):
        pass
        self.camera.tick()
        
    def input(self, evento):
        posCentral = self.salaAtual.getPos()
        for i in range(-self.renderDistance,self.renderDistance+1):
            for j in range(-self.renderDistance,self.renderDistance+1):
                if i+posCentral[0] < 0 or i+posCentral[0] >= len(self.salas) or j+posCentral[1] < 0 or j+posCentral[1] >= len(self.salas[0]):
                    continue
                self.salas[i+posCentral[0]][j+posCentral[1]].input(evento)
    
    def render(self, screen):
        screen.fill((200,255,255))