
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
        pygame.draw.rect(surface, brown, (int(self.x), 0, self.width, self.top_heigth))
        #วางถ่อล้าง
        pygame.draw.rect(surface, brown, (int(self.x), self.top_heigth + self.gab, self.width, HEIGH - (self.top_heigth + self.gab)))
    
    def get_rects(self):
         # ส่งค่า Hitbox ของทั้งท่อบนและท่อล่างกลับไป
        top_rect = pygame.Rect(int(self.x), 0, self.width, self.top_heigth)
        bottom_rect = pygame.Rect(int(self.x), self.top_heigth + self.gab, self.width, HEIGH - (self.top_heigth + self.gab))
        return top_rect, bottom_rect

    
    
pipes = []
spawn_pipe_time = 0

running = True
while running:
    # ตั้งค่า Framerate ไว้ที่ 60 FPS
    clock.tick(60)
    
    # ตรวจสอบ Event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # วาดพื้นหลัง
    screen.blit(bg, (0, 0))
    
    # สร้างท่อใหม่ทุกๆ 100 เฟรม
    spawn_pipe_time += 1
    if spawn_pipe_time > 100:
        pipes.append(Pipe(WIDTH))
        spawn_pipe_time = 0
        
    # อัปเดตและวาดท่อทั้งหมด
    for pipe in pipes[:]:
        pipe.update()
        pipe.draw(screen)

        # ลบท่อที่หลุดหน้าจอไปแล้วเพื่อประหยัดความจำ
        if pipe.x < -pipe.width:
            pipes.remove(pipe)

    pygame.display.update()

pygame.quit()
sys.exit()