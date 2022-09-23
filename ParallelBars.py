import pygame

class Bars:
    def __init__(self, posup=True, charge=True) -> None:
        self.dimensions = (75*12+32, 75*8+32)
        self.display = pygame.display.set_mode(self.dimensions)
        self.posup = posup
        self.barlen = 600
        self.barx = (self.dimensions[0]-self.barlen)-50
        self.barPos = [50, self.dimensions[1]-50]
        self.mm = 50/(self.barPos[1]-self.barPos[0])
        self.chargeSign = charge
        self.origin = [80, self.barPos[1]]
        self.chargePos = self.origin[:]
        self.font = pygame.font.SysFont('Times New Roman', 14)
        self.genGraphStuff()
        self.putOnScreen()
    
    def genGraphStuff(self):
        self.frame = pygame.Surface(self.dimensions)
        pygame.draw.rect(self.frame, (0, 0, 0), pygame.Rect(0, 0, *self.dimensions), 1)
        pygame.draw.rect(self.frame, (132, 86, 43), pygame.Rect(1, 1, self.dimensions[0]-2, self.dimensions[1]-2), 14)
        pygame.draw.rect(self.frame, (0, 0, 0), pygame.Rect(15, 15, self.dimensions[0]-30, self.dimensions[1]-30), 1)
        pygame.draw.rect(self.frame, (55, 71, 79), pygame.Rect(16, 16, self.dimensions[0]-32, self.dimensions[1]-32))
        self.bar = pygame.Surface((self.barlen, 20), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.bar, (0, 0, 0), pygame.Rect(10, 0, self.barlen-20, 20), 2)
        pygame.draw.circle(self.bar, (132, 86, 43), (10, 10), 10)
        pygame.draw.circle(self.bar, (0, 0, 0), (10, 10), 10, 2)
        pygame.draw.circle(self.bar, (132, 86, 43), (self.barlen-10, 10), 10)
        pygame.draw.circle(self.bar, (0, 0, 0), (self.barlen-10, 10), 10, 2)
        pygame.draw.rect(self.bar, (132, 86, 43), pygame.Rect(8, 2, self.barlen-16, 16))
        amnt = -2+(self.barlen//20)
        positive = pygame.Surface((20, 20), pygame.SRCALPHA, 32)
        pygame.draw.line(positive, (0, 0, 0), (4, 9), (17, 9), 2)
        negative = positive.copy()
        pygame.draw.line(positive, (0, 0, 0), (10, 3), (10, 16), 2)
        posbar = pygame.Surface((self.barlen, 20), pygame.SRCALPHA, 32)
        negbar = pygame.Surface((self.barlen, 20), pygame.SRCALPHA, 32)
        step = self.barlen/amnt
        for i in range(amnt):
            posbar.blit(positive, (i*step, 0))
            negbar.blit(negative, (i*step, 0))
        self.orderOfCharge = [posbar, negbar] if self.posup else [negbar, posbar]
        self.charge = pygame.Surface((30, 30), pygame.SRCALPHA, 32)
        pygame.draw.circle(self.charge, (132, 86, 43), (15, 15), 15)
        pygame.draw.circle(self.charge, (0, 0, 0), (15, 15), 15, 2)
        self.charge.blit(positive if self.chargeSign else negative, (4, 5))

    def drawAxis(self):
        pygame.draw.line(self.display, (200, 200, 200), (25, self.origin[1]-1), (self.dimensions[0]-25, self.origin[1]-1), 2)
        pygame.draw.line(self.display, (200, 200, 200), (self.origin[0]-1, 25), (self.origin[0]-1, self.dimensions[1]-25), 2)
        pygame.draw.line(self.display, (200, 200, 200), (self.barx, self.barPos[1]-5), (self.barx, self.barPos[1]+10), 2)
        self.display.blit((p:=self.font.render(f'{(self.barx-self.origin[0])*self.mm:.1f}', False, (200, 200, 200))), (self.barx-p.get_size()[0]/2, self.barPos[1]+12))
        pygame.draw.line(self.display, (200, 200, 200), (self.origin[0]+2, self.barPos[0]), (self.origin[0]-2, self.barPos[0]))
        self.display.blit((p:=self.font.render(f'{(self.origin[1]-self.barPos[0])*self.mm:.1f}', False, (200, 200, 200))), (self.origin[0]-(s:=p.get_size())[0]-4, self.barPos[0]-s[1]/2))


    def showDistances(self):
        self.display.blit((p:=self.font.render(f'({(self.chargePos[0]-self.origin[0])*self.mm:.1f}, {(self.chargePos[1]-self.origin[1])*self.mm:.1f})', False, (200, 200, 200))),
            (self.chargePos[0]-2-p.get_size()[0], self.chargePos[1]-30))

    def update(self):
        pass

    def putOnScreen(self):
        self.display.blit(self.frame, (0, 0))
        self.drawAxis()
        self.display.blit(self.bar, (self.barx, self.barPos[0]-10))
        self.display.blit(self.bar, (self.barx, self.barPos[1]-10))
        self.display.blit(self.orderOfCharge[0], (self.barx, self.barPos[0]-10))
        self.display.blit(self.orderOfCharge[1], (self.barx, self.barPos[1]-10))
        self.display.blit(self.charge, (self.chargePos[0]-15, self.chargePos[1]-15))
        self.showDistances()
        pygame.display.flip()
        

