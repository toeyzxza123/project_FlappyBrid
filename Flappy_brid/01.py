import pygame
import random 
import sys

pygame.init() 
WIDTH,HEIGH = 400,500
screen = pygame.display.set_mode((WIDTH,HEIGH)) #ขนานหน้าจอ
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock() #เฟรมเรท

font_score = pygame.font.SysFont("sarabun TH",20)
font_gamrover = pygame.font.SysFont("sarabun TH",20)

#สี
blue = (135,206,235)
red = (255,0,0)
yello = (255,215,0)
brown = (165,42,42)

screen.fill(blue) #สีหน้าจอ
massage_taxt1 = font_score.render("SCORE :",True,red)
massage_taxt2 = font_gamrover.render("GAME OVER",True,red)

#พื้นหลัง
bg = pygame.image.load("Flappy_brid/bg.png.jpg")
bg = pygame.transform.scale(bg,(400,500))

class brid:
    def __init__(self):
        self.x = 100
        self.y = 300
        self.size = 30
        self.gravity = 0.4
        self.velocity = 0
        self.jump_force = -8

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity

    def jump(self):
        self.velocity = self.jump_force

    def draw(self,surface):
        pygame.draw.circle(surface , (yello) , (self.x,int(self.y)),self.size//2)

    def get_rect(self):
        return pygame.Rect(self.x - self.size//2, int(self.y) - self.size//2, self.size, self.size)

class Pipe :
    def __init__(self,x_pos):
        self.x = float(x_pos)
        self.width = 60
        self.gab = 150
        self.speed = 3
        self.top_heigth = random.randint(100,HEIGH - self.gab - 100)
        self.passed = False

    def update(self):
        self.x -= self.speed

    def draw(self, surface):
        #วางถ่อบน
        pygame.draw.rect(surface,(brown),(int(self.x),0,self.width,self.top_heigth))
        #วางถ่อล้าง
        pygame.draw.rect(surface,(brown),(int(self.x),self.top_heigth,self.gab,self.width,HEIGH-(self.top_heigth+self.gab)))
    
    def get_rects(self):
         # ส่งค่า Hitbox ของทั้งท่อบนและท่อล่างกลับไป
        top_rect = pygame.Rect(int(self.x),0,self.width,self.top_heigth)
        botton_ract = pygame.Rect(int(self.x),self.top_heigth,self.gab,self.width,HEIGH-(self.top_heigth+self.gab))
        return top_rect,botton_ract


running = True
while running :
    for even in pygame.event.get():
        if even.type == pygame.QUIT:
            running = False

    screen.blit(bg,(0,0))
    pygame.display.update()
pygame.quit()
