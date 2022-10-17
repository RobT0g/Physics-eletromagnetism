import pygame
import math

pygame.init()                                                           # inicialização

class Eletroscope:
    def __init__(self) -> None:
        self.size = (500, 700)
        self.display = pygame.display.set_mode(self.size)        # tela definida
        pygame.display.set_caption('Eletroscópio')
        self.genFrame()
        self.charge = 0
        self.putOnScreen()
    
    def genFrame(self):
        self.frame = pygame.Surface(self.size)
        pygame.draw.rect(self.frame, (55, 71, 79), pygame.Rect(0, 0, *self.size))
        pygame.draw.rect(self.frame, (20, 20, 20), pygame.Rect(0, 0, *self.size), 16)
        pygame.draw.rect(self.frame, (50, 50, 50), pygame.Rect(0, 0, *self.size), 1)
        pygame.draw.rect(self.frame, (0, 0, 0), pygame.Rect(15, 15, self.size[0]-30, self.size[1]-30), 1)
        self.eletro = pygame.Surface((200, 500), pygame.SRCALPHA, 32)
        pygame.draw.circle(self.eletro, (134, 133, 129), (100, 100), 100, 10)
        pygame.draw.circle(self.eletro, (0, 0, 0), (100, 100), 90, 2)
        pygame.draw.circle(self.eletro, (0, 0, 0), (100, 100), 100, 2)
        pygame.draw.rect(self.eletro, (55, 71, 79), pygame.Rect(0, 150, 200, 50))
        pygame.draw.line(self.eletro, (184, 115, 51), (100, 10), (100, 300), 10)
        pygame.draw.line(self.eletro, (200, 200, 200), (14, 80), (14, 100), 3)
        pygame.draw.line(self.eletro, (200, 200, 200), (200-14, 80), (200-14, 100), 3)
        sq = pygame.Surface((18, 18))
        pygame.draw.rect(sq, (200, 200, 200), pygame.Rect(0, 0, 17, 17))
        pygame.draw.rect(sq, (0, 0, 0), pygame.Rect(0, 0, 17, 17), 1)
        self.zero = sq.copy()
        pygame.draw.circle(self.zero, (0, 0, 0), (9, 9), 5, 2)
        pygame.draw.line(sq, (0, 0, 0), (3, 8), (14, 8), 2)
        self.msq = sq.copy()
        self.psq = sq.copy()
        pygame.draw.line(self.psq, (0, 0, 0), (8, 3), (8, 14), 2)
    
    def drawSheets(self):
        pos = [
            [(150+163, 150+23), (150+163+20*math.sin(math.radians(self.charge+38)), 150+23+20*math.cos(math.radians(self.charge+38)))], 
            [(250, 451), (250+40*math.sin(math.radians(self.charge)), 451+40*math.cos(math.radians(self.charge))), (250+40*math.sin(math.radians(-self.charge)), 451+40*math.cos(math.radians(-self.charge)))]
        ]
        pygame.draw.line(self.display, (200, 200, 200), pos[0][0], pos[0][1], 3)
        pygame.draw.line(self.display, (200, 200, 200), pos[1][0], pos[1][1], 4)
        pygame.draw.line(self.display, (200, 200, 200), pos[1][0], pos[1][2], 4)

    def update(self):
        pos = pygame.mouse.get_pos()
        if pos[0] > 400 and pos[0] < 418 and pos[1] > 250 and pos[1] < 268 and self.charge < 45:
            self.charge = self.charge+2.5
        if pos[0] > 400 and pos[0] < 418 and pos[1] > 270 and pos[1] < 288 and self.charge > 0:
            self.charge = self.charge-2.5
        if pos[0] > 400 and pos[0] < 418 and pos[1] > 290 and pos[1] < 308:
            self.charge = 0

    def putOnScreen(self):
        self.display.blit(self.frame, (0, 0))
        self.display.blit(self.eletro, (150, 150))
        self.display.blit(self.psq, (400, 250))
        self.display.blit(self.msq, (400, 270))
        self.display.blit(self.zero, (400, 290))
        self.drawSheets()
        pygame.display.flip()

el = Eletroscope()

running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.MOUSEBUTTONDOWN:
            el.update()
            el.putOnScreen()
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            running = False