# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 04:22:21 2024

@author: emree
"""

import pygame
import math
from math import pi
import time

from tensorflow.keras.models import load_model
import numpy as np
 
import os
import sys

script_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_dir)

saveImg=False

actions=[]

WIDTH=1420
HEIGHT=850
FPS=10
SCALE=40

#ekran 480*360
#colors
WHITE=(255,255,255)
BLACK=(0,0,0)
COL1=(155,155,155)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
FON=(177,221,240)
FON2=(120,200,230)
COL2=(30,120,160)
COL3=(150,0,0)
model1Clr=(31,119,180)
model2Clr=(255,127,14)
model3Clr=(44,160,44)
DEGER=0

clrList=[[(250,215,172),(180,101,4)],
         [(250,217,212),(174,65,50)],
         [(176,227,230),(14,128,136)],
         [(177,221,240),(16,115,158)],
         [(208,206,226),(86,81,126)],
         [(186,200,211),(35,68,93)],
         [(227,200,0),(176,149,0)],
         [(178,43,76),(255,0,0)],
         [(171,161,226),(0,110,175)],
         [(109,135,100),(58,84,49)]]

LIMIT=[50,1050,50,800]
FREQ=433*pow(10,6)
GTX=2
GRX=2

# load model
modelA = load_model('model_dataSet_3L.h5')

model3L = load_model('model_dataSet_3L.h5')
model5L = load_model('model_dataSet_5L.h5')
model9L = load_model('model_dataSet_9L.h5')
# summarize model.
# modelA.summary()


scrnClr= [[[0,0,0] for _ in range(HEIGHT)] for _ in range(WIDTH)]


def normalize(deger,inMin,inMax,outMin,outMax):
    x=deger
    sonuc=(x-inMin)*(outMax-outMin)/(inMax-inMin)+outMin  
    return sonuc

def valueCreate(SigVal,numL):
    sigList=[] 
    if numL==3:
        normC=[[ -157.467, -50.365],[-143.356, -50.365],[ -160.856, -50.365]]
    if numL==5:
        normC=[[ -162.438, -50.365],[ -157.467, -50.365],[ -143.356, -50.365],[ -159.754, -50.365],[ -139.736, -48.183]]
    if numL==9:
        normC=[[ -162.438, -50.365],[ -166.113, -47.867],[ -157.467, -50.365],[ -163.298, -49.067],[ -143.356, -50.365],[ -191.505, -47.867],[ -159.754, -50.365],[ -160.856, -50.365],[ -139.736, -48.183]]
        
    # normC=[[-169.393, -50.365],[-231.352, -47.867],[-139.221, -49.869],[-131.514, -49.067],[-146.181, -49.869],[ -173.294, -47.867],[-153.171, -50.365],[ -139.708, -48.486999999999995],[-166.15, -48.183]]
    for i in range(0, len(SigVal)):
        sigList.append(normalize(SigVal[i],normC[i][0],normC[i][1],0,1))    
    return [sigList]

def valueCreate3L(SigVal):
    sigList=[] 
    normC=[[ -81.404, -50.365],[ -81.404, -50.365],[ -78.525, -48.486999999999995]]
    
    for i in range(0, len(SigVal)):
        sigList.append(normalize(SigVal[i],normC[i][0],normC[i][1],0,1))    
    return [sigList]

class lacationData(pygame.sprite.Sprite):
    
    def __init__(self, LLab="Location",pos=(1260,95),clrSlct=7):
        pygame.sprite.Sprite.__init__(self)
        
        # self.image = pygame.image.load(r'img\2.png')
        self.image=pygame.Surface((285,90))
        self.image.fill(clrList[clrSlct][0])
        pygame.draw.rect(self.image, WHITE, (0,60,285,30))        
        pygame.draw.rect(self.image, clrList[clrSlct][1], (0,0,285,89),2)
        pygame.draw.rect(self.image, clrList[clrSlct][1], (0,0,285,29),2)
        pygame.draw.rect(self.image, clrList[clrSlct][1], (0,59,285,29),2)
        pygame.draw.rect(self.image, clrList[clrSlct][1], (142,27,143,61),2)
        self.rect=self.image.get_rect()
        
        self.rect.center=pos
        
        self.clrSlct=clrSlct
        self.textPrint("Location",20,WHITE,15,0,285)
        self.textPrint("X",20,WHITE,45,0,142)
        self.textPrint("Y",20,WHITE,45,142,142)        
        
    def textPrint(self,txt,txtSize,txtClr,txtY,txtX1,txtX2):
        font1 = pygame.font.SysFont('timesnewroman', txtSize)
        self.loraLabel=txt       
        text1 = font1.render(self.loraLabel, True, txtClr)
        textRect1 = text1.get_rect()
        textRect1.left =txtX1+ int((txtX2-text1.get_rect().width)/2)
        textRect1.centery = txtY
        self.image.blit(text1, textRect1)
    

    def update(self,disX,disY):
        disX=str(disX)+" m"
        disY=str(disY)+ " m"
        pygame.draw.rect(self.image, WHITE, (2,64,283,26))
        pygame.draw.rect(self.image, clrList[self.clrSlct][1], (0,59,144,31),2)
        pygame.draw.rect(self.image, clrList[self.clrSlct][1], (142,59,143,31),2)
        self.textPrint(disX ,17,BLACK,75,0,142)
        self.textPrint(disY ,17,BLACK,75,142,142)

class LoRa(pygame.sprite.Sprite):
    def __init__(self, LLab="L1",pos=(600,75),clrSlct=0):
        pygame.sprite.Sprite.__init__(self)
        
        # self.image = pygame.image.load(r'img\2.png')
        self.image=pygame.Surface((30,30))
        self.image.fill(clrList[clrSlct][0])
        pygame.draw.rect(self.image, clrList[clrSlct][1], (0,0,29,29),2)
        # pygame.draw.line(self.image, RED, [0,0],[20,20] , 2)
        self.rect=self.image.get_rect()
        
        self.rect.center=pos
        
        font1 = pygame.font.SysFont('timesnewroman', 20)
        self.loraLabel=LLab        
        text1 = font1.render(self.loraLabel, True, COL3)
        textRect1 = text1.get_rect()
        textRect1.left = 5
        textRect1.centery = 14
        self.image.blit(text1, textRect1)

class LoRaData(pygame.sprite.Sprite):
    
    def __init__(self, LLab="L1",pos=(1225,100),clrSlct=0):
        pygame.sprite.Sprite.__init__(self)
        
        # self.image = pygame.image.load(r'img\2.png')
        self.image=pygame.Surface((285,62))
        self.image.fill(clrList[clrSlct][0])
        pygame.draw.rect(self.image, WHITE, (53,30,230,30))        
        pygame.draw.rect(self.image, clrList[clrSlct][1], (0,0,285,62),2)
        pygame.draw.rect(self.image, clrList[clrSlct][1], (0,0,53,62),2)
        pygame.draw.rect(self.image, clrList[clrSlct][1], (51,0,116,31),2)
        # pygame.draw.rect(self.image, clrList[clrSlct][1], (52,32,115,31),2)
        # pygame.draw.rect(self.image, clrList[clrSlct][1], (166,30,118,61),2)
        self.rect=self.image.get_rect()
        
        self.rect.center=pos
        
        self.clrSlct=clrSlct

        self.textPrint(LLab,20,COL3,30,0,53)
        self.textPrint("Distance",20,COL3,15,53,115)
        self.textPrint("RSSI",20,COL3,15,168,115)
        
        self.y_speed=0
        
        
    def textPrint(self,txt,txtSize,txtClr,txtY,txtX1,txtX2):
        font1 = pygame.font.SysFont('timesnewroman', txtSize)
        self.loraLabel=txt       
        text1 = font1.render(self.loraLabel, True, txtClr)
        textRect1 = text1.get_rect()
        textRect1.left =txtX1+ int((txtX2-text1.get_rect().width)/2)
        textRect1.centery = txtY
        self.image.blit(text1, textRect1)
        pass
    
    
    def update(self,lrDis,lrRssi):
        dis=str(lrDis)+" m"
        rssi=str(lrRssi)+ " dBm"
        pygame.draw.rect(self.image, WHITE, (54,37,230,22))
        pygame.draw.rect(self.image, clrList[self.clrSlct][1], (165,29,120,33),2)
        self.textPrint(dis ,17,BLACK,45,53,115)
        self.textPrint(rssi ,17,BLACK,45,168,115)

class barrierA(pygame.sprite.Sprite):
    def __init__(self,posB=(280,520)):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load(r'img\bA.png')
        self.image = pygame.transform.rotate(self.image, 180)
        self.rect=self.image.get_rect()
        
        
        
        # self.rect.center=posB
        
        self.rect.left=posB[0]
        self.rect.top=posB[1]
        
        for i in range(0, self.rect.width):
            for j in range(0, self.rect.height):
                renk=[self.image.get_at((i,j))[0],self.image.get_at((i,j))[1],self.image.get_at((i,j))[2]]
                scrnClr[i+self.rect.left][j+self.rect.top]=renk
                # print(i,j,i+self.rect.left,j+self.rect.top,renk)
            
        
        self.cntr=self.rect.center
        self.pos=self.rect.center
        self.y_speed=0
        self.angle_left=1
        self.aci=0
        
class barrierB(pygame.sprite.Sprite):
    def __init__(self,posB=(580,320)):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load(r'img\bB.png')
        self.image = pygame.transform.rotate(self.image, 180)
        self.rect=self.image.get_rect()
        
        # self.rect.center=posB
        
        
        self.rect.left=posB[0]
        self.rect.top=posB[1]
        
        for i in range(0, self.rect.width):
            for j in range(0, self.rect.height):
                renk=[self.image.get_at((i,j))[0],self.image.get_at((i,j))[1],self.image.get_at((i,j))[2]]
                scrnClr[i+self.rect.left][j+self.rect.top]=renk
        
        
        self.cntr=self.rect.center
        self.pos=self.rect.center
        self.y_speed=0
        self.angle_left=1
        self.aci=0
        
class barrierC(pygame.sprite.Sprite):
    def __init__(self,posB=(580,320)):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load(r'img\bC.png')
        self.image = pygame.transform.rotate(self.image, 180)
        self.rect=self.image.get_rect()
        
        # self.rect.center=posB
        
        self.rect.left=posB[0]
        self.rect.top=posB[1]
        
        for i in range(0, self.rect.width):
            for j in range(0, self.rect.height):
                renk=[self.image.get_at((i,j))[0],self.image.get_at((i,j))[1],self.image.get_at((i,j))[2]]
                scrnClr[i+self.rect.left][j+self.rect.top]=renk
        
        
        self.cntr=self.rect.center
        self.pos=self.rect.center
        self.y_speed=0
        self.angle_left=1
        self.aci=0

    
class Player(pygame.sprite.Sprite):
    def __init__(self,pos=(50,50)):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load(r'img\mobil3a.png')
        
        
        self.image = pygame.transform.rotate(self.image, 270)
        #self.image=pygame.Surface((20,20))
        #self.image.fill(BLUE)
        
        self.rect=self.image.get_rect()
        
        self.rect.center=pos
        self.cntr=self.rect.center
        self.pos=self.rect.center
        self.y_speed=0
        self.angle_left=1
        self.aci=0
        # self.a=0
        
    def update(self,action):
        # self.a=self.a+1
        deletePATH=False
        
        keystate = pygame.key.get_pressed()
        
        
        if keystate[pygame.K_c]:
            deletePATH=True
        
        
        if keystate[pygame.K_LEFT] or action == 0:
            self.aci=self.aci+18
            # actions.append(0)
        elif keystate[pygame.K_RIGHT] or action == 1:
            self.aci=self.aci-18
            # actions.append(1)
        elif (keystate[pygame.K_UP] or action == 2):
            self.cntr=(self.rect.width/2+10*math.cos(math.radians(self.aci))+
                       self.rect.left,self.rect.height/2-10*math.sin(math.radians(self.aci))+self.rect.top)
            
            # actions.append(2)
            if self.cntr[0]<LIMIT[0] or self.cntr[0]>LIMIT[1] or self.cntr[1]<LIMIT[2] or self.cntr[1]>LIMIT[3]:
                self.cntr=self.rect.center
            # print(len(pygame.sprite.spritecollide(self, all_sprite, False)))
            
        yedekPos=self.rect.center  
        
                
                
        if(self.aci==360):
            self.aci=0
        if(self.aci<0):
            self.aci=self.aci+360
            
        self.image = pygame.image.load(r'img\mobil3.png')        
        self.image = pygame.transform.rotate(self.image, self.aci)        
        self.rect=self.image.get_rect()
        self.rect.center=self.cntr
        
        if len(pygame.sprite.spritecollide(self, all_sprite, False))>1:
                self.rect.center=yedekPos
        
        return self.aci, self.rect.center,deletePATH
    
    def goPos(self,pos):
        self.rect.center=pos
        reg=True
        if len(pygame.sprite.spritecollide(self, all_sprite, False))>1:
            reg=False            
        return self.rect.center,reg
        



# Sprite listesini yazdıran fonksiyon
def print_sprite_list(sprite_group):
    print("Sprite Listesi:")
    for i, sprite in enumerate(sprite_group):
        print(f"Sprite {i}: Konum: ({sprite.rect.x}, {sprite.rect.y})")

def hipotenus(p1,p2):
        a=pow((p1[0]-p2[0]),2)
        b=pow((p1[1]-p2[1]),2)                   
        h=int(pow((a+b),0.5)) 
        h=round(h*(SCALE/50),2)           
        return h  

def rssiLoss(pointList):    
    barrierRssi=[0,0,0,0,0]
    barrierLoss=[0.75,0.5,1.5,2.5,0.1]
    for i in range(0, len(pointList)):
        
        scrnClr[pointList[i][0]][pointList[i][1]][0]
        pointClr=(scrnClr[pointList[i][0]][pointList[i][1]][0],scrnClr[pointList[i][0]][pointList[i][1]][1],scrnClr[pointList[i][0]][pointList[i][1]][2])
        
        if pointClr==(255,201,14):
            # print("ahşap:",pointList[i])
            barrierRssi[0]=barrierRssi[0]+1
        if pointClr==(185,122,87):
            # print("tuğla:",pointList[i])
            barrierRssi[1]=barrierRssi[1]+1
        if pointClr==(0,162,232):
            # print("cam:",pointList[i])
            barrierRssi[2]=barrierRssi[2]+1
        if pointClr==(127,127,127):
            # print("beton:",pointList[i])
            barrierRssi[3]=barrierRssi[3]+1
        if pointClr==(181,230,29) or pointClr==(34,177,76):
            # print("ağaç:",pointList[i])
            barrierRssi[4]=barrierRssi[4]+1
    
    for i in range(0, len(barrierRssi)):
        barrierRssi[i]=barrierLoss[i]*barrierRssi[i]
    
    totalBarrierLoss=round(sum(barrierRssi),3)
    # print(barrierRssi)
    # print(totalBarrierLoss)
    return totalBarrierLoss


    
def linerEqu(p1,p2):
        point=[]
        xD=p1[0]-p2[0]
        yD=p1[1]-p2[1]
        
        if xD!=0:
            m=yD/xD
            b=p1[1]-m*p1[0]
            if abs(xD)>abs(yD):
                if xD<0:
                    for i in range(p1[0], p2[0]):
                        point.append((i,round(m*i+b)))
                else:
                    for i in range(p2[0], p1[0]):
                        point.append((i,round(m*i+b)))
            else:
                if yD<0:
                    for i in range(p1[1], p2[1]):
                        point.append((round((i-b)/m),i))
                elif yD>0:
                    for i in range(p2[1], p1[1]):
                        point.append((round((i-b)/m),i))
                else:
                    if xD<0:
                        for i in range(p1[1], p2[1]):
                            point.append((i,p1[1]))
                    elif xD>0:
                        for i in range(p2[1], p1[1]):
                            point.append((i,p1[1]))                    
        else:
            if yD<0:
                for i in range(p1[1], p2[1]):
                    point.append((p1[0],i))
            elif yD>0:
                for i in range(p2[1], p1[1]):
                    point.append((p1[0],i))     
        return point
    
def lacation(p):    
        x=round((p[0]-50)*(SCALE/50),2)  
        y=round((p[1]-50)*(SCALE/50),2)            
        return x,y 
    
def lacationINnv(p):     
        x=int(round(((50/SCALE)*p[0])+50))
        y=int(round(((50/SCALE)*p[1])+50))           
        return x,y 
    
def rssiCalc(dist,f,gTX,rTX,barrierLoss):    
    if dist==0:
        dist=0.01
    rssi=-20*math.log(dist, 10)-20*math.log(f, 10)-20*math.log(4*math.pi/299792458, 10)+gTX+rTX-barrierLoss          
    rssi=round(rssi,3)    
    return rssi 
    
def env():
    screen.fill(FON)    
    points=[[LIMIT[0], LIMIT[2]], [LIMIT[1], LIMIT[2]], [LIMIT[1], LIMIT[3]], [LIMIT[0], LIMIT[3]]]    
    pygame.draw.polygon(screen, COL1, points , 5)
    
    V=int((LIMIT[1]-LIMIT[0])/50)-1
    H=int((LIMIT[3]-LIMIT[2])/50)-1
    
    for i in range(0, V):
        draw_dashed_line(screen, COL1, (100+i*50, 50), (100+i*50, LIMIT[3]))
    for i in range(0, H):
        draw_dashed_line(screen, COL1, (50, 100+i*50), (LIMIT[1], 100+i*50))
    

def draw_dashed_line(screen, color, start_pos, end_pos, dash_length=5, space_length=5):
    # Başlangıç ve bitiş noktalarının farkı
    x1, y1 = start_pos
    x2, y2 = end_pos
    total_length = math.hypot(x2 - x1, y2 - y1)  # Çizgi uzunluğu
    dash_count = int(total_length // (dash_length + space_length))  # Çizgi ve boşluk toplamı

    # X ve Y yönündeki adımlar
    dx = (x2 - x1) / dash_count
    dy = (y2 - y1) / dash_count

    # Çizgileri çizme
    for i in range(dash_count):
        start = (x1 + i * dx, y1 + i * dy)
        end = (x1 + (i + 0.5) * dx, y1 + (i + 0.5) * dy)
        pygame.draw.line(screen, color, start, end, 2)


pygame.init()
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Lora")
clock=pygame.time.Clock()

all_sprite=pygame.sprite.Group()

personNum=1

persons=[]
for i in range(0, personNum):
    persons.append(Player(pos=(50+i*100,50)))


# mobil=Player()


LRmodulPos=[[(25,25),0],[(25,425),1],[(25,825),2],[(550,825),3],[(1075,825),4],[(1075,425),5],[(1075,25),6],[(550,25),8],[(550,425),9]]
LRmodulNum=len(LRmodulPos)
LRmodul=[]
LRmodulData=[]
for i in range(1, LRmodulNum+1):
    LRmodul.append(LoRa(LLab="L"+str(i),pos=LRmodulPos[i-1][0],clrSlct=LRmodulPos[i-1][1]))
    LRmodulData.append(LoRaData(LLab="L"+str(i),pos=(1260,110+75*i),clrSlct=LRmodulPos[i-1][1]))

disData=lacationData()


"""

