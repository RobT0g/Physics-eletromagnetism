from email.mime import base
import pygame

class Bars:
    def __init__(self, posup=True, charge=True) -> None:
        self.dimensions = (75*12+32, 75*8+32)
        self.display = pygame.display.set_mode(self.dimensions)
        self.posup = posup
        self.mm = 50/(self.dimensions[0]-100)
        self.barpos = 30
        self.chargeSign = charge
        self.origin = [50, self.dimensions[1]-80]
        self.chargePos = self.origin[:]
        self.font = pygame.font.SysFont('Times New Roman', 14)
        self.fontL = pygame.font.SysFont('Times New Roman', 18)
        self.adjusting = True
        self.btn = None
        self.finished = False
        self.modsToBtn = {
            'char': [500, 10],                  #*e
            'fiel': [2.85, 0.1],                #*10^-13N/C
            'spdx': [0.25, 0.01],               #m/s
            'spdy': [0.2, 0.01]                 #m/s
        }
        self.limitsValues = {
            'char': [500, 600], 
            'fiel': [2.85, 3.55], 
            'spdx': [0.15, 0.25], 
            'spdy': [0.10, 0.4]
        }
        self.bCharge = 1.6                              #*10^-19 C
        self.mass = self.modsToBtn['char'][0]*9.1*0.25  #*10^-31 Kg
        self.tick = 5                               #s
        self.accel = self.modsToBtn['char'][0]*self.bCharge*self.modsToBtn['fiel'][0]/self.mass     #*10^-1 m/s²
        self.genGraphStuff()
        self.putOnScreen()
    
    def genGraphStuff(self):
        self.frame = pygame.Surface(self.dimensions)
        pygame.draw.rect(self.frame, (0, 0, 0), pygame.Rect(0, 0, *self.dimensions), 1)
        pygame.draw.rect(self.frame, (132, 86, 43), pygame.Rect(1, 1, self.dimensions[0]-2, self.dimensions[1]-2), 14)
        pygame.draw.rect(self.frame, (0, 0, 0), pygame.Rect(15, 15, self.dimensions[0]-30, self.dimensions[1]-30), 1)
        pygame.draw.rect(self.frame, (55, 71, 79), pygame.Rect(16, 16, self.dimensions[0]-32, self.dimensions[1]-32))
        bar = pygame.Surface((self.dimensions[0]-32, 20), pygame.SRCALPHA, 32)
        pygame.draw.rect(bar, (113, 121, 126), pygame.Rect(0, 0, self.dimensions[0]-32, 20))
        pygame.draw.rect(bar, (0, 0, 0), pygame.Rect(-1, 0, self.dimensions[0]-30, 20), 1)
        positive = pygame.Surface((20, 20), pygame.SRCALPHA, 32)
        pygame.draw.line(positive, (0, 0, 0), (4, 9), (17, 9), 2)
        negative = positive.copy()
        pygame.draw.line(positive, (0, 0, 0), (10, 3), (10, 16), 2)
        posbar = bar.copy()
        negbar = bar.copy()
        amnt = 20
        step = (self.dimensions[0]-32)/amnt
        for i in range(amnt):
            posbar.blit(positive, (i*step+8, 0))
            negbar.blit(negative, (i*step+8, 0))
        self.orderOfCharge = [posbar, negbar] if self.posup else [negbar, posbar]
        self.charge = pygame.Surface((30, 30), pygame.SRCALPHA, 32)
        pygame.draw.circle(self.charge, (212, 175, 55), (15, 15), 15)
        pygame.draw.circle(self.charge, (0, 0, 0), (15, 15), 15, 2)
        self.charge.blit(positive if self.chargeSign else negative, (4, 5))
        sq = pygame.Surface((18, 18))
        pygame.draw.rect(sq, (200, 200, 200), pygame.Rect(0, 0, 17, 17))
        pygame.draw.rect(sq, (0, 0, 0), pygame.Rect(0, 0, 17, 17), 1)
        pygame.draw.line(sq, (0, 0, 0), (3, 8), (14, 8), 2)
        self.msq = sq.copy()
        self.psq = sq.copy()
        pygame.draw.line(self.psq, (0, 0, 0), (8, 3), (8, 14), 2)

    def drawAxis(self):
        pygame.draw.line(self.display, (200, 200, 200), (25, self.origin[1]-1), (self.dimensions[0]-25, self.origin[1]-1), 2)
        pygame.draw.line(self.display, (200, 200, 200), (self.origin[0]-1, 25), (self.origin[0]-1, self.dimensions[1]-25), 2)
        pygame.draw.line(self.display, (200, 200, 200), (self.origin[0]+(50/self.mm), self.origin[1]-2), (self.origin[0]+(50/self.mm), self.origin[1]+24), 2)
        self.display.blit((txt:=self.font.render(f'50.0', False, (200, 200, 200))), (self.origin[0]+(50/self.mm)-((s:=txt.get_size())[0]/2), self.origin[1]+25))

    def clickedOn(self):
        pos = pygame.mouse.get_pos()
        for i in self.btn:
            if pos[0] > self.btn[i][0][0] and pos[0] < self.btn[i][1][0] and pos[1] > self.btn[i][0][1] and pos[1] < self.btn[i][1][1]:
                return i
        return None

    def setVars(self):
        #try:
            opt = self.btn[self.clickedOn()][2]
            print(opt)
            if(opt[0] == 'init'):
                self.adjusting = False
                return
            if opt[1] and self.modsToBtn[opt[0]][0] < self.limitsValues[opt[0]][1]:
                self.modsToBtn[opt[0]][0] += self.modsToBtn[opt[0]][1]
            elif not opt[1] and self.modsToBtn[opt[0]][0] > self.limitsValues[opt[0]][0]:
                self.modsToBtn[opt[0]][0] -= self.modsToBtn[opt[0]][1]
            if opt[0] == 'char' or opt[0] == 'fiel':
                self.mass = self.modsToBtn['char'][0]*9.1*0.25
                self.accel = self.modsToBtn['char'][0]*self.bCharge*self.modsToBtn['fiel'][0]/self.mass
                print(self.accel)
        #except Exception as e:
        #    print('ERROR ', e)
        #    pass


    def showUi(self):
        basepos = (-100+self.dimensions[0]/2, -50+self.dimensions[1]/2)
        self.display.blit((bs:=self.fontL.render(f'''Carga       {self.modsToBtn['char'][0]}*e''', False, (200, 200, 200))), basepos)
        baseSize = bs.get_size()
        self.display.blit(self.psq, (basepos[0]+baseSize[0]+10, basepos[1]+2))
        self.display.blit(self.msq, (basepos[0]+baseSize[0]+30, basepos[1]+2))
        self.display.blit((t:=self.fontL.render(f'''Campo  {self.modsToBtn['fiel'][0]:.2f}E-13''', False, (200, 200, 200))), (basepos[0]+baseSize[0]-t.get_size()[0], basepos[1]+baseSize[1]))
        self.display.blit(self.psq, (basepos[0]+baseSize[0]+10, basepos[1]+baseSize[1]+2))
        self.display.blit(self.msq, (basepos[0]+baseSize[0]+30, basepos[1]+baseSize[1]+2))
        self.display.blit((t:=self.fontL.render(f'''Vx     {self.modsToBtn['spdx'][0]:.2f}m/s''', False, (200, 200, 200))), (basepos[0]+baseSize[0]-t.get_size()[0], basepos[1]+2*baseSize[1]))
        self.display.blit(self.psq, (basepos[0]+baseSize[0]+10, basepos[1]+2*baseSize[1]+2))
        self.display.blit(self.msq, (basepos[0]+baseSize[0]+30, basepos[1]+2*baseSize[1]+2))
        self.display.blit((t:=self.fontL.render(f'''Vy     {self.modsToBtn['spdy'][0]:.2f}m/s''', False, (200, 200, 200))), (basepos[0]+baseSize[0]-t.get_size()[0], basepos[1]+3*baseSize[1]))
        self.display.blit(self.psq, (basepos[0]+baseSize[0]+10, basepos[1]+3*baseSize[1]+2))
        self.display.blit(self.msq, (basepos[0]+baseSize[0]+30, basepos[1]+3*baseSize[1]+2))
        txt = self.fontL.render(f'Iniciar', False, (200, 200, 200))
        pygame.draw.rect(self.display, (0, 0, 0), pygame.Rect(basepos[0]+40, basepos[1]+5*baseSize[1]-5, (s:=txt.get_size())[0]+20, s[1]+10))
        pygame.draw.rect(self.display, (200, 200, 200), pygame.Rect(basepos[0]+40, basepos[1]+5*baseSize[1]-5, (s:=txt.get_size())[0]+20, s[1]+10), 2)
        self.display.blit(txt, (basepos[0]+50, basepos[1]+5*baseSize[1]))
        if not self.btn:
            self.btn = {
                'charp': [(p:=(basepos[0]+baseSize[0]+10, basepos[1]+2)), (p[0]+18, p[1]+18), ('char', True)], 
                'charm': [(p:=(basepos[0]+baseSize[0]+30, basepos[1]+2)), (p[0]+18, p[1]+18), ('char', False)], 
                'fielp': [(p:=(basepos[0]+baseSize[0]+10, basepos[1]+baseSize[1]+2)), (p[0]+18, p[1]+18), ('fiel', True)], 
                'fielm': [(p:=(basepos[0]+baseSize[0]+30, basepos[1]+baseSize[1]+2)), (p[0]+18, p[1]+18), ('fiel', False)], 
                'spdxp': [(p:=(basepos[0]+baseSize[0]+10, basepos[1]+2*baseSize[1]+2)), (p[0]+18, p[1]+18), ('spdx', True)], 
                'spdxm': [(p:=(basepos[0]+baseSize[0]+30, basepos[1]+2*baseSize[1]+2)), (p[0]+18, p[1]+18), ('spdx', False)], 
                'spdyp': [(p:=(basepos[0]+baseSize[0]+10, basepos[1]+3*baseSize[1]+2)), (p[0]+18, p[1]+18), ('spdy', True)], 
                'spdym': [(p:=(basepos[0]+baseSize[0]+30, basepos[1]+3*baseSize[1]+2)), (p[0]+18, p[1]+18), ('spdy', False)],
                'inita': [(basepos[0]+40, basepos[1]+5*baseSize[1]-5), (basepos[0]+40+(s:=txt.get_size())[0]+20, basepos[1]+5*baseSize[1]-5+s[1]+10), ('init', True)]
            }
        
    def recalc(self):
        if self.finished == True:
            return
        self.chargePos[0] += self.modsToBtn['spdx'][0]*self.tick/self.mm
        self.chargePos[1] -= self.modsToBtn['spdy'][0]*self.tick/self.mm
        #self.modsToBtn['spdy'][0] -= self.accel*0.1*self.tick
        if (self.chargePos[1] <= self.barpos) and (self.modsToBtn['spdy'][0] >= 0):
            self.finished = True
            self.chargePos[1] = self.barpos
        if (self.chargePos[1] >= self.origin[1]) and (self.modsToBtn['spdy'][0] <= 0):
            self.finished = True
            self.chargePos[1] = self.origin[1]
            return

    def showDistances(self):
        self.display.blit((p:=self.font.render(f'({(self.chargePos[0]-self.origin[0])*self.mm:.0f}, {(self.chargePos[1]-self.origin[1])*self.mm:.0f})', False, (200, 200, 200))),
            (self.chargePos[0]-2-p.get_size()[0], self.chargePos[1]-30))
        pygame.draw.line(self.display, (9, 151, 193), (self.chargePos[0], self.chargePos[1]-1), ((self.modsToBtn['spdx'][0]*75/self.limitsValues['spdx'][1])+self.chargePos[0], self.chargePos[1]-1), 2)
        pygame.draw.line(self.display, (9, 151, 193), (self.chargePos[0]-1, self.chargePos[1]), (self.chargePos[0]-1, (-self.modsToBtn['spdy'][0]*75/self.limitsValues['spdy'][1])+self.chargePos[1]), 2)

    def update(self):
        if self.adjusting:
            return
        self.recalc()
        self.putOnScreen()
        

    def refresh(self):
        self.setVars()
        self.putOnScreen()

    def putOnScreen(self):
        self.display.blit(self.frame, (0, 0))
        self.display.blit(self.orderOfCharge[0], (16, self.barpos))
        self.display.blit(self.orderOfCharge[1], (16, self.origin[1]))
        self.drawAxis()
        self.showDistances()
        self.display.blit(self.charge, (self.chargePos[0]-15, self.chargePos[1]-15))
        if self.adjusting:
            self.showUi()
        pygame.display.flip()
        