barrierList=[]


for i in range(0, 5):
    barrierList.append(barrierA(posB=(180+i*120,620)))
    
    if(i!=1 and i!=3):
        barrierList.append(barrierB(posB=(800,150+i*60)))
        barrierList.append(barrierB(posB=(920,150+i*60)))
        barrierList.append(barrierB(posB=(180+i*50,200)))

for i in range(0, 10):
    for j in range(0, 3):
        barrierList.append(barrierC(posB=(170+i*25,300+j*25)))
        
for i in range(0, 6):
    for j in range(0, 8):
        barrierList.append(barrierC(posB=(812+i*25,512+j*25)))
"""

barrierList=[]

bA=[(100,650),(160,440),(280,90),(540,230),(850,300),(730,520),(390,690),(750,700),(250,550),(540,65)]
bB=[(120,130),(130,300),(400,480),(540,600),(630,390),(700,140),(970,230),(970,600),(900,700),(65,500)]
bC=[(200,720),(300,325),(350,225),(410,360),(450,100),(540,720),(770,230),(950,90),(910,420),(880,560)]


for i in range(0, len(bA)):
    barrierList.append(barrierA(posB=bA[i]))
    barrierList.append(barrierB(posB=bB[i]))
    barrierList.append(barrierC(posB=(bC[i][0],bC[i][1])))
    barrierList.append(barrierC(posB=(bC[i][0]+25,bC[i][1])))
    barrierList.append(barrierC(posB=(bC[i][0],bC[i][1]+25)))
    barrierList.append(barrierC(posB=(bC[i][0]+25,bC[i][1]+25)))

# all_sprite.add(mobil)

for i in range(0, personNum):    
    all_sprite.add(persons[i])


for i in range(0, LRmodulNum):
    all_sprite.add(LRmodul[i])
    all_sprite.add(LRmodulData[i])

all_sprite.add(disData)

for i in range(0, len(barrierList)):
    all_sprite.add(barrierList[i])

# print_sprite_list(all_sprite)

running=True

locStatus=[]
rssiStatus=[]

locStatus2=[]
rssiStatus2=[]

mobilPATH=[]
mobilPATHPred=[]

personPATH=[]


personPATHPred3L=[]
personPATHPred5L=[]
personPATHPred9L=[]

for j in range(0, personNum):
    personPATH.append([])
    personPATHPred3L.append([])
    personPATHPred5L.append([])
    personPATHPred9L.append([])
    
for i in range(0, LRmodulNum):
    locStatus.append([0,0])
    rssiStatus.append(0)

for j in range(0, personNum):
    personLocStatus=[]
    personRssiStatus=[]
    for i in range(0, LRmodulNum):
        personLocStatus.append([0,0])
        personRssiStatus.append(0)
    locStatus2.append(personLocStatus)
    rssiStatus2.append(personRssiStatus)

# j=0

lX=50
lY=50
dataSet=[]

path=[]
while running:
    clock.tick(FPS)

    #process input
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
            
    #update
    
    personStatus=[]
    
    for i in range(0, personNum):
        personStatus.append(persons[i].update(3))
 
    # a,mC,pathDelete=mobil.update(3)
    # if pathDelete==True:
    #     mobilPATH=[list(mC)]
    #     mobilPATHPred=[list(mC)]
        
    pathControl=False
    for j in range(0, personNum):
        if personStatus[j][2]==True:
            pathControl=True
            
    if pathControl==True:
        personPATH=[]
        personPATHPred3L=[]
        personPATHPred5L=[]
        personPATHPred9L=[]
        personPATHPred3L.append([])
        personPATHPred5L.append([])  
        personPATHPred9L.append([])         
        for j in range(0, personNum):
            personPATH.append([])
            personPATHPred3L.append([])
            personPATHPred5L.append([])
            personPATHPred9L.append([])

        
    
        
    # mC,regStatus=mobil.goPos((lX,lY))
 
    chng=0
    # for i in range(0, LRmodulNum):        
    #     locStatus[i][1]=hipotenus(LRmodul[i].rect.center,mC)
    #     if locStatus[i][1]!=locStatus[i][0]:
    #         chng=1  
            
    for j in range(0, personNum):        
        for i in range(0, LRmodulNum): 
            locStatus2[j][i][1]=hipotenus(LRmodul[i].rect.center,personStatus[j][1])
            if locStatus2[j][i][1]!=locStatus2[j][i][0]:
                chng=1 
    
    signal=[]
    # if chng==1:
    #     for i in range(0, LRmodulNum):
    #         locStatus[i][0]=locStatus[i][1]
    #         rssiStatus[i]=rssiCalc(locStatus[i][1],FREQ,GTX,GRX,rssiLoss(linerEqu(LRmodulPos[i][0],mC)))
    #         LRmodulData[i].update(locStatus[i][1],rssiStatus[i])
    #         signal.append(rssiStatus[i])
    #     disData.update(lacation(mC)[0],lacation(mC)[1])
    #     mobilPATH.append(mC)
    #     arr = np.array(valueCreate(signal))
    #     xTahmin=normalize(modelA.predict(arr)[0][0],0,1,0,800)
    #     yTahmin=normalize(modelA.predict(arr)[0][1],0,1,0,600)
          
    #     mobilPATHPred.append((lacationINnv((xTahmin,yTahmin))))

    
    if chng==1:
        for j in range(0, personNum):
            signal=[] 
            signal3=[] 
            signal5=[]
            signal9=[]            
            for i in range(0, LRmodulNum):
                locStatus2[j][i][0]=locStatus2[j][i][1]
                rssiStatus2[j][i]=rssiCalc(locStatus2[j][i][1],FREQ,GTX,GRX,rssiLoss(linerEqu(LRmodulPos[i][0],personStatus[j][1])))
                LRmodulData[i].update(locStatus2[0][i][1],rssiStatus2[0][i])
                signal9.append(rssiStatus2[j][i])
                if(i==2 or i==4 or i==7 ):
                    signal3.append(rssiStatus2[j][i])
                if(i==0 or i==2 or i==4 or i==6 or i==8 ):
                    signal5.append(rssiStatus2[j][i])
                    
            disData.update(lacation(personStatus[0][1])[0],lacation(personStatus[0][1])[1])
            personPATH[j].append(personStatus[j][1])
            
            arr = np.array(valueCreate(signal3,3))
            xTahmin=normalize(model3L.predict(arr)[0][0],0,1,0,800)
            yTahmin=normalize(model3L.predict(arr)[0][1],0,1,0,600)                        
            personPATHPred3L[j].append((lacationINnv((xTahmin,yTahmin))))
            
            arr = np.array(valueCreate(signal5,5))
            xTahmin=normalize(model5L.predict(arr)[0][0],0,1,0,800)
            yTahmin=normalize(model5L.predict(arr)[0][1],0,1,0,600)                        
            personPATHPred5L[j].append((lacationINnv((xTahmin,yTahmin))))
            
            arr = np.array(valueCreate(signal9,9))
            xTahmin=normalize(model9L.predict(arr)[0][0],0,1,0,800)
            yTahmin=normalize(model9L.predict(arr)[0][1],0,1,0,600)                        
            personPATHPred9L[j].append((lacationINnv((xTahmin,yTahmin))))

            
    
    
    """
    fmt=[]
    for i in range(0, LRmodulNum+2):
        fmt.append("%.3f")

    lX=lX+5
    if lX>1050:
        lX=50
        lY=lY+5
        if lY>804:
            import numpy as np
            import pandas as pd
            df = pd.DataFrame(dataSet)
            # fmt = ["%.3f","%.3f","%.3f","%.2f","%.2f"]
            np.savetxt("dataSet_"+str(LRmodulNum)+"L.csv", df, fmt=fmt, delimiter=",")
            print("dataSet tamamlandı!")
            lY=50 
            
    

    if regStatus==True:
        rawDataset=[]
        for i in range(0, LRmodulNum):
            rawDataset.append(rssiStatus[i])
        rawDataset.append(lacation(mC)[0])
        rawDataset.append(lacation(mC)[1])        
        dataSet.append(rawDataset)
    """
 
    env();    
    all_sprite.draw(screen)
    

    
    # if len(mobilPATH)>1:
    #     for i in range(1, len(mobilPATH)):
    #         pygame.draw.line(screen, RED, list(mobilPATH)[i-1],list(mobilPATH)[i], 5)
    #         pygame.draw.line(screen, BLUE, list(mobilPATHPred)[i-1],list(mobilPATHPred)[i], 2)
            
    #     transparent_surface = pygame.Surface((100,100), pygame.SRCALPHA)
    #     pygame.draw.circle(transparent_surface, (0, 0, 255, 64), (50,50), 50)
    #     screen.blit(transparent_surface, (list(mobilPATHPred)[len(mobilPATHPred)-1][0]-50,list(mobilPATHPred)[len(mobilPATHPred)-1][1]-50))

    if len(personPATH[j])>1:
        for j in range(0, personNum):
            for i in range(1, len(personPATH[j])):
                pygame.draw.line(screen, BLACK, list(personPATH[j])[i-1],list(personPATH[j])[i], 5)
                pygame.draw.line(screen, model1Clr, list(personPATHPred3L[j])[i-1],list(personPATHPred3L[j])[i], 4)
                pygame.draw.line(screen, model2Clr, list(personPATHPred5L[j])[i-1],list(personPATHPred5L[j])[i], 4)
                pygame.draw.line(screen, model3Clr, list(personPATHPred9L[j])[i-1],list(personPATHPred9L[j])[i], 4)
                
            """
            transparent_surface = pygame.Surface((100,100), pygame.SRCALPHA)
            pygame.draw.circle(transparent_surface, (0, 0, 255, 64), (50,50), 50)
            screen.blit(transparent_surface, (list(personPATHPred3L[j])[len(personPATHPred3L[j])-1][0]-50,list(personPATHPred3L[j])[len(personPATHPred3L[j])-1][1]-50))
            """
    
    
    """
    for i in range(0, len(pxx)):
        pygame.draw.circle(screen, BLACK, pxx[i], 1)
    """    
    
  
    pygame.display.flip()
    
    # keystate = pygame.key.get_pressed()
    
    if pygame.key.get_pressed()[pygame.K_s]:
        pygame.image.save(screen, 'ekran_goruntusu_v2.png')
        
        # Ekranın belirli bir bölümünü seçmek için bir dikdörtgen (x, y, genişlik, yükseklik)
        rect = pygame.Rect(0, 0, 1100, 850)  # Bu 100x100 piksel bir bölüm seçiyor
        
        # Ekranın seçilen bölgesini al ve kaydet
        subsurface = screen.subsurface(rect)
        pygame.image.save(subsurface, 'ekran_bolumu_v2.png')
    

pygame.quit()